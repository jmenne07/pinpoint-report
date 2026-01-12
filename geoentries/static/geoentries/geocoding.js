var nomi = document.getElementById("nomi-form").addEventListener("submit", async(e) =>{
    //prevent Pagereload
    e.preventDefault();
    e.stopPropagation();

    const formdata = new FormData(e.target);
    var value = formdata.values().next().value;
    value = value.replaceAll(" ", "+");

    url = "https://nominatim.openstreetmap.org/search?q=";
    url = url.concat(value);
    url = url.concat("&format=jsonv2");

    console.log("Get data for " + value);

    fetch(url))
        .then(res => res.json())
        .then(json => {
            let position = [json[0].lat, json[0].lon];
            marker.setLatLng(position);
            marker.addTo(map);

            map.setView(position, map.getZoom());
        });

});
