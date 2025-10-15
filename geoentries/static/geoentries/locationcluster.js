const markers = L.markerClusterGroup();

fetch("http://localhost:8000/geoentries/locations")
    .then(response => response.json())
    .then(data => {
        data.forEach(location => {
            marker = L.marker([location.latitude, location.longitude]); 
            markers.addLayer(marker);
        });
        map.addLayer(markers);
    })

