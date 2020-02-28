API_URL ?= http://localhost
DIST=iq-client/dist

db:
	@cd iq-api && docker-compose -f standalone.docker-compose.yml up -d
clean-db:
	@cd iq-api && docker-compose -f standalone.docker-compose.yml down

dist:
	@if test -d $(DIST); \
	then echo 'dist already exists..'; \
	else cd iq-client && API_URL=$(API_URL) yarn build && echo 'dist created.'; fi

clean-dist:
	@if test -d $(DIST); \
	then rm -rf $(DIST); echo 'deleted.'; \
	else echo ''; fi

all: dist
	@docker-compose up -d

clean-all:
	@docker-compose down
