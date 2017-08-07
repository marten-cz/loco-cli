#!/usr/bin/make

upload:
	python setup.py sdist upload -r pypi

package-test: upload-test testpypi
	# No more commands

upload-test:
	python setup.py sdist upload -r pypitest

testpypi:
	virtualenv --clear --always-copy pypitest
	#bash -c "source pypitest/bin/activate && pip install -r requirements.txt && pip install -i https://testpypi.python.org/pypi loco-cli && loco-cli config"
	pypitest/bin/pip install -r requirements.txt
	pypitest/bin/pip install -i https://testpypi.python.org/pypi loco-cli
	echo "testapikey" | pypitest/bin/loco-cli config
