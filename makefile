tmp_dir = /tmp/get2json

build:
	cp -R . $(tmp_dir)

publish: clean build
	-/opt/google_appengine/appcfg.py update $(tmp_dir)
	read -p "Hit enter to continue..." _

test:
	-/opt/google_appengine/dev_appserver.py .

clean:
	rm -rf $(tmp_dir)
