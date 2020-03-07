CLIENT_HOME=iq-client
MODULES=${CLIENT_HOME}/node_modules
DIST=${CLIENT_HOME}/dist

dist:
	@if test -d $(DIST); \
	then echo 'dist already exists..'; \
	else cd iq-client && yarn && yarn build && echo 'dist created.'; fi

clean-dist:
	@if test -d $(DIST); \
	then rm -rf $(DIST); echo 'deleted.'; \
	else echo ''; fi

all: dist
	@docker-compose up -d

clean:
	@docker-compose down

clean-all: clean-dist
	@docker-compose down

flush: clean-dist
	@docker-compose down --rmi local
