

/*
 * Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
 * GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
*/

/*
 * Function which adds a new category-selection field, if the current category has at least one subcategory.
 * If this is not the case, and the former selection had a subcategory, the selection fields for 
 * subcategories are removed.
*/

var maxlevel = 0

function getsubcats(element) {

  // Set the current level to know which selections have to be removed (if any)
  const id = element.id;
  var level;
  if (id == "category")
    level = 0;
  else
    level = id;
  console.log(level);

  // Get surrunding elements
  const form = document.getElementById("form");
  const submit = document.getElementById("submit");

  //create a url to fetch the children
  let url = `category/${element.value}/children`;
  console.log(url);
  fetch(url)
    // Check if the response is correct
    .then(response => {
      if (!response.ok)
        throw new Error("HTTP Error: Status: ${response.status}");
      return response.json();
    })
    //Handle the json-Data
    .then(data => {
      console.log(data);
      let subcats = data["categories"];
      level++;
      //Remove submit temporarly to set the correct position
      form.removeChild(submit);

      // Remove all equal or  higher selects defineProperties
      if (maxlevel >= level) {
        for (let i = level; i <= maxlevel; i++) {
          sel = document.getElementById(i);
          sel.remove();
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
        select.innerHTML = "Choose a subcategory";
        select.onchange = function () {
          getsubcats(this);
        }
        select.name = "category";

        // Create the new options 
        var option = document.createElement("option");
        option.value = "";
        option.innerHTML = "Subcategory";
        option.disabled = true;
        option.selected = true;
        select.appendChild(option);

        for (var cat of subcats) {
          option = document.createElement("option")
          option.value = cat.id;
          option.innerHTML = cat.name;
          select.appendChild(option);
        }

        element.name = "root";
        form.appendChild(select);
        maxlevel = level;
      }
      //Reappend submit
      form.appendChild(submit);
      console.log(maxlevel);
    })
}
