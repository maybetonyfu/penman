.PHONY: build
build-image:
	@echo "Build docker image"
	docker build --tag=builder $$(pwd)

build-exe: build-image
	@echo "Build exe file from container"
	docker run --name=penman builder

build: build-exe
	@echo "Copy exe from container"
	docker cp penman:/root/dist/main penman
	docker rm -vf penman

