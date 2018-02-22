BINDIR = /usr/bin
scripts := $(patsubst %/,%,$(wildcard */))
build-scripts := $(foreach script,$(scripts), build-$(script))
clean-scripts := $(foreach script,$(scripts), clean-$(script))
.PHONY: all
.PHONY: build $(build-scripts)
.PHONY: clean $(clean-scripts)

all:
	@echo "Invalid use of make, please use one of the given options"

build: $(build-scripts)
	@echo "Ran:\n" $(build-scripts)

$(build-scripts):
	$(eval cur-dir=$(subst build-,,$@))
	@echo "Building: " $(cur-dir)
	@$(MAKE) -C $(cur-dir) build
	@echo 

clean: $(clean-scripts)
	@echo "Ran:\n" $(clean-scripts)

$(clean-scripts):
	$(eval cur-dir=$(subst clean-,,$@))
	@echo "Cleaning: " $(cur-dir)
	@$(MAKE) -C $(cur-dir) clean
	@echo 