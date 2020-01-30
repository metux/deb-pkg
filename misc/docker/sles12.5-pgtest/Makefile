TOPDIR			:= ../
IMAGE_NAME		:= sles12.5-pgtest

include $(TOPDIR)/common/std.mk

build-docker-image:	prepare-files

prepare-files:
	@rm -Rf files/upload/zyprepo
	@mkdir -p files/upload/zyprepo
	@cp -R ../../.zyprepo/default/* files/upload/zyprepo
