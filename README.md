docker-compose up --build 
    
docker-compose run --service-ports --rm app sh -c "python3 manage.py runserver 0.0.0.0:8000"