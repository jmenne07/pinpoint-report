
FROM python:3 

WORKDIR /app 

COPY pyproject.toml /app/

RUN pip install --upgrade pip && pip install -e . --no-cache  
RUN apt-get update && apt-get install -y gettext \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
RUN python manage.py compilemessages
RUN python manage.py collectstatic --noinput
CMD ["uvicorn" , "openpinpoint.asgi:application", "--host","0.0.0.0", "--port" , "8000"]
