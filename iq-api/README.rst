**************
how to setup
**************

Install python library::
    
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    poetry install


vi docker/.env::

    MONGO_ROOT_USER=root
    MONGO_ROOT_PASSWORD=root
    MONGO_USER=user
    MONGO_PASSWORD=password
    MONGO_PORT=27017

Execute mongodb::

    cd docker
    docker-compose up -d


Run::

    cd iq_api
    uvicorn main:app --reload
