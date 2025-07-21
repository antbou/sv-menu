DC=docker/docker-compose.yml

.PHONY: run run-args build clean shell

run:
	docker-compose -f $(DC) run --rm svmenu

run-args:
	docker-compose -f $(DC) run --rm svmenu $(ARGS)

build:
	docker-compose -f $(DC) build

clean:
	docker-compose -f $(DC) down --rmi all --volumes --remove-orphans

shell:
	docker-compose -f $(DC) run --rm svmenu /bin/bash