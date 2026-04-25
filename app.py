from flask import Flask, render_template, request, redirect, session
from db import get_connection
import math
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "smart_delivery_secret")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_nearest_driver(pickup_x, pickup_y):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM drivers WHERE status='available'")
    drivers = cursor.fetchall()

    nearest_driver = None
    shortest_distance = None

    for driver in drivers:
        distance = calculate_distance(
            pickup_x,
            pickup_y,
            driver["current_x"],
            driver["current_y"]
        )

        if shortest_distance is None or distance < shortest_distance:
            shortest_distance = distance
            nearest_driver = driver

    cursor.close()
    conn.close()

    return nearest_driver, shortest_distance


def add_notification(user_id, title, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notifications (user_id, title, message) VALUES (%s, %s, %s)",
        (user_id, title, message)
    )

    conn.commit()
    cursor.close()
    conn.close()


def is_market_open(open_time, close_time):
    if open_time is None or close_time is None:
        return False

    now = datetime.now()

    open_seconds = open_time.total_seconds()
    close_seconds = close_time.total_seconds()
    now_seconds = now.hour * 3600 + now.minute * 60 + now.second

    return open_seconds <= now_seconds <= close_seconds

from datetime import timedelta

def update_expired_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status='delivered',
            delivered_at=NOW(),
            estimated_minutes=0
        WHERE payment_status='paid'
        AND status IN ('assigned', 'picked_up')
        AND created_at <= (NOW() - INTERVAL 30 MINUTE)
        """
    )

    cursor.execute(
        """
        UPDATE drivers
        SET status='available'
        WHERE id NOT IN (
            SELECT driver_id FROM orders
            WHERE driver_id IS NOT NULL
            AND status IN ('assigned', 'picked_up')
        )
        """
    )

    conn.commit()
    cursor.close()
    conn.close()


def calculate_custom_price(pickup_x, pickup_y, delivery_x, delivery_y):
    distance = calculate_distance(pickup_x, pickup_y, delivery_x, delivery_y)
    return round(20 + distance * 2, 2)

@app.route("/")
def login_page():
    return render_template("auth/login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        session["full_name"] = user["full_name"]

        if user["role"] == "admin":
            return redirect("/admin")
        elif user["role"] == "driver":
            return redirect("/driver")
        return redirect("/customer")

    return render_template("auth/login.html", error="Wrong email or password")


@app.route("/register")
def register_page():
    return render_template("auth/register.html")


@app.route("/register", methods=["POST"])
def register():
    full_name = request.form["full_name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        return render_template("auth/register.html", error="Email already exists")

    cursor.execute(
        "INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, 'customer')",
        (full_name, email, password)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/customer")
def customer_dashboard():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    return render_template("customer/dashboard.html")


@app.route("/create_order")
def create_order_page():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    return render_template(
    "customer/create_order.html",
    google_api_key=GOOGLE_API_KEY
)


@app.route("/create_order", methods=["POST"])
def create_order():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    pickup_address = request.form["pickup_address"]
    delivery_address = request.form["delivery_address"]

    if request.form["pickup_x"] == "" or request.form["pickup_y"] == "" or request.form["delivery_x"] == "" or request.form["delivery_y"] == "":
        return redirect("/create_order")

    pickup_x = float(request.form["pickup_x"])
    pickup_y = float(request.form["pickup_y"])
    delivery_x = float(request.form["delivery_x"])
    delivery_y = float(request.form["delivery_y"])

    package_description = request.form["package_description"]

    total_price = calculate_custom_price(pickup_x, pickup_y, delivery_x, delivery_y)

    nearest_driver, distance = find_nearest_driver(pickup_x, pickup_y)

    conn = get_connection()
    cursor = conn.cursor()

    if nearest_driver:
        cursor.execute(
            """
            INSERT INTO orders
            (customer_id, driver_id, pickup_address, delivery_address,
            pickup_x, pickup_y, delivery_x, delivery_y,
            package_description, status, distance_to_driver, total_price, payment_status, estimated_minutes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'assigned', %s, %s, 'unpaid', 30)
            """,
            (
                session["user_id"],
                nearest_driver["id"],
                pickup_address,
                delivery_address,
                pickup_x,
                pickup_y,
                delivery_x,
                delivery_y,
                package_description,
                distance,
                total_price
            )
        )

        order_id = cursor.lastrowid

        cursor.execute(
            "UPDATE drivers SET status='busy' WHERE id=%s",
            (nearest_driver["id"],)
        )

        cursor.execute(
            "INSERT INTO order_tracking (order_id, status, note) VALUES (%s, %s, %s)",
            (order_id, "assigned", "Nearest driver assigned automatically")
        )

    else:
        cursor.execute(
            """
            INSERT INTO orders
            (customer_id, pickup_address, delivery_address,
            pickup_x, pickup_y, delivery_x, delivery_y,
            package_description, status, total_price, payment_status, estimated_minutes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s, 'unpaid', 30)
            """,
            (
                session["user_id"],
                pickup_address,
                delivery_address,
                pickup_x,
                pickup_y,
                delivery_x,
                delivery_y,
                package_description,
                total_price
            )
        )

        order_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO order_tracking (order_id, status, note) VALUES (%s, %s, %s)",
            (order_id, "pending", "No available driver now")
        )

    conn.commit()
    cursor.close()
    conn.close()

    add_notification(
        session["user_id"],
        "Custom Delivery Created",
        f"Your custom delivery order #{order_id} was created."
    )

    return redirect(f"/pay_order/{order_id}")


@app.route("/markets")
def markets():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM markets WHERE is_active=1 ORDER BY id DESC")
    markets_list = cursor.fetchall()

    for market in markets_list:
        market["is_open_now"] = is_market_open(market["open_time"], market["close_time"])

    cursor.close()
    conn.close()

    return render_template("customer/markets.html", markets=markets_list)


@app.route("/market/<int:market_id>")
def market_menu(market_id):
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM markets WHERE id=%s", (market_id,))
    market = cursor.fetchone()

    if not market:
        cursor.close()
        conn.close()
        return redirect("/markets")

    market["is_open_now"] = is_market_open(market["open_time"], market["close_time"])

    cursor.execute(
        "SELECT * FROM products WHERE market_id=%s ORDER BY id DESC",
        (market_id,)
    )
    products = cursor.fetchall()

    for product in products:
        product["can_order"] = (
            market["is_open_now"] == True
            and product["is_available"] == 1
            and market["is_active"] == 1
        )

    cursor.close()
    conn.close()

    return render_template("customer/market_menu.html", market=market, products=products)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if "user_id" not in session:
        return redirect("/login")

    product_id = request.form.get("product_id")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, quantity FROM cart_items
        WHERE customer_id=%s AND product_id=%s
    """, (session["user_id"], product_id))

    item = cursor.fetchone()

    if item:
        cursor.execute("""
            UPDATE cart_items
            SET quantity = quantity + 1
            WHERE id=%s
        """, (item[0],))
    else:
        cursor.execute("""
            INSERT INTO cart_items (customer_id, product_id, quantity)
            VALUES (%s, %s, 1)
        """, (session["user_id"], product_id))

    conn.commit()
    cursor.close()
    conn.close()

    session["success"] = "Added to cart successfully ✅"
    return redirect(request.referrer)


