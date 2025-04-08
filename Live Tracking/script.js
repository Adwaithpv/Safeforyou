// ✅ Firebase Configuration
// Replace this config with your Firebase project's credentials
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

// ✅ Create a reference to the Realtime Database
const database = firebase.database();

// ✅ Set a unique identifier for the user (change this per user/session)
const userID = "user_12345";

// ✅ Make initMap global so Google Maps API can call it
window.initMap = function () {
    console.log("✅ Google Maps Loaded & `initMap` Called!");

    // ✅ Initialize Google Map centered at (0, 0)
    window.map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: { lat: 0, lng: 0 } // Default center
    });

    // ✅ Create a Marker to show user's location
    window.marker = new google.maps.Marker({
        position: { lat: 0, lng: 0 },
        map: window.map
    });

    // ✅ Listen for real-time location updates from Firebase
    database.ref("locations/" + userID).on("value", (snapshot) => {
        const data = snapshot.val();
        if (data) {
            const position = { lat: data.lat, lng: data.lng };
            // Update marker position and map center
            window.marker.setPosition(position);
            window.map.setCenter(position);
            console.log(`📍 Map updated: ${data.lat}, ${data.lng}`);
        } else {
            console.warn("⚠️ No location data available.");
        }
    });
};

// ✅ Function to continuously update location to Firebase
function updateLocation() {
    if (!navigator.geolocation) {
        console.error("❌ Geolocation is not supported.");
        return;
    }

    // ✅ Start watching user's location
    navigator.geolocation.watchPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            const timestamp = Date.now();

            // ✅ Update Firebase Realtime Database with current location
            database.ref("locations/" + userID).set({ lat, lng, timestamp });
            console.log(`📍 Updated: ${lat}, ${lng}`);
        },
        (error) => {
            console.error("❌ Location Error:", error);
            alert("Location access denied. Please enable GPS.");
        },
        {
            enableHighAccuracy: true, // Use GPS
            maximumAge: 0             // No caching
        }
    );
}

// ✅ Automatically start location tracking when the page loads
document.addEventListener("DOMContentLoaded", updateLocation);
