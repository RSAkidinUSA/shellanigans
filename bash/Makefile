BINDIR = /usr/bin
scripts := mixup dummy
install-scripts := $(foreach script,$(scripts), install-$(script))
uninstall-scripts := $(foreach script,$(scripts), uninstall-$(script))
.PHONY: all
.PHONY: install $(install-scripts)
.PHONY: uninstall $(uninstall-scripts)

all:
	@echo "Invalid use of make, please use one of the given options"

install: $(install-scripts)
	@echo "Installed:\n" $(install-scripts)

install-mixup:
	install -m 557 name-mixup.sh $(BINDIR)/iamwho

install-dummy:
	@echo "This is a dummy install option for documentation sake"

uninstall: $(uninstall-scripts)
	@echo "Removed:\n" $(uninstall-scripts)

uninstall-mixup:
	rm -f $(BINDIR)/iamwho

uninstall-dummy:
	@echo "This is a dummy uninstall option for documentation sake"