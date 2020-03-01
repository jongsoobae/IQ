## IQ-API

# install
~~~
# virtualenv 로 해당 프로젝트 venv가 만들어져있음을 전제한다.
$ pwd
IQ/iq-api/iq_api
$ pip install -r ./iq-api/iq_api.egg-info/requires.txt
~~~

### run server 
~~~
$ pwd
IQ/iq-api/iq_api
$ uvicorn main:app --reload
~~~

### api docuemnt
http://127.0.0.1:8000/docs
