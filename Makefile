.PHONY = help upload wheel setup test black mypy

define HELP_LIST_TARGETS

	To display all targets:
		$$ make help
	Upload compiled Arduino code to board:
		$$ make upload
	To build the latest wheel from Python code:
		$$ make wheel
	To set up the Python package:
		$$ make setup
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

upload:
	@python3 ino/upload.py COM3

wheel:
	@pip3 install wheel
	@python3 setup.py clean --all bdist_wheel

setup: wheel
	@pip3 install dist/*whl --force-reinstall

test: upload setup
	@python3 -m pip install pytest
	@python3 -m pytest --verbose --capture=no tests

clean:
	@rm -rfv build/ dist/ *.egg-info/

black:
	@black inodaqv2 tests ino

mypy:
	@mypy --cache-dir=/tmp/mypy_cache_inodaqv2 inodaqv2 tests ino
