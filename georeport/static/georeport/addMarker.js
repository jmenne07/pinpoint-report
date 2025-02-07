/*
 * Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
 * GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
*/

/*
 * A simple script, which extracts the latitude and longitude value from http
 * and adds a marker at the correspoing location on the map.
*/

var marker = L.marker()

var lat = document.getElementById("p-lat").dataset.lat;
var lng = documetn.getElementById("p-lng").dataset.lng;

marker.setLatLng([lat, lng]).addTo(map);