@app.route("/cart")
def cart():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            cart_items.id AS cart_id,
            cart_items.quantity,
            products.id AS product_id,
            products.name,
            products.price,
            products.image_url
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id
        WHERE cart_items.customer_id = %s
        ORDER BY cart_items.created_at DESC
        """,
        (session["user_id"],)
    )

    cart_items = cursor.fetchall()

    total = 0
    for item in cart_items:
        total += float(item["price"]) * int(item["quantity"])

    cursor.close()
    conn.close()

    return render_template("customer/cart.html", cart_items=cart_items, total=total)


@app.route("/remove_from_cart/<int:item_id>")
def remove_from_cart(item_id):
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM cart_items WHERE id=%s AND customer_id=%s",
        (item_id, session["user_id"])
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/cart")


@app.route("/checkout")
def checkout_page():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT cart_items.quantity, products.price
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id
        WHERE cart_items.customer_id=%s
        """,
        (session["user_id"],)
    )

    items = cursor.fetchall()
    total = sum(item["price"] * item["quantity"] for item in items)

    cursor.close()
    conn.close()

    if len(items) == 0:
        return render_template("customer/cart.html", cart_items=[], total=0, empty_cart=True)

    return render_template(
    "customer/checkout.html",
    total=total,
    google_api_key=GOOGLE_API_KEY
)


