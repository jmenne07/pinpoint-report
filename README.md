# Pinpoint-Report

Pinpoint-Report is a web-app, which allows to create reports for locations.
This is done by clicking on a map to specify the location and afterwards
fill some fields to provide information.

## Deployment

Before deploying the app, it is advised to change the following settings ins pinpoint-report.settings.py:

Settings | Reason
---------|------
SECRET_KEY | Key to secure the application
DEBUG | Sets the app to debug mode or to production mode
ALLOWED_HOSTS | List with hosts, on which the app is allowed to run
DATABASES | Should be set to the used databases. The default database is a sqlite3 database in the filesystem
INTERNAL_IPS | A list of ips, which can share sensitive information. (Currently on needed for debug_toolbar)
SEND_MAIL | Determines if mails should be send or not
EMAIL_HOST | Host of the used mailclient
EMAIL_PORT | Port of the used mailclient
DEFAULT_FROM_EMAIL | Mailaddress from which mails will be send (if SEND_MAIL is True)
KEY |  A key used to encrypt and decrypt close-links. In production it is advised to use a fixed key, so that closelinks still work after a restart
MINIO_ENDPOINT | Ths host and port of the minio to store images
MINIO_ACCESS_KEY | The username of the minio-instance
MINIO_SECRET_KEY | The password of the minio-instance

To run the web-app with docker or podman just run **docker compose up** or **podman compose up**.
In this case the pinpoint-report-container has a sqlite3 db in the filesystem.

To install the web-app locally The following things have to be run:

Setting up the environment:

``` sh
python -m venv .venv 
python -m pip install -r rquirements.txt 
python manage.py migrate 
```

In this case the migrate-command initialised the database and creates the sqlite3-file.

The server can than be started with

```
python manage.py runserver
```

In both cases, it is recommended to create a super user after starting the server/app.
To do this the following command is needed:

```sh
python manage.py createsuperuser
```

In the case of a local installation this can also be done before starting the server.
If the server is run via docker, it is needed to run the command in the pinpoint-container.
