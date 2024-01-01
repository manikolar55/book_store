# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "bookstore_project.wsgi:application", "--bind", "0.0.0.0:8000"]