@app.route("/checkout", methods=["POST"])
def checkout():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    delivery_address = request.form["delivery_address"]

    if request.form["delivery_x"] == "" or request.form["delivery_y"] == "":
        return redirect("/checkout")

    delivery_x = float(request.form["delivery_x"])
    delivery_y = float(request.form["delivery_y"])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT cart_items.quantity,
               products.name AS product_name,
               products.price,
               products.market_id,
               markets.name AS market_name,
               markets.address AS market_address,
               markets.latitude,
               markets.longitude
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id
        JOIN markets ON products.market_id = markets.id
        WHERE cart_items.customer_id=%s
        """,
        (session["user_id"],)
    )

    items = cursor.fetchall()

    if not items:
        cursor.close()
        conn.close()
        return redirect("/cart")

    market_id = items[0]["market_id"]
    pickup_address = items[0]["market_address"]
    if items[0]["latitude"] is None or items[0]["longitude"] is None:
     return "Market location is missing. Please contact admin."

    pickup_x = float(items[0]["latitude"])
    pickup_y = float(items[0]["longitude"])

    total = 0
    description_parts = []

    for item in items:
        total += item["price"] * item["quantity"]
        description_parts.append(f"{item['product_name']} x{item['quantity']}")

    package_description = ", ".join(description_parts)

    nearest_driver, distance = find_nearest_driver(pickup_x, pickup_y)

    if nearest_driver:
        cursor.execute(
            """
            INSERT INTO orders
            (customer_id, driver_id, market_id, pickup_address, delivery_address,
            pickup_x, pickup_y, delivery_x, delivery_y,
            package_description, status, distance_to_driver, total_price, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'assigned', %s, %s, 'unpaid')
            """,
            (
                session["user_id"],
                nearest_driver["id"],
                market_id,
                pickup_address,
                delivery_address,
                pickup_x,
                pickup_y,
                delivery_x,
                delivery_y,
                package_description,
                distance,
                total
            )
        )

        order_id = cursor.lastrowid

        cursor.execute(
            "UPDATE drivers SET status='busy' WHERE id=%s",
            (nearest_driver["id"],)
        )

    else:
        cursor.execute(
            """
            INSERT INTO orders
            (customer_id, market_id, pickup_address, delivery_address,
            pickup_x, pickup_y, delivery_x, delivery_y,
            package_description, status, total_price, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s, 'unpaid')
            """,
            (
                session["user_id"],
                market_id,
                pickup_address,
                delivery_address,
                pickup_x,
                pickup_y,
                delivery_x,
                delivery_y,
                package_description,
                total
            )
        )

        order_id = cursor.lastrowid

    for item in items:
        cursor.execute(
            """
            INSERT INTO order_items (order_id, product_name, quantity, price)
            VALUES (%s, %s, %s, %s)
            """,
            (order_id, item["product_name"], item["quantity"], item["price"])
        )

    cursor.execute(
        "INSERT INTO order_tracking (order_id, status, note) VALUES (%s, %s, %s)",
        (order_id, "created", "Market order created")
    )

    cursor.execute(
        "DELETE FROM cart_items WHERE customer_id=%s",
        (session["user_id"],)
    )

    conn.commit()
    cursor.close()
    conn.close()

    add_notification(session["user_id"], "Market Order Created", f"Order #{order_id} was created.")

    return redirect(f"/pay_order/{order_id}")


@app.route("/pay_order/<int:order_id>")
def pay_order(order_id):
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM orders WHERE id=%s AND customer_id=%s",
        (order_id, session["user_id"])
    )

    order = cursor.fetchone()

    cursor.close()
    conn.close()

    if not order:
        return redirect("/track_order")

    return render_template("customer/pay_order.html", order=order)


@app.route("/demo_pay/<int:order_id>", methods=["POST"])
def demo_pay(order_id):
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    card_name = request.form.get("card_name")
    card_number = request.form.get("card_number")
    expiry = request.form.get("expiry")
    cvv = request.form.get("cvv")

    if not card_name or not card_number or not expiry or not cvv:
        return redirect(f"/pay_order/{order_id}")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET payment_status='paid'
        WHERE id=%s AND customer_id=%s
        """,
        (order_id, session["user_id"])
    )

    cursor.execute(
        """
        INSERT INTO order_tracking (order_id, status, note)
        VALUES (%s, %s, %s)
        """,
        (order_id, "paid", "Demo payment completed")
    )

    conn.commit()
    cursor.close()
    conn.close()


    return render_template("customer/payment_success.html", order_id=order_id)


