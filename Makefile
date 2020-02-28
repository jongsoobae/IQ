API_URL ?= http://localhost
DIST=iq-client/dist


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
