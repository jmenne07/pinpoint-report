# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
import json
from .models import Category
import os

# TODO: User and groups are currently not exported
# This has to be added to work correctly.


def write_categories_to_file(path="cat.json"):
    """
    Creates a json file, which contains all
    necessary information to repopulate the database from scratch
    with the categories.

    Arguments:
        path: The path to the json file
    """
    categories = Category.objects.all()  # type:ignore

    data = []
    for cat in categories:
        catData = {}
        catData["name"] = cat.name
        catData["parent"] = cat.parent.name if cat.parent else ""

        data.append(catData)

    jsondata = json.dumps(data, indent=4)
    with open(path, "w") as file:
        file.write(jsondata)


def populateCategories(path="cat.json"):
    """
    populates a database with categories provided by a json-file.
    It works best, if the json was created by the function write_categories_to_file.

    Arguments:
        path: The path to the json-file
    """

    if not os.path.exists(path):
        print("File not found")
        return
    with open(path, "r") as file:
        data = json.load(file)
        for x in data:
            cat = Category(name=x["name"])
            if x["parent"] != "":
                cat.parent = Category.objects.filter(name=x["parent"]).first()  # type: ignore Attribute object is not known
            cat.save()
