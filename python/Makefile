BINDIR = /usr/bin
scripts := $(patsubst %/,%,$(wildcard */))
install-scripts := $(foreach script,$(scripts), install-$(script))
uninstall-scripts := $(foreach script,$(scripts), uninstall-$(script))
.PHONY: all
.PHONY: install $(install-scripts)
.PHONY: uninstall $(uninstall-scripts)

all:
	@echo "Invalid use of make, please use one of the given options"

install: $(install-scripts)
	@echo "Installed:\n" $(install-scripts)

$(install-scripts):
	@echo "Installing: " $@
	$(eval cur-dir=$(subst install-,,$@))
	$(MAKE) -C $(cur-dir) install
	@echo 

uninstall: $(uninstall-scripts)
	@echo "Removed:\n" $(uninstall-scripts)

$(uninstall-scripts):
	@echo "Removing: " $@
	$(eval cur-dir=$(subst uninstall-,,$@))
	$(MAKE) -C $(cur-dir) uninstall
	@echo 