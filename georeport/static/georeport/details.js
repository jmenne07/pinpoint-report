var marker = L.marker();

var lat = document.getElementById("p-lat").dataset.lat;
var lng = document.getElementById("p-lng").dataset.lng;

marker.setLatLng([lat, lng])
    .addTo(map);
