"use strict";

// Function to initialize Google Map

function initMap() {
    const init_coords = { lat: 37.782884, lng: -122.418916 }

    const map = new google.maps.Map(document.getElementById('map'), {
        center: init_coords,
        zoom: 14
    });

    const infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        const user_coords = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        // Make user current location icon
        const user_location_icon = {
          url: 'static/img/rainbow_poo.png',
          scaledSize: new google.maps.Size(40, 40)
        };
        // make user current location marker
        const user_marker = new google.maps.Marker({ 
          position: user_coords, 
          map: map, 
          title: "You're Here", 
          icon: user_location_icon 
        });
        // Place user current location marker on map
        user_marker.setMap(map);
        // Add info window to user current location marker
        addInfoWindowToMarker(user_marker, map)

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



    const user_location_icon = {
      url: 'static/img/rainbow_poo.png',
      scaledSize: new google.maps.Size(40, 40)
    };

    const icon = {
      url: '/static/img/poo_emoji.png',
      scaledSize: new google.maps.Size(40, 40)
    };

}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}

function handleGetBathrooms(evt) {
    evt.preventDefault();

    $.get('/get_near_me.json', getNearBathrooms);
}

$('#search_near_me').on('click', handleGetBathrooms);
    // const locations = [
    //     {
    //         name: "Quizno's",
    //         coords: { lat: 37.7872185, lng: -122.4104286 }
    //     },
    //     {
    //         name: "Academy of Art University",
    //         coords: { lat: 37.789732 , lng: -122.408567 }
    //     },
    //   ];

    // Loop over locations to make markers for each location
    // const markers = locations.map(location => {
    //     return addMarker(icon, location.coords, location.name, map);
    // });

    // Loop over markers to attach click handlers
    // markers.forEach(marker => {
    //     addInfoWindowToMarker(marker, map)
    // })





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

// Changes marker position to given latitude and longitude
function changeMarkerPos(latitude, longitude) {
    myLatLng = new google.maps.LatLng(latitude, longitude)
    marker.setPosition(myLatLng);
    map.panTo(myLatLng);
}

// Gets text from given route and converts to json
function getNearBathrooms(response) {
    // Grab the inner body text from the response route
    const bathroom_json = JSON.parse(response);
    for (const bathroom of bathroom_json) {
        console.log(bathroom.name, bathroom.latitude, bathroom.longitude);
    }
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
        <b>Lng:</b> ${marker.position.lng()}</br>
      `;

  const infoWindow = new google.maps.InfoWindow({ 
    content,
    maxWidth: 200
  });

  marker.addListener('click', () => {
    infoWindow.open(map, marker);
  });
}


