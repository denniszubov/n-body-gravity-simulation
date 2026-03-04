.PHONY: build run test clean

build:
	pip install -e ".[app,dev]"

run:
	streamlit run app/app.py

test:
	pytest tests/ -v

clean:
	rm -rf build/ dist/ *.egg-info/ _skbuild/