@app.route("/track_order")
def track_order():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    update_expired_orders()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT orders.*, users.full_name AS driver_name
        FROM orders
        LEFT JOIN drivers ON orders.driver_id = drivers.id
        LEFT JOIN users ON drivers.user_id = users.id
        WHERE orders.customer_id=%s
        ORDER BY orders.created_at DESC
        """,
        (session["user_id"],)
    )

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("customer/track_order.html", orders=orders)


@app.route("/notifications")
def notifications():
    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM notifications WHERE user_id=%s ORDER BY created_at DESC",
        (session["user_id"],)
    )

    notifications_list = cursor.fetchall()

    cursor.execute(
        "UPDATE notifications SET is_read=1 WHERE user_id=%s",
        (session["user_id"],)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return render_template("customer/notifications.html", notifications=notifications_list)


@app.route("/driver")
def driver_dashboard():
    if "user_id" not in session or session["role"] != "driver":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM drivers WHERE user_id=%s", (session["user_id"],))
    driver = cursor.fetchone()

    if not driver:
        cursor.close()
        conn.close()
        return "Driver profile not found"

    cursor.execute(
        """
        SELECT orders.*, users.full_name AS customer_name
        FROM orders
        JOIN users ON orders.customer_id = users.id
        WHERE orders.driver_id=%s
        ORDER BY orders.created_at DESC
        """,
        (driver["id"],)
    )

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("driver/dashboard.html", orders=orders, driver=driver)


@app.route("/update_order_status/<int:order_id>/<status>")
def update_order_status(order_id, status):
    if "user_id" not in session or session["role"] != "driver":
        return redirect("/")

    allowed_status = ["picked_up", "delivered"]

    if status not in allowed_status:
        return redirect("/driver")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT orders.*, drivers.user_id AS driver_user_id
        FROM orders
        JOIN drivers ON orders.driver_id = drivers.id
        WHERE orders.id=%s AND drivers.user_id=%s
        """,
        (order_id, session["user_id"])
    )

    order = cursor.fetchone()

    if not order:
        cursor.close()
        conn.close()
        return redirect("/driver")

    if status == "picked_up":
     cursor.execute(
        "UPDATE orders SET status=%s, picked_up_at=NOW(), estimated_minutes=25 WHERE id=%s",
        (status, order_id)
    )
    elif status == "delivered":
     cursor.execute(
        "UPDATE orders SET status=%s, delivered_at=NOW(), estimated_minutes=0 WHERE id=%s",
        (status, order_id)
    )

    cursor.execute(
        "INSERT INTO order_tracking (order_id, status, note) VALUES (%s, %s, %s)",
        (order_id, status, "Status updated by driver")
    )

    if status == "delivered":
        cursor.execute(
            "UPDATE drivers SET status='available' WHERE id=%s",
            (order["driver_id"],)
        )

    conn.commit()
    cursor.close()
    conn.close()

    add_notification(order["customer_id"], "Order Updated", f"Your order #{order_id} is now {status}.")

    return redirect("/driver")


