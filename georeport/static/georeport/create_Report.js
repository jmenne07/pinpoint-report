/* 
 * Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
 * GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
*/
var lat_input = document.getElementById("latitude");
var lng_input = document.getElementById("longitude");
let marker = L.marker();

/* 
 * set to 6 decimals points to get a precision of around 10cm 
 * according to https://en.wikipedia.org/wiki/Decimal_degrees
*/
const precision = 6


lat_input.addEventListener("change", () => {
  marker.setLatLng([lat_input.value, lng_input.value])
  i.addTo(map);

});
lng_input.addEventListener("change", () => {
  marker.setLatLng([lat_input.value, lng_input.value])
    .addTo(map);

});

function onMapClick(e) {
  marker.setLatLng(e.latlng)
    .addTo(map);

  lat_input.value = e.latlng.lat.toFixed(precision);
  lng_input.value = e.latlng.lng.toFixed(precision);
}

map.on("click", onMapClick);

