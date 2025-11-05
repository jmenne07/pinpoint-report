
FROM python:3 

WORKDIR /app 

COPY pyproject.toml /app/

RUN pip install --upgrade pip && pip install -e . --no-cache  

COPY . /app/
#RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
