.PHONY: test lint tox coverage

test:
	py.test -sv jenkinsapi_tests

lint:
	pycodestyle
	pylint jenkinsapi/*.py

tox:
	tox

coverage:
	py.test -sv --cov=jenkinsapi --cov-report=term-missing --cov-report=xml jenkinsapi_tests
