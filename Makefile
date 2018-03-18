.IPHONY:
	install builds dist install install-light dev-install \
	uninstall reinstall clean test test-end2end \
	precompile-sources restore-sources docs-html version

builds:
	sudo python3 setup.py build_ext -fi

dist:
	python3 setup.py dist

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
	sudo rm -Rf .pytest_cache/ .tox/ build/ dist/ pymarketcap.egg-info/
	sudo find . -type d -name "__pycache__" -exec rm -r {} +
	sudo find . -type d -name "_build" -exec rm -r {} +
	sudo rm pymarketcap/*.c pymarketcap/*.so

test:
	pytest tests -vs

test-end2end:
	pytest tests -vs --end2end --cov

precompile-sources:
	python3 -c "from precompiler import run_builder;import os; \
		run_builder(os.path.join(os.getcwd(), 'pymarketcap', 'core.pyx'))"

restore-sources:
	python3 -c "from precompiler import run_unbuilder;run_unbuilder()"

docs-html:
	cd docs && make html && cd ..

version:
	cd .. && python3 -c "import pymarketcap;print(pymarketcap.__version__);" cd pymarketcap