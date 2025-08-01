all: build

build:
	npm install
	npm run build

install:
	mkdir -p $(DESTDIR)/usr/share/cockpit/sftp-manager
	cp -r dist/* $(DESTDIR)/usr/share/cockpit/sftp-manager
	mkdir -p $(DESTDIR)/usr/lib/cockpit/sftp-manager
	cp src/backend/*.py $(DESTDIR)/usr/lib/cockpit/sftp-manager
	touch $(DESTDIR)/var/log/sftp_user_setup.log
	chown root:root $(DESTDIR)/var/log/sftp_user_setup.log
	chmod 600 $(DESTDIR)/var/log/sftp_user_setup.log

clean:
	rm -rf node_modules dist

package-rpm:
	rpmbuild -ba cockpit-sftp-manager.spec

package-deb:
	dpkg-buildpackage -us -uc



