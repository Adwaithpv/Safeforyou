// ✅ Firebase Configuration
const firebaseConfig = {
    apiKey: "AIzaSyBxhcL4o6U6AXkPGyVpoqhlCaCQjbLW7ic",
    authDomain: "live-location-2524d.firebaseapp.com",
    databaseURL: "https://live-location-2524d-default-rtdb.firebaseio.com",
    projectId: "live-location-2524d",
    storageBucket: "live-location-2524d.appspot.com",
    messagingSenderId: "973654631560",
    appId: "1:973654631560:web:55620264e4385225fb6b3d",
    measurementId: "G-B1FRFDETVT"
};

// ✅ Initialize Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();
const userID = "user_12345"; // Change per user

// ✅ Ensure `initMap` is Global (i.e., on `window`)
window.initMap = function () {
    console.log("✅ Google Maps Loaded & `initMap` Called!");

    // ✅ Create the Map
    window.map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: { lat: 0, lng: 0 }
    });

    // ✅ Add a Marker
    window.marker = new google.maps.Marker({
        position: { lat: 0, lng: 0 },
        map: window.map
    });

    // ✅ Firebase Real-time Updates
    database.ref("locations/" + userID).on("value", (snapshot) => {
        const data = snapshot.val();
        if (data) {
            const position = { lat: data.lat, lng: data.lng };
            window.marker.setPosition(position);
            window.map.setCenter(position);
            console.log(`📍 Map updated: ${data.lat}, ${data.lng}`);
        } else {
            console.warn("⚠️ No location data available.");
        }
    });
};

// ✅ Update Location Function
function updateLocation() {
    if (!navigator.geolocation) {
        console.error("❌ Geolocation is not supported.");
        return;
    }

    navigator.geolocation.watchPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            const timestamp = Date.now();

            database.ref("locations/" + userID).set({ lat, lng, timestamp });
            console.log(`📍 Updated: ${lat}, ${lng}`);
        },
        (error) => {
            console.error("❌ Location Error:", error);
            alert("Location access denied. Please enable GPS.");
        },
        { enableHighAccuracy: true, maximumAge: 0 }
    );
}

// ✅ Start tracking user location
document.addEventListener("DOMContentLoaded", updateLocation);
