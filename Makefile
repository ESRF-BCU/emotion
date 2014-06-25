#
# E-Motion installation script.
#
# Creates links from standard blissadm directories to
# /users/blissadm/python/bliss_modules/emotion
#


EMOTION_PATH=/users/blissadm/python/bliss_modules/emotion
BLISSADM_PATH=/users/blissadm

# Creates links
install:
	ln -sf ${EMOTION_PATH}/tango/emotion_server ${BLISSADM_PATH}/server/src/emotion_server
	ln -snf ${EMOTION_PATH} ${BLISSADM_PATH}/emotion
	ln -snf ${EMOTION_PATH}/tango/config ${BLISSADM_PATH}/local/userconf/emotion

# Builds sphinx documentation.
doc:
	cd doc
	make html

# Removes links
clean:
	rm -rf *.pyc *~
	rm -f ${BLISSADM_PATH}/server/src/emotion_server
	rm -f ${BLISSADM_PATH}/emotion
	rm -f ${BLISSADM_PATH}/local/userconf/emotion


