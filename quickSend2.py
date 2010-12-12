#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mirlight by grizz - Witek Firlej http://grizz.pl
# Copyright (C) 2010 Witold Firlej
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

__author__    = "Witold Firlej (http://grizz.pl)"
__project__      = "quickSend2"
__version__   = "0.1"
__license__   = "GPL"
__copyright__ = "Witold Firlej"

import sys
import ConfigParser
import os
from ftplib import FTP_TLS

def verbose (msg, level=1):
	try:
		for item in sys.argv:
			if item == "-v" and level == 1:
				print msg
				break
			elif item == "-vv" and level <= 2:
				print msg
				break
			elif item == "-vvv" and level <= 3:
				print msg
				break
	except IndexError:
		pass



def checkFiles():
	"""
	Check if basic conf file exists. If not, create them.
	"""
	if not os.path.exists('quickSend2.conf'):
		verbose("Creating quickSend2.conf file")
		config.add_section("Server")
		config.set("Server", "host", "")
		config.set("Server", "user", "")
		config.set("Server", "passwd", "") 		##XXX no plain text here!
		with open('quickSend2.conf', 'wb') as configfile:
			config.write(configfile)



def connectToFtp():
	ftp.connect(config.get("Server", "host"))
	ftp.login(config.get("Server", "user"), config.get("Server", "passwd"))
	ftp.prot_p()

def checkLocalFile(file):
	result = os.path.isfile(file)
	##XXX check, also, size of the file
	if result:
		verbose("Local file exist")
		return result # True
	else:
		verbose("There is no something like "+file)
		return result # False



def checkRemoteFile(file):
	files = ftp.nlst()
	if file in files:
		verbose("There is file named %s on Server"%file)
		return False
	else:
		return True


def sendFile(file):
	verbose("Sending...")
	try:
		ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
		addComment(file)
		verbose("...OK!")
	except:
		verbose("...failed!")
		raise

def addComment(file):
	open('comment.txt', 'w').write(raw_input("Input comment: "))
	ftp.storlines("STOR " + ".comments/"+file+".comment", open('comment.txt'))
	#plik = open(file+".comment", 'w')
	#plik.write("komentarz do pliku")
	#plik.close()

if __name__ == "__main__":
	verbose("\n\t%s \n\tversion %s \n\tby %s\n" % (__project__, __version__, __author__))
	config = ConfigParser.ConfigParser()
	checkFiles()
	config.read("quickSend2.conf")
	ftp = FTP_TLS()
	verbose("Conecting...")
	try:
		connectToFtp()
		verbose("Connected!")
	except:
		verbose("Can not connect!")
	fileToSend = sys.argv[1]
	if checkLocalFile(fileToSend) and checkRemoteFile(fileToSend):
			sendFile(fileToSend)
	verbose("Bye!")
