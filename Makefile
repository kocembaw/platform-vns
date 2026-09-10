.PHONY: help up down logs test build deploy clean

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

up:  ## Start the local stack (api + db + generator)
	docker compose up --build

down:  ## Stop the stack (make down ARGS=-v also drops the db volume)
	docker compose down $(ARGS)

logs:  ## Tail the stack logs
	docker compose logs -f

test:  ## Lint + unit tests
	bash ci/test.sh

build:  ## Build and tag the images
	bash ci/build.sh

deploy:  ## Push (if REGISTRY set) and apply the Kubernetes manifests
	bash ci/deploy.sh

clean:  ## Stop the stack and remove volumes
	docker compose down -v
