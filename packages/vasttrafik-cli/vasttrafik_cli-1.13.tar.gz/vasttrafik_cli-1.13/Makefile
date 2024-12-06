# vasttrafik-cli
# Copyright (C) 2012-2021 Salvo "LtWorf" Tomaselli
#
# vasttrafik-cli is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

all:
	@echo Nothing to do

.PHONY: clean
clean:
	$(RM) -r deb-pkg
	$(RM) -r __pycache__
	$(RM) -r *~
	$(RM) -r .mypy_cache/
	$(RM) -r dist/
	$(RM) -r pypi/
	$(RM) -r build/
	$(RM) -r *egg-info/

.PHONY: dist
dist: clean
	cd ..; tar -czvvf vasttrafik-cli.tar.gz \
		vasttrafik-cli/conf/ \
		vasttrafik-cli/CHANGELOG \
		vasttrafik-cli/COPYING \
		vasttrafik-cli/completion \
		vasttrafik-cli/Makefile \
		vasttrafik-cli/man \
		vasttrafik-cli/vasttrafik \
		vasttrafik-cli/setup.py \
		vasttrafik-cli/mypy.conf \
		vasttrafik-cli/README.md \
		vasttrafik-cli/screenshot.png
	mv ../vasttrafik-cli.tar.gz vasttrafik-cli_`head -1 CHANGELOG`.orig.tar.gz
	gpg --detach-sign -a *.orig.tar.gz

deb-pkg: dist
	mv vasttrafik-cli_`head -1 CHANGELOG`.orig.tar.gz* /tmp
	cd /tmp; tar -xf vasttrafik-cli_*.orig.tar.gz
	cp -r debian /tmp/vasttrafik-cli/
	cd /tmp/vasttrafik-cli/; dpkg-buildpackage --changes-option=-S
	mkdir deb-pkg
	mv /tmp/vasttrafik-cli_* deb-pkg
	$(RM) -r /tmp/vasttrafik-cli
	lintian deb-pkg/*changes

.PHONY: mypy
mypy:
	mypy --config-file mypy.conf vasttrafik

.PHONY: test
test: mypy

.PHONY: upload
upload:
	$(RM) -r dist
	./setup.py sdist
	./setup.py bdist_wheel
	twine upload --username __token__ --password `cat .token` dist/*
