install:
	sudo apt-get install supervisor python-pip python-virtualenv openjdk-7-jre
	if test -d /home/minecraft; \
	  then echo minecraft user already exists; \
	else sudo useradd -d /home/minecraft minecraft; \
	fi
	sudo python setup.py install

test:
	rm -rf .tox
	detox

clean:
	rm -rf venv

rename:
	find . -maxdepth 1 -type f \( ! -iname "Makefile" \) -print0 | xargs -0 sed -i 's/outline/$(name)/g'
	find outline -maxdepth 1 -type f -print0 | xargs -0 sed -i 's/outline/$(name)/g'
	mv outline/manage_outline.py outline/manage_$(name).py
	mv outline $(name)
	echo "Great, you're all set! Well, you'll probably want to adjust the setup file by hand a bit."
