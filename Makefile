#
# E-Motion installation.
#

# Installation directories :
# /users/blissadm/python/bliss_modules/
# /users/blissadm/local/userconf/emotion/
# /users/blissadm/local/userconf/emotion/templates/
# /users/blissadm/server/src/emotion_server



BLISSADM_PATH=/users/blissadm

MOD_PATH=${BLISSADM_PATH}/python/bliss_modules

CONFIG_PATH=${BLISSADM_PATH}/local/userconf/emotion

TEMPLATES_PATH=${CONFIG_PATH}/templates

DEV_PATH=${PWD}

# "Distribution" installation.
# Copy of files from current git directory.
install:
        ####  install of the py module.
	python setup.py install

        ####  config dir and template files.
	mkdir -p ${TEMPLATES_PATH}
	chmod 777 ${CONFIG_PATH}
	cp config/*.xml ${TEMPLATES_PATH}
	cp config/*.yml ${TEMPLATES_PATH}

        ####  tango server and startup-script
	mkdir -p ${BLISSADM_PATH}/server/src
	touch ${BLISSADM_PATH}/server/src/emotion_server
	mv ${BLISSADM_PATH}/server/src/emotion_server ${BLISSADM_PATH}/server/src/emotion_server.bup
	cp tango/emotion_server ${BLISSADM_PATH}/server/src/emotion_server

	touch ${BLISSADM_PATH}/server/src/Emotion.py
	mv ${BLISSADM_PATH}/server/src/Emotion.py ${BLISSADM_PATH}/server/src/Emotion.py.pub
	cp tango/Emotion.py ${BLISSADM_PATH}/server/src/Emotion.py

	touch ${BLISSADM_PATH}/server/src/TgGevent.py
	mv ${BLISSADM_PATH}/server/src/TgGevent.py ${BLISSADM_PATH}/server/src/TgGevent.py.bup
	cp tango/TgGevent.py ${BLISSADM_PATH}/server/src/TgGevent.py

        ####  Spec macros
	mv ${BLISSADM_PATH}/spec/macros/tango_mot.mac ${BLISSADM_PATH}/spec/macros/tango_mot.mac.bup
	cp spec/tango_mot.mac ${BLISSADM_PATH}/spec/macros/tango_mot.mac


# Builds sphinx documentation.
doc:
	cd doc
	make html


