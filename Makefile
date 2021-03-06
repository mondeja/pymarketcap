.PHONY:
	install builds dist install install-light dev-install \
	uninstall reinstall clean test test-end2end \
	precompile-sources restore-sources docs-html \
	build-meta show-doc version

python = python3
run-setup = $(python) setup.py
pip = pip3
pip-install = $(pip) install

builds:
	$(run-setup) build_ext -fi

dist:
	$(run-setup) dist

sdist:
	$(run-setup) sdist

install:
	$(pip install) -r requirements.txt
	$(run-setup) install

install-light:
	$(pip install) -r requirements.txt
	$(run-setup) install --no-curl

install-dev:
	$(pip install) -r dev-requirements.txt
	$(run-setup) develop

uninstall:
	$(pip) uninstall pymarketcap -y
	make restore-sources

reinstall:
	make clean
	make uninstall
	$(run-setup) install -f

clean:
	sudo rm -Rf .pytest_cache/ .tox/ build/ \
		dist/ pymarketcap.egg-info/ htmlcov/
	sudo find . -type d -name "__pycache__" -exec rm -r {} +
	sudo find . -type d -name "_build" -exec rm -r {} +
	sudo rm pymarketcap/*.c pymarketcap/*.so tests/cache/*.json

test:
	pytest test -vs

test-end2end:
	pytest test -vs --end2end

precompile-sources:
	$(python) -c "from precompiler import run_builder;import os; \
		run_builder(os.path.join(os.getcwd(), 'pymarketcap', 'core.pyx'))"

restore-sources:
	$(python) -c "from precompiler import run_unbuilder;run_unbuilder()"

doc-html:
	cd doc && make html && cd ..

build-meta:
	# Build metadata for the project (README.rst)
	bash scripts/build_doc.sh

show-doc:
	if [ ! -f doc/build/html/index.html ]; then make doc-html; fi
	see "doc/_build/html/index.html"

version:
	cd ..
	$(python) -c "import pymarketcap as p;print(p.__version__);"
	cd pymarketcap

version-micro-up:
	$(python) scripts/vss.py micro

version-micro-down:
	$(python) scripts/vss.py unmicro
