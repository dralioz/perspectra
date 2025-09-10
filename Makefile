TAG=1.0.0
local-install:
	pip install -e .

clean:
	rm -rf dist/ build/ *.egg-info

docker-build:
	docker build -t perspectra-api:$(TAG) .

docker push:
	docker push perspectra-api:$(TAG)

format:
	isort . src tests
	black -l 120 src tests

check-format:
	isort . --check
	black -l 120 --check src tests

lint:
	flake8 src tests

build-debug:
	docker-compose -f docker-compose.debug.yml up --build -d perspectra-api

up-debug: down-debug 
	docker-compose --env-file=.env.dev -f docker-compose.debug.yml up --remove-orphans --detach --force-recreate

down-debug:
	docker-compose -f docker-compose.debug.yml down

tail-logs:
	docker-compose -f docker-compose.debug.yml logs -f

restart-debug: down-debug up-debug

start-debug: down-debug build-debug up-debug

run-unit-tests:
	coverage erase
	coverage run -m pytest tests/unit
	coverage xml

run-integration-tests:
	pytest --cov=. tests/integration

run-all-tests: 
	pytest --cov=. tests