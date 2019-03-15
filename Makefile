# Makefile variables
PACKAGE_NAME = slack-xlrelease-app
MAKE := $(MAKE) --no-print-directory
SHELL = /bin/bash
OUTPUT_DIR = output
VERSION := $(shell git describe --tags --always --dirty | sed -e 's/slack-xlrelease-app-//' | tr -d '\n')

help :
	@echo "Makefile for $(PACKAGE_NAME)"
	@echo
	@echo 'Generic targets:'
	@echo
	@echo "    ▶ build                               Build the project"
	@echo "    ▶ test                                Run tests"
	@echo "    ▶ docker-build                        Build Docker images in this project"
	@echo "    ▶ docker-push                         Build and push Docker images in this project"
	@echo "    ▶ release-tag                         Tag current state of the project with a version"

build : set-version

set-version :
	@echo Project version: $(VERSION)
	@echo "$(VERSION)" > bot/version.txt

docker-build : build
	docker build -f docker/app/Dockerfile -t xebialabsunsupported/slack-xlrelease-app:$(VERSION) -t xebialabsunsupported/slack-xlrelease-app:latest .

docker-push : docker-build
	docker push xebialabsunsupported/slack-xlrelease-app:$(VERSION)
	docker push xebialabsunsupported/slack-xlrelease-app:latest

release-tag :
	@[ -n "${NEW_VERSION}" ] || (echo "set NEW_VERSION to the version you want to release, e.g. 1.0.1" && false)
	@git diff-files --quiet --ignore-submodules -- > /tmp/log 2>&1 || (\
		echo >&2 "Cannot release: you have unstaged changes:" && \
		git diff-files --name-status -r --ignore-submodules -- >&2 && \
		false \
	)
	@echo Current version is $(VERSION), releasing $(NEW_VERSION)
	@git tag -a -m slack-xlrelease-app-$(NEW_VERSION) slack-xlrelease-app-$(NEW_VERSION)
