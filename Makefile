
checklist: format lint typehint test

format:
	black *.py

typehint:
	mypy *.py

test:
	pytest tests/

lint:
	pylint *.py


.PHONY: format typehint tet lint checklist
