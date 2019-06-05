"use strict";

// Global variable for map
var map;
let markers = [];
var icon;
var user_location_icon;
var user_marker;
var user_coords;

// Function to initialize Google Map
function initMap() {
    const init_coords = { lat: 37.782884, lng: -122.418916 };

    map = new google.maps.Map(document.getElementById('map'), {
        center: init_coords,
        zoom: 14
    });

    const infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        user_coords = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        // make user current location marker
        user_marker = new google.maps.Marker({ 
          position: user_coords, 
          map: map, 
          title: "You're Here", 
          icon: user_location_icon 
        });
        // Add marker to markers list
        markers.push(user_marker)
        // Place user current location marker on map
        user_marker.setMap(map);
        // Add info window to user current location marker
        addInfoWindowToUserMarker(user_marker, map)

          infoWindow.setPosition(user_coords);
          infoWindow.setContent('Location found.');
          map.setCenter(user_coords);

        }, function() {
          handleLocationError(true, infoWindow, map.getCenter());
        });
      } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
      }

    // Icon to be used for near bathrooms
    icon = {
      url: '/static/img/poo_emoji.png',
      scaledSize: new google.maps.Size(40, 40)
    };

    user_location_icon = {
      url: 'static/img/rainbow_poo.png',
      scaledSize: new google.maps.Size(40, 40)
    };

}

// Function to get user location and refresh markers
function geolocateUser() {
    const infoWindow = new google.maps.InfoWindow;
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        user_coords = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        // Remove all markers from map
        deleteMarkers();
        // make user current location marker
        user_marker = new google.maps.Marker({ 
          position: user_coords, 
          map: map, 
          title: "You're Here", 
          icon: user_location_icon 
        });
        // Place user current location marker on map
        user_marker.setMap(map);
        // Add info window to user current location marker
        addInfoWindowToUserMarker(user_marker, map)

          infoWindow.setPosition(user_coords);
          infoWindow.setContent('Location found.');
          map.setCenter(user_coords);

        }, function() {
          handleLocationError(true, infoWindow, map.getCenter());
        });
      } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
      }
      return user_coords;
}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}

// Gets text from given route and converts to json
function getNearBathrooms(response) {
    // Grab the inner body text from the response route
    const bathroom_json = response;
    // Loop through bathrooms from response
    for (const bathroom of bathroom_json) {
        console.log(bathroom.name, bathroom.latitude, bathroom.longitude);

        // Make marker for bathroom and set to map
        let position = {}
        position["lat"] = bathroom.latitude;
        position["lng"] = bathroom.longitude;
        const marker = new google.maps.Marker({
            position: position, 
            map: map, 
            title: bathroom.name, 
            icon: icon });
        marker.setMap(map);
        markers.push(marker);
        addInfoWindowToMarker(marker, map);
    }
}

function handleGetBathrooms(evt) {
    evt.preventDefault();
    user_coords = geolocateUser();

    $.get('/get_near_me.json', user_coords, getNearBathrooms);
}

$('#search_near_me').on('click', handleGetBathrooms);


/*
 Helper functions
 */


/**
 Adds a marker with the given icon, position, and title to the given map.

 Parameters
    icon - an object defined using Google's Icon interface
    position - an object with lat, lng properties
    title - a title for the marker
    map - a Map object
 
 Returns Google Maps Marker object
 */
function addMarker(icon, position, title, map) {
  const marker = new google.maps.Marker({ position, map, title, icon });

  return marker;
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  setMapOnAll(null);
  markers = [];
}

// Changes marker position to given latitude and longitude
function changeMarkerPos(latitude, longitude) {
    myLatLng = new google.maps.LatLng(latitude, longitude);
    marker.setPosition(myLatLng);
    map.panTo(myLatLng);
}



/*
 Attaches the given infoWindow to the given marker.
 Also attaches a click event handler to the marker.
 
 When the user clicks on a marker, it closes the previous infoWindow and opens
 the infoWindow with the content for that marker.
 
 Parameters
    infoWindow - an InfoWindow object
    content - a string, the content displayed in the InfoWindow
    marker - a Marker object
    map - a Map object
 */
function addInfoWindowToMarker(marker, map) {
  const content = `<h1>${marker.title}</h1>
      <p>
        <b>Lat:</b> ${marker.position.lat()}</br>
        <b>Lng:</b> ${marker.position.lng()}</br></br>
        <button type="button" id="checkin" onclick="checkIn()">Check In</button>
      </p>
      `;

  const infoWindow = new google.maps.InfoWindow({ 
    content,
    maxWidth: 200
  });

  marker.addListener('click', () => {
    infoWindow.open(map, marker);
  });

}

function checkIn() {
    window.location = '/checkin/37';

}

function addInfoWindowToUserMarker(user_marker, map) {
  const content = `<h1>${user_marker.title}</h1>`;

  const infoWindow = new google.maps.InfoWindow({ 
    content,
    maxWidth: 200
  });

  user_marker.addListener('click', () => {
    infoWindow.open(map, user_marker);
  });
}