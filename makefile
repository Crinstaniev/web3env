test:
	pytest -s -v 

flask:
	python3 run_ui.py

.PHONY: build-x86 build-arm run clean push-x86 push-arm

IMAGE_NAME = web3env
DOCKERHUB_USERNAME = crinstaniev

build-amd64:
	docker buildx build --platform linux/amd64 -t $(IMAGE_NAME):amd64 .

build-arm64:
	docker buildx build --platform linux/arm64 -t $(IMAGE_NAME):arm64 .

run-amd64:
	docker run -p 8080:8080 $(IMAGE_NAME):amd64

run-arm64:
	docker run -p 8080:8080 $(IMAGE_NAME):arm64

clean:
	docker image rm $(IMAGE_NAME):amd64 $(IMAGE_NAME):arm64

push-amd64:
	docker tag $(IMAGE_NAME):amd64 $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):amd64
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):amd64

push-arm64:
	docker tag $(IMAGE_NAME):arm64 $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):arm64
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):arm64

build: build-amd64 build-arm64
push: push-amd64 push-arm64
