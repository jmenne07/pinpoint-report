/*
 * Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
 * GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
*/
/*
 * A small script, which extracts the coordinates given by leaflet
 * and inserts them into the correct fields. It also works the other way.
 */

// Specify all needed elements
var lat_element = document.getElementById("latitude");
var lng_element = document.getElementById("longitude");
let marker = L.marker();


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

}

map.on("click", onMapClick);
