# Use an official Python runtime as a parent image
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "bookstore_project.wsgi:application", "--bind", "0.0.0.0:8000"]
