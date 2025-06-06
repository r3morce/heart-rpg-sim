help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  setup       to setup the project"
	@echo "  run         to run the project"
	@echo "  run_debug   to run the project in debug mode"
	@echo "  run_docker  to build and run the project in docker"
	@echo "  test        to run the tests"
	@echo "  test_debug  to run the tests in debug mode"

setup:
	python3 -m venv venv
	pip install -r requirements.txt
	source venv/bin/activate
	@echo API_KEY=fillme > .env
	@echo Created .env file

run:
	python3 main.py

run_debug:
	isort .
	black .
	python3 main.py --debug

run_docker:
	docker-compose build && docker-compose up

test:
	pytest tests -q

test_debug:
	pytest tests -v
