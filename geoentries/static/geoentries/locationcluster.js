const markers = L.markerClusterGroup();

fetch(window.APP_CONFIG.urls.locations)
    .then(response => response.json())
    .then(data => {
        data.forEach(location => {
            marker = L.marker([location.latitude, location.longitude]); 
            markers.addLayer(marker);
        });
        map.addLayer(markers);
    })

