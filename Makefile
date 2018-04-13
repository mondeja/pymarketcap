.IPHONY:
	install builds dist install install-light dev-install \
	uninstall reinstall clean test test-end2end \
	precompile-sources restore-sources docs-html \
	build-meta show-doc version

builds:
	sudo python3 setup.py build_ext -fi

dist:
	python3 setup.py dist

sdist:
	python3 setup.py sdist

install:
	pip3 install -r requirements.txt
	python3 setup.py install

install-light:
	pip3 install -r requirements.txt
	python3 setup.py install --no-curl

dev-install:
	sudo pip3 install -r dev-requirements.txt
	sudo python3 setup.py install

uninstall:
	sudo pip3 uninstall pymarketcap -y
	make restore-sources

reinstall:
	make clean
	make uninstall
	sudo python3 setup.py install -f

clean:
	sudo rm -Rf .pytest_cache/ .tox/ build/ dist/ pymarketcap.egg-info/ htmlcov/
	sudo find . -type d -name "__pycache__" -exec rm -r {} +
	sudo find . -type d -name "_build" -exec rm -r {} +
	sudo rm pymarketcap/*.c pymarketcap/*.so

test:
	pytest tests -vs

test-end2end:
	pytest tests -vs --end2end

precompile-sources:
	python3 -c "from precompiler import run_builder;import os; \
		run_builder(os.path.join(os.getcwd(), 'pymarketcap', 'core.pyx'))"

restore-sources:
	python3 -c "from precompiler import run_unbuilder;run_unbuilder()"

doc-html:
	cd doc && make html && cd ..

build-meta:
	# Build metadata for the project (README.rst)
	bash scripts/build_doc.sh

show-doc:
	if [ ! -f doc/build/html/index.html ]; then make doc-html; fi
	see "doc/_build/html/index.html"

version:
	cd .. && python3 -c "import pymarketcap;print(pymarketcap.__version__);" cd pymarketcap