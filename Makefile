.PHONY: build upload

upload publish: build
	poetry publish

build:
	poetry build

all: build upload