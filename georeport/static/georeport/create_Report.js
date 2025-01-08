/* 
 * Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
 * GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
*/
var lat_input = document.getElementById("id_latitude");
var lng_input = document.getElementById("id_longitude");
let marker = L.marker();


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

    lat_input.value = e.latlng.lat.toFixed(6);
    lng_input.value = e.latlng.lng.toFixed(6);

}

map.on("click", onMapClick);

