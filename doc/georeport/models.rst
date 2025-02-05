Models
======

.. todo::

    Split into 2 files. 1 to read and one for the autodoc

The models represent the structure in the datebase as such, that each model 
is a table in the database. 
The translation from the *models.py* file to the specifc tables is done by
django with the help of migrations.

After each alteration of a model-class the following two scripts have to be run.
.. code:: 
    
    python manage migrations
    python manage migrate 

The first command creates a migration file, while the second one applies the migration to the database.

The following models are used: 

* Category
* Report 

Categories are used to group reports and assing the corresponding staff. This is done by preventing access to users,
which have not authority about the category

.. automodule:: georeport.models
   :members:
   :undoc-members:

