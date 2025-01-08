/* 
 * Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
 * GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
*/
var marker = L.marker();

var lat = document.getElementById("p-lat").dataset.lat;
var lng = document.getElementById("p-lng").dataset.lng;

marker.setLatLng([lat, lng])
    .addTo(map);
