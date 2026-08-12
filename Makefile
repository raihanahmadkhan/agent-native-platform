.PHONY: install run test

install:
	cd service && pip install -r requirements.txt

run:
	cd service && uvicorn app.main:app --reload

test:
	cd service && PYTHONPATH=. pytest -q
