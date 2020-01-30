
include $(TOPDIR)/common/conf.mk

ALL_SCRIPTS := $(SCRIPTS) $(AUTOGEN_SCRIPT)

build:	build-docker-image $(ALL_SCRIPTS)

build-docker-image:
	@$(DOCKER_BUILD) . -t $(DOCKER_TAG)

install-scripts:	$(ALL_SCRIPTS)
	@mkdir -p $(DESTDIR)/$(BINDIR)
	@for s in $(ALL_SCRIPTS) ; do cp $$s $(DESTDIR)/$(BINDIR) ; chmod ugo+x $(DESTDIR)/$(BINDIR)/`basename $$s` ; done

install:	install-scripts

install-local:
	@$(MAKE) BINDIR=$(HOME)/.bin install-scripts

clean:
	@rm -f $(AUTOGEN_SCRIPT)

ifneq ($(AUTOGEN_SCRIPT),)
$(AUTOGEN_SCRIPT): $(TOPDIR)/common/runscript.head $(TOPDIR)/common/runscript.tail
	@( \
            cat $(TOPDIR)/common/runscript.head ; \
            echo "" ; \
            echo "# BEGIN configuration" ; \
            echo "CONTAINER_IMAGE=\"$(CONTAINER_IMAGE)\"" ; \
            echo "CONTAINER_X11=\"$(CONTAINER_X11)\"" ; \
            echo "CONTAINER_DRI=\"$(CONTAINER_DRI)\"" ; \
            echo "CONTAINER_NAME=\"$(CONTAINER_NAME)\"" ; \
            echo "CONTAINER_AUDIO=\"$(CONTAINER_AUDIO)\"" ; \
            echo "# END configuration" ; \
            echo "" ; \
            if [ -f runscript.extra ]; then \
                echo "#### BEGIN runscript.extra" ; \
                cat runscript.extra ; \
                echo "#### END runscript.extra" ; \
                echo "" ; \
            fi ; \
            cat $(TOPDIR)/common/runscript.tail \
        ) > $@
	@chmod +x $@
endif

push:
	@$(DOCKER) push $(DOCKER_TAG)

.PHONY: build build-scripts build-image install clean
