Create the Virtual Environment on Python 3.8 version

#install all the requirements

pip install -r requirements.txt

#set the rabbitmmq-server locally

sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl status rabbitmq-server
#then run this command in project directory
celery -A bookstore_project worker -l info

#run the postgres locally from docker

sudo docker pull postgres
docker run -d \
  --name bookstore_db \
  -e POSTGRES_USER=bookstoreuser \
  -e POSTGRES_PASSWORD=bookstorepassword \
  -e POSTGRES_DB=bookstoredb \
  -e POSTGRES_HOST_AUTH_METHOD=md5 \
  -v /path/to/local/data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres

run the project
python manage.py runserver

#for running the test cases
python manage.py test bookstore.tests


#Docker
run the command docker-compose up

