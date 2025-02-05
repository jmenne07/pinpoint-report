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
            datetime creation_time
            dateimte updated_at
            boolean published
            int state
            email email
        }
        Category{
            string name
        }
        Location{
            float Latitude
            float Longitude
        }
        Image
        User
        Group
        Report }o--|| Category : "belongs to"
        Report }| -- || Location: "is at"
        Report || -- o{ Image: "has"
        Category |o--o{Category: "Parent of"
        User }o--o{ Group : "is in"
        User }o--o{ Category: "owns"
        Group }o--o{ Category: "owns"


