API_URL ?= http://localhost:8001
WS_URL ?= ws://localhost:8001
CLIENT_HOME=iq-client
MODULES=${CLIENT_HOME}/node_modules
DIST=${CLIENT_HOME}/dist

include .env

modules:
	@if test -d $(MODULES); \
	then echo 'node_modules already installed..'; \
	else cd iq-client && yarn && echo 'node_modules installed.'; fi

dist: modules
	@if test -d $(DIST); \
	then echo 'dist already exists..'; \
	else cd iq-client && API_URL=$(API_URL) WS_URL=$(WS_URL) yarn build && echo 'dist created.'; fi

clean-dist:
	@if test -d $(DIST); \
	then rm -rf $(DIST); echo 'deleted.'; \
	else echo ''; fi

all: dist
	@docker-compose up -d

clean-all:
	@docker-compose down

flush: clean-dist
	@docker-compose down --rmi local