@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM orders")
    total_orders = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM orders WHERE status='pending'")
    pending_orders = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM orders WHERE status='delivered'")
    delivered_orders = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM users WHERE role='customer'")
    total_customers = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM users WHERE role='driver'")
    total_drivers = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT orders.*, customers.full_name AS customer_name, drivers_users.full_name AS driver_name
        FROM orders
        JOIN users AS customers ON orders.customer_id = customers.id
        LEFT JOIN drivers ON orders.driver_id = drivers.id
        LEFT JOIN users AS drivers_users ON drivers.user_id = drivers_users.id
        ORDER BY orders.created_at DESC
        """
    )

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin/dashboard.html",
        orders=orders,
        total_orders=total_orders,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        total_customers=total_customers,
        total_drivers=total_drivers
    )


@app.route("/admin_drivers")
def admin_drivers():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT drivers.*, users.full_name, users.email
        FROM drivers
        JOIN users ON drivers.user_id = users.id
        ORDER BY drivers.id DESC
        """
    )

    drivers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/drivers.html", drivers=drivers)


@app.route("/admin_customers")
def admin_customers():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE role='customer' ORDER BY id DESC")
    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/customers.html", customers=customers)


@app.route("/admin_markets")
def admin_markets():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM markets ORDER BY id DESC")
    markets_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/markets.html", markets=markets_list)

@app.route("/support")
def support_page():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM orders WHERE customer_id=%s ORDER BY created_at DESC",
        (session["user_id"],)
    )
    orders = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM support_tickets WHERE customer_id=%s ORDER BY created_at DESC",
        (session["user_id"],)
    )
    tickets = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("customer/support.html", orders=orders, tickets=tickets)


@app.route("/support", methods=["POST"])
def create_support_ticket():
    if "user_id" not in session or session["role"] != "customer":
        return redirect("/")

    order_id = request.form.get("order_id")
    subject = request.form["subject"]
    message = request.form["message"]

    if order_id == "":
        order_id = None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO support_tickets (customer_id, order_id, subject, message)
        VALUES (%s, %s, %s, %s)
        """,
        (session["user_id"], order_id, subject, message)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/support")


@app.route("/admin_support")
def admin_support():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT support_tickets.*, users.full_name, users.email
        FROM support_tickets
        JOIN users ON support_tickets.customer_id = users.id
        ORDER BY support_tickets.created_at DESC
        """
    )

    tickets = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/support.html", tickets=tickets)


@app.route("/admin_orders")
def admin_orders():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    update_expired_orders()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT orders.*, customers.full_name AS customer_name, drivers_users.full_name AS driver_name
        FROM orders
        JOIN users AS customers ON orders.customer_id = customers.id
        LEFT JOIN drivers ON orders.driver_id = drivers.id
        LEFT JOIN users AS drivers_users ON drivers.user_id = drivers_users.id
        ORDER BY orders.created_at DESC
        """
    )
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/orders.html", orders=orders)


@app.route("/admin_update_order/<int:order_id>/<status>")
def admin_update_order(order_id, status):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    allowed = ["pending", "assigned", "picked_up", "delivered", "cancelled"]

    if status not in allowed:
        return redirect("/admin_orders")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if status == "picked_up":
        cursor.execute(
            "UPDATE orders SET status=%s, picked_up_at=NOW(), estimated_minutes=25 WHERE id=%s",
            (status, order_id)
        )
    elif status == "delivered":
        cursor.execute(
            "UPDATE orders SET status=%s, delivered_at=NOW(), estimated_minutes=0 WHERE id=%s",
            (status, order_id)
        )

        cursor.execute("SELECT driver_id FROM orders WHERE id=%s", (order_id,))
        order = cursor.fetchone()

        if order and order["driver_id"]:
            cursor.execute(
                "UPDATE drivers SET status='available' WHERE id=%s",
                (order["driver_id"],)
            )
    else:
        cursor.execute(
            "UPDATE orders SET status=%s WHERE id=%s",
            (status, order_id)
        )

    cursor.execute(
        "INSERT INTO order_tracking (order_id, status, note) VALUES (%s, %s, %s)",
        (order_id, status, "Status updated by admin")
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/admin_orders")


@app.route("/admin_add_market", methods=["GET", "POST"])
def admin_add_market():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        open_time = request.form.get("open_time")
        close_time = request.form.get("close_time")

        # 🔥 صورة محلية تلقائية حسب الاسم
        image_file = name.lower().replace(" ", "-") + ".jpg"
        image_path = "/static/images/markets/" + image_file

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO markets (name, address, latitude, longitude, open_time, close_time, is_active, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, 1, %s)
            """,
            (name, address, latitude, longitude, open_time, close_time, image_path)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/admin_markets")

    return render_template("admin/add_market.html")


