.PHONY = help compile upload test black

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
FULLY_QUALIFIED_BOARD_NAME = arduino:avr:uno
PATH_INO_SRC = src/ino

define HELP_LIST_TARGETS
To display all targets:
    $$ make help
Compile Arduino code:
    $$ make compile
Upload compiled Arduino code to board:
    $$ make upload
Test compiled Arduino code:
    $$ make test
To run black over Python code
    $$ make black
endef

export HELP_LIST_TARGETS

help:
	@echo "$$HELP_LIST_TARGETS"

compile:
	@arduino-cli compile \
	--port $(SERIAL_PORT) \
	--fqbn $(FULLY_QUALIFIED_BOARD_NAME) \
	--verbose \
	--build-path=$(BUILD_PATH) \
	--build-cache-path=$(CORE_CACHE_PATH) \
	$(PATH_INO_SRC)/

upload: compile
	@arduino-cli upload \
	--port $(SERIAL_PORT) \
	--fqbn $(FULLY_QUALIFIED_BOARD_NAME) \
	--verbose \
	--input-dir=$(BUILD_PATH) \
	$(PATH_INO_SRC)/

test: upload
	@python3 -m pytest --verbose --capture=no .

black:
	@black src
