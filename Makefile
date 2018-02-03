#!/usr/bin/make

upload:
	python setup.py sdist upload -r pypi

package-test: upload-test testpypi
	# No more commands

upload-test:
	python setup.py sdist upload -r pypitest

testpypi:
	# Python2
	virtualenv -p `which python2` --clear --always-copy pypitest
	pypitest/bin/pip install -r requirements.txt
	pypitest/bin/pip install -i https://testpypi.python.org/pypi loco-cli
	echo "testapikey" | pypitest/bin/loco-cli config

	# Python3
	virtualenv -p `which python3` --clear --always-copy pypitest
	pypitest/bin/pip install -r requirements.txt
	pypitest/bin/pip install -i https://testpypi.python.org/pypi loco-cli
	echo "testapikey" | pypitest/bin/loco-cli config
