**************
development
**************

Install python library::
    
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    poetry install

Execute mongodb::

    cd iq-api
    docker-compose -f standalone.docker-compose.yml up -d


Run::

    uvicorn app.main:app --reload
