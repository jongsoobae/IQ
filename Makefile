CLIENT_HOME=iq-client
MODULES=${CLIENT_HOME}/node_modules
DIST=${CLIENT_HOME}/dist

modules:
	@if test -d $(MODULES); \
	then echo 'node_modules already installed..'; \
	else cd iq-client && yarn && echo 'node_modules installed.'; fi

dist: modules
	@if test -d $(DIST); \
	then echo 'dist already exists..'; \
	else cd iq-client && yarn build && echo 'dist created.'; fi

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
