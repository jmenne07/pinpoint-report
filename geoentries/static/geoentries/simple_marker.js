const marker = L.marker();

const lat = window.APP_CONFIG.location.lat.replace(",", ".");
const lng = window.APP_CONFIG.location.lng.replace(",", ".");

marker.setLatLng([lat, lng]).addTo(map);
map.setView([lat, lng], map.getZoom());
