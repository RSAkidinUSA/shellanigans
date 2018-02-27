BINDIR = /usr/bin

.PHONY: all
.PHONY: install
.PHONY: uninstall

all:
	@echo "Invalid use of make, please use one of the given options"

install:
	pip3 install psutil
	install -m 557 color-bomb.py $(BINDIR)/color-bomb

uninstall:
	rm -f $(BINDIR)/color-bomb
