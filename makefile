all: build-deb-setup build-deb install-deb

build-deb-setup:
	sudo apt update
	sudo apt install -y debhelper dh-python python3.8-venv python3-all
	python3 -m venv venv
	venv/bin/pip install stdeb debhelper

build-deb:
	venv/bin/python setup.py --command-packages=stdeb.command bdist_deb

clean:
	rm -r *.egg-info *.tar.gz *dist* venv

install-deb:
	sudo dpkg -i deb_dist/*.deb