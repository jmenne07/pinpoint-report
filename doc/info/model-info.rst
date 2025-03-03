Model-Info
==========

Models describe the data-structure of the database.

In this project, there are two main models, which are called **Category** and **Report**.

The report-model contains request, provided by an user.

The reports are grouped by categories.
Furthermore the category also handles access to the reports. This is done by checking if a
user corresponds with a category and only if this is the case,the user gets access to the category and the
reports.

The structure of the database is shown in the following diagram.


.. mermaid::

     erDiagram
        Report{
            string title
            string description
            datetime created_at
            dateimte updated_at
            boolean published
            int state
            email email
            float Latitude
            float longitude
            State state
        }
        Category{
            string name
        }
        Image{
            string file
        }
        User
        Group
        Report }o--|| Category : "belongs to"
        Report || -- o{ Image: "has"
        Category |o--o{Category: "Parent of"
        User }o--o{ Group : "is in"
        User }o--o{ Category: "owns"
        Group }o--o{ Category: "owns"


The :ref:`model classes <Models>` are an abstraction created by django for the database, such that it is 
only needed to alter the code, to change the model in the database. Furthermore with this abstraction 
it is easier to change the database, since every database is handled in the same way.
After each alteration of a model-class the following two scripts have to be run.
.. code:: 
    
    python manage migrations
    python manage migrate 

The first command creates a migration file, while the second one applies the migration to the database.

The following models are used: 

* Category
* Report 

Categories are used to group reports.
Furthermore, categories also serve as a kind of access control, beccause only users who either are directly 
assigned to a category or who are in a group, which is assigned to category (and superuser) are allowed to change
reports belonging to the category.
The permissions are also dependen on the default persmissions of django (add, change, delete, view).
This means, that to access or alter a specific report, the basepermissions and the category must be correct.
