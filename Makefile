.PHONY = help wheel setup test clean format mypy lint

define HELP_LIST_TARGETS

  To display all targets:
    $$ make help
  To build the latest wheel from Python code:
    $$ make wheel
  To set up the Python package:
    $$ make setup
  Test compiled Arduino code:
    $$ make test
  To remove Python installation artifacts:
    $$ make clean
  To run all formatters:
    $$ make format
  To run mypy over Python code:
    $$ make mypy
  To run all linters:
    $$ make lint

endef

export HELP_LIST_TARGETS

help:
	@echo "$$HELP_LIST_TARGETS"

wheel:
	@pip3 install wheel
	@python3 setup.py clean --all bdist_wheel

setup: wheel
	@pip3 install dist/*whl --force-reinstall

test:
	@python3 -m pip install pytest
	@python3 -m pytest --verbose --capture=no tests

clean:
	@rm -rfv build/ dist/ *.egg-info/

format:
	@black gui tests
	@clang-format -i --verbose --style=file inodaqv2/*.cpp inodaqv2/*.hpp

mypy:
	@mypy --cache-dir=/tmp/mypy_cache_inodaqv2 inodaqv2 tests

lint:
	@cppcheck inodaqv2 --enable=all
