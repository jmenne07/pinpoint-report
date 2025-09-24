// Copyright 2025 Jörn Menne
// Licensed under the Apache License, Version 2.0
// See NOTICE file for details.

// Define the map and set the tilelayer
var map = L.map("map").setView([51.7173, 8.753557], 15);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>"
}).addTo(map);
