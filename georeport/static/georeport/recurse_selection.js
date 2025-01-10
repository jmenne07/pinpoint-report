function getsubcats(element) {
    const id = element.id;;
    var level = 0;

    if (id != "category")
        level = id;
    console.log(level);
    const rootselect = document.getElementById(id);

    let = url = `category/${rootselect.value}/children`;

    const form = document.getElementById("form");
    const submit = document.getElementById("submit");
    console.log(url);
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP Error: Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            level++;

            let subcats = data["subcategories"];
            if (subcats.length == 0) {
                let oldselect = document.getElementById(level);
                if (oldselect) {
                    form.removeChild(oldselect);
                    oldselect.remove();
                    form.removeChild(submit);
                    form.appendChild(submit);
                }
                return
            }
            let select = document.createElement("select");
            select.id = level;
            select.name = select.id;
            select.value = "";
            select.innerHTML = "Choose a subcategory";
            select.onchange = function () {
                getsubcats(this);
            }

            var option = document.createElement("option");
            option.value = "";
            option.innerHTML = "Subcategory";
            option.disabled = true;
            option.selected = true;
            select.appendChild(option);


            console.log(subcats);
            for (var cat of subcats) {
                option = document.createElement("option");
                option.value = cat.id;
                option.innerText = cat.name;
                select.appendChild(option);
            }

            form.removeChild(submit);
            form.appendChild(select);
            form.appendChild(submit);

            console.log(level);
        });

}

/*TODO Better ids for selection */
/*TODO Labels for selection*/
/*TODO tidy up*/


