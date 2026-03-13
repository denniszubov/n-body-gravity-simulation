.PHONY: build run test clean

build:
	pip install -e ".[app,dev]"

run:
	uvicorn app.main:app --reload

test:
	pytest tests/ -v

clean:
	rm -rf build/ dist/ *.egg-info/ _skbuild/
