BINDIR = /usr/bin
SCRIPTS := mixup dummy
.PHONY: all
.PHONY: install install-$(SCRIPTS)
.PHONY: uninstall uninstall-$(SCRIPTS)

all:
	@echo "Invalid use of make, please use one of the given options"

install: install-$(SCRIPTS)
	@echo "Installed" $(SCRIPTS)

install-mixup:
	install -m 557 name-mixup.sh $(BINDIR)/iamwho

install-dummy:
	@echo "This is a dummy install option for documentation sake"

uninstall: uninstall-$(SCRIPTS)
	@echo "Removed" $(SCRIPTS)

uninstall-mixup:
	rm -f $(BINDIR)/iamwho

uninstall-dummy:
	@echo "This is a dummy uninstall option for documentation sake"