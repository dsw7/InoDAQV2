.PHONY = help compile upload test

ifndef TMP
    ifndef TMPDIR
        $(error No "TMP" or "TMPDIR" environment variable. Cannot proceed)
    endif
    TMP=$(TMPDIR)
endif

BUILD_PATH = $(TMP)/inodaq-v2-build/
CORE_CACHE_PATH = $(TMP)/inodaq-v2-core-cache/
PATH_CFG = src/configs/inodaqv2.ini
SERIAL_PORT := $(shell grep ^port $(PATH_CFG) | awk '{print $$3}')
LIGHT_PURPLE = "\033[1;1;35m"
NO_COLOR = "\033[0m"
FULLY_QUALIFIED_BOARD_NAME = arduino:avr:uno
PATH_INO_SRC = src/ino

define MESSAGE
	@echo -e $(LIGHT_PURPLE)\> $(1)$(NO_COLOR)
endef

define HELP_LIST_TARGETS
To display all targets:
    $$ make help
Compile Arduino code:
    $$ make compile
Upload compiled Arduino code to board:
    $$ make upload
Test compiled Arduino code:
    $$ make test
endef

export HELP_LIST_TARGETS

help:
	@echo "$$HELP_LIST_TARGETS"

compile:
	$(call MESSAGE,Compiling Arduino code)
	@arduino-cli compile \
	--port $(SERIAL_PORT) \
	--fqbn $(FULLY_QUALIFIED_BOARD_NAME) \
	--verbose \
	--build-path=$(BUILD_PATH) \
	--build-cache-path=$(CORE_CACHE_PATH) \
	$(PATH_INO_SRC)/

upload: compile
	$(call MESSAGE,Uploading Arduino code)
	@arduino-cli upload \
	--port $(SERIAL_PORT) \
	--fqbn $(FULLY_QUALIFIED_BOARD_NAME) \
	--verbose \
	--input-dir=$(BUILD_PATH) \
	$(PATH_INO_SRC)/

test: upload
	$(call MESSAGE,Running unit tests)
	@python3 -m pytest --verbose --capture=no .
