#!/bin/sh
#make virtual_environment
echo y | conda create -n docker_train python=3.9 && conda activate docker_train
#install dependency_packages
pip install -r requirements.txt
#make_database
python manage.py migrate
#upload_dependency_data
python db_upload/db.py
#find_server_IPAddress
echo "your_server_IP_address"
echo  | ipconfig getifaddr en0
#runserver_finally
python manage.py runserver 0:8000

