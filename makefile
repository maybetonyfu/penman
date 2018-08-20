.PHONY: build
build:
	@echo "Build pex file"
	pex . -c main.py -o build/penman.pex