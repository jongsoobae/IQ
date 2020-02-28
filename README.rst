**************
How to setup
**************

=========
Prerequisites
=========

vi  .env::

    MONGO_INITDB_ROOT_USERNAME=root
    MONGO_INITDB_ROOT_PASSWORD=root
    MONGO_HOST=mongo
    MONGO_PORT=27017
    CORS_ALLOWED=http://127.0.0.1:3000,http://localhost:3000,http://127.0.0.1:8002

========
Develop
========
`here <iq-api/README.rst>`_

==========
Deployment
==========
run at once::
    make all

Others::
    make dist
    make clean-dist
    make all
    make clean-all
