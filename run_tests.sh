#!/bin/sh

python3 -m nose --with-xunit --with-coverage --cover-inclusive \
		--cover-branches --cover-html --cover-xml --cover-erase \
		--cover-package=backend --verbosity 2 $*
exit $?
