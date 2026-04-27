/*
 * Copyright 2026 Jörn Menne
 * Licensed under the Apache License, Version 2.0
 * See NOTICE file for details.
 */
/*
 * A small script, which extracts the coordinates given by leaflet
 * and inserts them into the correct fields. It also works the other way.
 */

// Specify all needed elements
var lat_element = document.getElementById("latitude") || document.getElementById("id_latitude");
var lng_element = document.getElementById("longitude") || document.getElementById("id_longitude");
var nomi = document.getElementById("nomi-form")
var adress_element = document.getElementById("adresse");
var ad_element = document.getElementById("id_formated_adress")
let marker = L.marker();


map.locate({ setView: true, maxZoom: 18, enableHighAccuracy: true });


function onLocationFound(e) {
    marker.setLatLng(e.latlng).addTo(map);

}

map.on('locationfound', onLocationFound);




// Add change listener to the input-elements
lat_element.addEventListener("change", () => {
    marker.setLatLng([lat_element.value, lng_element.value])
        .addTo(map);
});
lng_element.addEventListener("change", () => {
    marker.setLatLng([lat_element.value, lng_element.value])
        .addTo(map);
});


/*
 * Read event-data if clicked on the map to get the geocoordinates.
 * The values are then capped to 6 decimals to get a precision of ~10cm.
 * Which is enoug for this usecase.
 * The precirsion is accorcding to https://en.wikipedia.org/wiki/Decimal_degrees
 */
function onMapClick(e, decimal_precision = 6) {
    marker.setLatLng(e.latlng).addTo(map);

    lat_element.value = e.latlng.lat.toFixed(decimal_precision);
    lng_element.value = e.latlng.lng.toFixed(decimal_precision);

    reverseGeocode(e.latlng.lat, e.latlng.lng);

}

map.on("click", onMapClick);

nomi.addEventListener("submit", async (e) => {
    //prevent pagereload 
    e.preventDefault();
    e.stopPropagation();

    const formdata = new FormData(e.target);
    var value = formdata.values().next().value;
    value = value.replaceAll(" ", "+");

    url = "https://nominatim.openstreetmap.org/search?q=";
    url = url.concat(value);
    url = url.concat("&format=jsonv2");
    console.log(url);
    // fetch("https://nominatim.openstreetmap.org/search?${result}")
    fetch(url)
        .then(res => res.json())
        .then(json => {
            console.log(json[0]);
            let position = [json[0].lat, json[0].lon];
            marker.setLatLng(position);
            marker.addTo(map)
            // L.marker(position).addTo(markerLayer);
            adress_element.value = json[0].display_name;
            lat_element.value = json[0].lat;
            lng_element.value = json[0].lon;

            map.setView(position, map.getZoom());
        });

});

function reverseGeocode(lat, lon) {
    var url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`;
    fetch(url)
        .then(res => res.json())
        .then(json => {
            adress_element.value = json.display_name;
            ad_element.value = adress_element.value;
        });
}



