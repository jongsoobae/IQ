**************
How to setup
**************

=============
Prerequisites
=============

should installed node and yarn

vi .env::

    MONGO_INITDB_ROOT_USERNAME=root
    MONGO_INITDB_ROOT_PASSWORD=root
    MONGO_HOST=mongo
    MONGO_PORT=27017

    WEB_SCHEME=http
    WEB_HOST=iq.dhk.co.kr
    WEB_PORT=80

    API_SCHEME=http
    WS_SCHEME=ws
    API_HOST=iq.dhk.co.kr
    API_PORT=8003


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
