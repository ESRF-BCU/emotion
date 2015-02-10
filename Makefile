#
# E-Motion installation script.
#
# Creates links from standard blissadm directories to
# /users/blissadm/python/bliss_modules/emotion
#

BLISSADM_PATH=/users/blissadm

MOD_PATH=${BLISSADM_PATH}/python/bliss_modules

CONFIG_PATH=${BLISSADM_PATH}/local/userconf/emotion

TEMPLATES_PATH=${CONFIG_PATH}/templates

DEV_PATH=${PWD}

# "Distribution" installation.
# Copy of files from current git directory.
install:
        # install of the py module.
	python setup.py install

        # config dir and template files.
	mkdir -p ${TEMPLATES_PATH}
	chmod 777 ${CONFIG_PATH}
	cp config/*.xml ${TEMPLATES_PATH}
	cp config/*.yml ${TEMPLATES_PATH}

        # tango server and startup-script
        # oups : faire un test...
	touch ${BLISSADM_PATH}/server/src/emotion_server
	mv ${BLISSADM_PATH}/server/src/emotion_server ${BLISSADM_PATH}/server/src/emotion_server.bup
	cp tango/emotion_server ${BLISSADM_PATH}/server/src/emotion_server

        # oups : faire un test...
	touch ${BLISSADM_PATH}/server/src/Emotion.py
	mv ${BLISSADM_PATH}/server/src/Emotion.py ${BLISSADM_PATH}/server/src/Emotion.py.pub
	cp tango/Emotion.py ${BLISSADM_PATH}/server/src/Emotion.py

        # oups : faire un test...
	touch ${BLISSADM_PATH}/server/src/TgGevent.py
	mv ${BLISSADM_PATH}/server/src/TgGevent.py ${BLISSADM_PATH}/server/src/TgGevent.py.bup
	cp tango/TgGevent.py ${BLISSADM_PATH}/server/src/TgGevent.py

        # Spec macros
	mv ${BLISSADM_PATH}/spec/macros/tango_mot.mac ${BLISSADM_PATH}/spec/macros/tango_mot.mac.bup
	cp spec/tango_mot.mac ${BLISSADM_PATH}/spec/macros/tango_mot.mac


# "Development" installation.
# Creates links from current git directory.
devi: install

        # remove install...
	mv ${MOD_PATH}/emotion ${MOD_PATH}/emotion_orig

        # Links do dev version
	ln -s ${DEV_PATH}/emotion ${MOD_PATH}/emotion

        # tango
	ln -sf ${DEV_PATH}/tango/emotion_server ${BLISSADM_PATH}/server/src/emotion_server
	ln -sf ${DEV_PATH}/tango/Emotion.py ${BLISSADM_PATH}/server/src/Emotion.py
	ln -sf ${DEV_PATH}/tango/TgGevent.py ${BLISSADM_PATH}/server/src/TgGevent.py

        # Spec
	ln -sf ${DEV_PATH}/spec/tango_mot.mac ${BLISSADM_PATH}/spec/macros/tango_mot.mac


# ACHTUNG
remove:
	rm -rf ${MOD_PATH}/emotion_orig


# Builds sphinx documentation.
doc:
	cd doc
	make html


# Removes links
clean:
	rm -rf *.pyc *~
	rm -f ${BLISSADM_PATH}/server/src/emotion_server
	rm -f ${BLISSADM_PATH}/emotion
	rm -f ${BLISSADM_PATH}/spec/macros/tango_mot.mac

