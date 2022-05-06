# #!/bin/bash

echo 'This program will help you to create FastAPI project. Please enter project name.'
read project_name
db_name="${project_name}_db"

cp -a site/. .

sed -i "s/project_name/$project_name/" docker-compose.yml
sed -i "s/db_name/$db_name/" docker-compose.yml

cp .env.example .env
sed -i "s/project_name/$project_name/" .env
sed -i "s/db_name/$db_name/" .env

port=8000
echo 'Please enter project port. Default is 8000.'
read port
sed -i "s/port:port/$port:$port/" docker-compose.yml
sed -i "s/port/$port/" dockerfile
sed -i "s/port/$port/" .env

# Для работы без докера
cp .env src/.env

# Удалить ненужное
rm -r site
rm setup.sh



