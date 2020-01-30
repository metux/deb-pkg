
DOCKER       ?= docker
DOCKER_BUILD ?= $(DOCKER) build
DOCKER_RUN   ?= $(DOCKER) run

PREFIX ?= /usr
BINDIR ?= $(PREFIX)/bin

DOCKER_TAG ?= $(DOCKER_USER)/$(IMAGE_NAME)
CONTAINER_IMAGE ?= $(DOCKER_TAG)
DOCKER_X11 ?= no

## customize me
DOCKER_USER  ?= metux