@app.route("/admin_delete_market/<int:market_id>")
def admin_delete_market(market_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM markets WHERE id=%s", (market_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/admin_markets")


@app.route("/admin_market_products/<int:market_id>")
def admin_market_products(market_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM markets WHERE id=%s", (market_id,))
    market = cursor.fetchone()

    cursor.execute("SELECT * FROM products WHERE market_id=%s ORDER BY id DESC", (market_id,))
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/products.html", market=market, products=products)


@app.route("/admin_add_product/<int:market_id>", methods=["GET", "POST"])
def admin_add_product(market_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]

        # image file from local project folder
        image_file = request.form["image_file"]
        image_url = "/static/images/products/" + image_file

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO products (market_id, name, description, price, image_url, is_available)
            VALUES (%s, %s, %s, %s, %s, 1)
            """,
            (market_id, name, description, price, image_url)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(f"/admin_market_products/{market_id}")

    return render_template("admin/add_product.html", market_id=market_id)


@app.route("/admin_delete_product/<int:product_id>")
def admin_delete_product(product_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT market_id FROM products WHERE id=%s", (product_id,))
    product = cursor.fetchone()

    if product:
        market_id = product["market_id"]
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
    else:
        market_id = 0

    cursor.close()
    conn.close()

    return redirect(f"/admin_market_products/{market_id}")


@app.route("/admin_add_driver", methods=["GET", "POST"])
def admin_add_driver():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        vehicle_type = request.form["vehicle_type"]
        current_x = request.form["current_x"]
        current_y = request.form["current_y"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, 'driver')",
            (full_name, email, password)
        )

        user_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO drivers (user_id, phone, vehicle_type, current_x, current_y, status)
            VALUES (%s, %s, %s, %s, %s, 'available')
            """,
            (user_id, phone, vehicle_type, current_x, current_y)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/admin_drivers")

    return render_template("admin/add_driver.html")

@app.route("/admin_delete_customer/<int:customer_id>")
def admin_delete_customer(customer_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cart_items WHERE customer_id=%s", (customer_id,))
    cursor.execute("DELETE FROM notifications WHERE user_id=%s", (customer_id,))
    cursor.execute("DELETE FROM support_tickets WHERE customer_id=%s", (customer_id,))
    cursor.execute("DELETE FROM orders WHERE customer_id=%s", (customer_id,))
    cursor.execute("DELETE FROM users WHERE id=%s AND role='customer'", (customer_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/admin_customers")

@app.route("/admin_delete_driver/<int:driver_id>")
def admin_delete_driver(driver_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id FROM drivers WHERE id=%s", (driver_id,))
    driver = cursor.fetchone()

    if driver:
        user_id = driver["user_id"]

        cursor.execute("DELETE FROM drivers WHERE id=%s", (driver_id,))

        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))

        cursor.execute("UPDATE orders SET driver_id=NULL WHERE driver_id=%s", (driver_id,))

        conn.commit()

    cursor.close()
    conn.close()

    return redirect("/admin_drivers")

@app.route("/admin_reply_ticket/<int:ticket_id>", methods=["POST"])
def admin_reply_ticket(ticket_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    reply = request.form["reply"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE support_tickets
        SET admin_reply=%s, reply_at=NOW()
        WHERE id=%s
        """,
        (reply, ticket_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/admin_support")

@app.route("/admin_close_ticket/<int:ticket_id>")
def admin_close_ticket(ticket_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE support_tickets SET status='closed' WHERE id=%s",
        (ticket_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/admin_support")

def market_is_open_by_id(market_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT open_time, close_time, is_active FROM markets WHERE id=%s", (market_id,))
    market = cursor.fetchone()

    cursor.close()
    conn.close()

    if not market or market["is_active"] == 0:
        return False

    return is_market_open(market["open_time"], market["close_time"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)