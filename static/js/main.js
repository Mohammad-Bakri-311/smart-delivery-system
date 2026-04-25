function getMyLocation() {
    if (!navigator.geolocation) {
        alert("Your browser does not support location.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            const xInput = document.getElementById("pickup_x");
            const yInput = document.getElementById("pickup_y");
            const addressInput = document.getElementById("pickup_address");

            if (xInput) xInput.value = lat;
            if (yInput) yInput.value = lng;
            if (addressInput) addressInput.value = "My Current Location";
        },
        function() {
            alert("Please allow location permission.");
        }
    );
}