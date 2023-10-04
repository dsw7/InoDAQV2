.PHONY = help upload wheel setup test black mypy tidy

define HELP_LIST_TARGETS

  To display all targets:
    $$ make help
  To build the latest wheel from Python code:
    $$ make wheel
  To set up the Python package:
    $$ make setup
  To upload compiled Arduino code to board:
    $$ make upload
  Test compiled Arduino code:
    $$ make test
  To remove Python installation artifacts:
    $$ make clean
  To run black over Python code:
    $$ make black
  To run mypy over Python code:
    $$ make mypy
  To lint HTML code:
    $$ make tidy

endef

export HELP_LIST_TARGETS

help:
	@echo "$$HELP_LIST_TARGETS"

wheel:
	@pip3 install wheel
	@python3 setup.py clean --all bdist_wheel

setup: wheel
	@pip3 install dist/*whl --force-reinstall

upload: setup
	@inodaq-upload

test: upload
	@python3 -m pip install pytest
	@python3 -m pytest --verbose --capture=no tests

clean:
	@rm -rfv build/ dist/ *.egg-info/

black:
	@black inodaqv2 tests

mypy:
	@mypy --cache-dir=/tmp/mypy_cache_inodaqv2 inodaqv2 tests

tidy:
	@tidy -errors inodaqv2/templates/*html
