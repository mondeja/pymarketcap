.IPHONY: install builds clean test bench proof

builds:
	python3 setup.py build_ext -fi

dist:
	python3 setup.py dist

install:
	pip3 install -r requirements.txt
	python3 setup.py install

dev-install:
	pip3 install -r dev-requirements.txt
	python3 setup.py install

uninstall:
	pip3 uninstall pymarketcap -y
	make restore-sources

clean:
	sudo rm -Rf .pytest_cache/ .tox/ build/
	sudo find . -type d -name "__pycache__" -exec rm -r {} +
	sudo rm pymarketcap/core.c pymarketcap/curl.c

test:
	pytest tests -vs

test-end2end:
	pytest tests -vs --end2end

precompile-sources:
	python3 -c "from precompiler import run_builder;import os; \
		run_builder(os.path.join(os.getcwd(), 'pymarketcap', 'core.pyx'))"

restore-sources:
	python3 -c "from precompiler import run_unbuilder;run_unbuilder()"