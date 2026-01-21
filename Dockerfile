
FROM python:3 

WORKDIR /app 

COPY pyproject.toml /app/

RUN pip install --upgrade pip && pip install -e . --no-cache  
RUN pip install uvicorn gunicorn
COPY . /app/
RUN python manage.py collectstatic --noinput
#CMD ["python", "manage.py", "runserver"]
CMD ["uvicorn" , "openpinpoint.asgi:application", "--host","0.0.0.0", "--port" , "8000"]
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "openpinpoint.wsgi:application"]
