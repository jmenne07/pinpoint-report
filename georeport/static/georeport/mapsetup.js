/*
 * Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
 * GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
*/
// Center the map-view on Paderborn and use openstreetmap as a mapservice

// Define the map and set the tilelayer
var map = L.map("map").setView([51.7173, 8.753557], 15);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>"
}).addTo(map);
