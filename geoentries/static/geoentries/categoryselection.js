/*
 * Copyright 2026 Jörn Menne
 * Licensed under the Apache License, Version 2.0
 * See NOTICE file for details.
 */

var maxlevel = 0

function getsubcategories(element) {

    const id = element.id;
    var level;
    if (id == "id_category")
        level = 0;
    else
        level = id;

    console.log(level);

    //Get surrunding elements
    const form = document.getElementById("form");
    const submit = document.getElementById("submit");
    const catsel = document.getElementById("catsel");

    let url = `/open311/v2/services/${element.value}/subcategories/`;
    console.log(url);

    fetch(url)
        .then(response => {

            if (!response.ok)
                throw new Error(`HTTP Error: Status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log(data);
            let subcats = data["subcategories"];
            level++;

            // Remove all equal or  higher selects defineProperties
            if (maxlevel >= level) {
                for (let i = level; i <= maxlevel; i++) {
                    let sel = document.getElementById(i);
                    if (sel) sel.remove();
                }
            }
            if (subcats.length == 0) {
                element.name = "category";
                maxlevel = level - 1;
            }
            else {

                //Create a new selection element
                let select = document.createElement("select");
                select.id = level;
                select.name = select.id;
                select.value = "";
                select.innerHTML = "Wählen Sie eine Unterkategorie";
                select.onchange = function () {
                    getsubcategories(this);
                }
                select.name = "category";
                select.required = true;

                // Create the new options 
                var option = document.createElement("option");
                option.value = "";
                option.innerHTML = "Unterkategorie";
                option.disabled = true;
                option.selected = true;
                select.appendChild(option);

                for (var cat of subcats) {
                    option = document.createElement("option")
                    option.value = cat.name;
                    option.innerHTML = cat.name;
                    select.appendChild(option);
                }

                element.name = "root";
                catsel.appendChild(select);
                maxlevel = level;
            }
            //Reappend submit
            // form.appendChild(submit);
            console.log(maxlevel);
        })
}
