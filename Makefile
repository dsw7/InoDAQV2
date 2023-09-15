.PHONY = help compile upload wheel setup install test black mypy

ifndef TMP
    ifndef TMPDIR
        $(error No "TMP" or "TMPDIR" environment variable. Cannot proceed)
    endif
    TMP=$(TMPDIR)
endif

BUILD_PATH = $(TMP)/inodaq-v2-build/
CORE_CACHE_PATH = $(TMP)/inodaq-v2-core-cache/
PATH_CFG = $(HOME)/.inodaqv2.ini
SERIAL_PORT := $(shell grep ^port $(PATH_CFG) | awk '{print $$3}')
FULLY_QUALIFIED_BOARD_NAME = arduino:avr:uno
PATH_INO_SRC = ino

define HELP_LIST_TARGETS

	To display all targets:
		$$ make help
	Compile Arduino code:
		$$ make compile
	Upload compiled Arduino code to board:
		$$ make upload
	To build the latest wheel from Python code:
		$$ make wheel
	To set up the Python package:
		$$ make setup
	To install project end-to-end:
		$$ make install
	Test compiled Arduino code:
		$$ make test
	To remove Python installation artifacts:
		$$ make clean
	To run black over Python code
		$$ make black
	To run mypy over Python code
		$$ make mypy

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

upload:
	@arduino-cli upload \
	--port $(SERIAL_PORT) \
	--fqbn $(FULLY_QUALIFIED_BOARD_NAME) \
	--verbose \
	--input-dir=$(BUILD_PATH) \
	$(PATH_INO_SRC)/

wheel:
	@pip3 install wheel
	@python3 setup.py clean --all bdist_wheel

setup:
	@pip3 install dist/*whl --force-reinstall

install: compile upload wheel setup

test: install
	@python3 -m pytest --verbose --capture=no tests

clean:
	@rm -rfv build/ dist/ *.egg-info/

black:
	@black inodaqv2 tests

mypy:
	@mypy --cache-dir=/tmp/mypy_cache_inodaqv2 inodaqv2 tests
