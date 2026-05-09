# Smart Delivery System 🚚

A full-stack smart delivery web application inspired by real-world platforms like Uber, Glovo, and Wolt.
The system allows customers to create delivery orders, automatically assigns the nearest driver, and provides dashboards for customers, drivers, and administrators.

---

##  Live Demo

🔗 https://smart-delivery-system.onrender.com

---

##  Demo Account (Customer)

Use the following account to test the system:

Email: [john@gmail.com](mailto:john@gmail.com)
Password: 1234
Role: Customer

> This is a public demo. Data may change as users interact with the system.

---

##  Admin Access

Admin features are **not publicly shared for security reasons**.

✔ Admin pages and functionalities are demonstrated in the screenshots
✔ Full admin access is available upon request

---

##  Features

* User authentication (login & register)
* Role-based system (Customer, Driver, Admin)
* Market browsing and product ordering
* Shopping cart system
* Custom delivery requests
* Google Maps integration (location selection)
* Google Places API (address search)
* Automatic nearest driver assignment
* Order tracking system
* Payment simulation
* Notifications system
* Support ticket system
* Driver dashboard with delivery management
* Admin dashboard for full system control

---

##  Core Logic

* Distance-based algorithm to assign the nearest available driver
* Dynamic driver availability management
* Full order lifecycle:

  * Created
  * Assigned
  * Picked Up
  * Delivered
* Role-based access control

---

##  Technologies Used

* Python (Flask)
* MySQL (Railway database)
* HTML / CSS / JavaScript
* Jinja2 Templates
* Google Maps API
* Google Places API
* Render (Deployment)
* GitHub

---

##  Database

The system uses a MySQL relational database with multiple tables such as:

* users
* drivers
* orders
* products
* markets
* cart_items
* tracking
* notifications
* support tickets

 SQL file is included:

```text
database/smart_delivery.sql
```

---

##  Screenshots

All screenshots are available in:

```text
static/images/screenshots/
```

Includes:

* Customer pages
* Driver dashboard
* Admin pages
* Order system
* Google Maps integration
* Database table designer (structure)

---

##  Run Locally

1. Clone the project:

```bash
git clone https://github.com/YOUR_USERNAME/smart-delivery-system.git
cd smart-delivery-system
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Create `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

4. Run the app:

```bash
python app.py
```

5. Open:

```text
http://localhost:5000
```

---

##  Security Notes

* `.env` file is not included in the repository
* API keys are stored using environment variables
* Database credentials are hidden
* Google API key is restricted by domain
* Passwords are stored as plain text for demo purposes only (not production-ready)

---

##  Future Improvements

* Add password hashing (bcrypt)
* Add real payment integration
* Add real-time updates (WebSockets)
* Improve driver actions and workflow
* Add route optimization
* Build mobile version

---

##  Author

Mohammad Bakri

---

##  Project Status

 Actively under development
