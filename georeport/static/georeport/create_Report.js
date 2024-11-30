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

