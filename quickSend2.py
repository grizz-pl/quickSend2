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
__version__   = "d.2010.12.13.7"
__license__   = "GPL"
__copyright__ = "Witold Firlej"

import sys
import ConfigParser
import os
from ftplib import FTP_TLS
#
#--------------------------------------------------------------------
#
def verbose (msg, level=1):
	try:
		for item in sys.argv:
			if item == "-v" and level == 1:
				print msg
	except IndexError:
		pass
#
#--------------------------------------------------------------------
#
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
#
#--------------------------------------------------------------------
#
def connectToFtp():
	ftp.connect(config.get("Server", "host"))
	ftp.login(config.get("Server", "user"), config.get("Server", "passwd"))
	ftp.prot_p()
#
#--------------------------------------------------------------------
#
def checkLocalFile(filename):
	result = os.path.isfile(filename)
	##XXX check, also, size of the file
	if result:
		verbose("Local file exist")
		return result # True
	else:
		verbose("There is no something like "+filename)
		return result # False
#
#--------------------------------------------------------------------
#
def checkRemoteFile(filename,category):
	ftp.cwd(category) 
	files = ftp.nlst()
	ftp.cwd("/") 				# return to main folder
	if filename in files:
		verbose("There is file named %s in category %s"%(filename,category))
		return False
	else:
		return True
#
#--------------------------------------------------------------------
#
def sendFile(fileToSend,filename,category):
	verbose("Sending...")
	try:
		ftp.storbinary("STOR " + category + "/" +filename, open(fileToSend, "rb"), 1024)
		verbose("...OK!")
	except:
		verbose("...failed!")
		raise
#
#--------------------------------------------------------------------
#
def addComment(filename, category, comment):
	"""
	add comment in .comments/category/filename.comment
	"""
	try:
		open('comment.txt', 'w').write(comment)
	except:
		verbose("Can not save comment!")
		raise
	try:
		ftp.storlines("STOR " + ".comments/"+category+"/"+filename+".comment", open('comment.txt'))
	except:
		verbose("Can not send comment!")
		raise
#
#--------------------------------------------------------------------
#
def listCategories():
	"""
	list folders on server
	@return folders list
	"""
	files = ftp.nlst()
	folders = []
	for filename in files:
		if isDirectory(filename):
			folders.append(filename)
	return folders
#
#--------------------------------------------------------------------
#
def isDirectory(filename):
	current = ftp.pwd()
	try:
		ftp.cwd(filename)
	except:
		ftp.cwd(current)
		return False
	ftp.cwd(current)
	return True
#
#--------------------------------------------------------------------
#
def addCategory(category):
	"""
	make new folder on Server
	"""
	try:
		ftp.mkd(category)
		ftp.mkd(".comments/"+category)
	except:
		verbose("Can not creaty a new category %s.\n\tThere is propably a file with this same name")
		raise
#
#--------------------------------------------------------------------
#
def work():
	"""
	CUI
	"""
	#
	#----------------------------------------------------------------
	#
	def chooseCategory(folders):
		"""
		choose category
		@return choosed category name
		"""
		i = 1
		for category in folders:
			print str(i)+ " - " + category
			i += 1
		while 1:
			x = raw_input("Choose category number (0 to make a new category): ")
			if x.isdigit():
				if int(x) == 0: 					# add a new category
					newCategory = raw_input("New category name: ")
					addCategory(newCategory)
					return newCategory
				return folders[int(x)-1] 			# return category name
			else:
				print "Numbers only!"
	#
	#----------------------------------------------------------------
	#
	verbose("Conecting...")
	try:
		connectToFtp()
		verbose("Connected!")
	except:
		verbose("Can not connect!")
	fileToSend = sys.argv[1]
	filename = fileToSend
	if checkLocalFile(fileToSend):
		category = chooseCategory(listCategories())
		if not checkRemoteFile(fileToSend,category): 			#if there is, already, file with this filename, on server. Rename it!
			filename = raw_input("File Exists!\n\tEnter a new name for the file: ")
		addComment(filename, category, raw_input("Input comment: "))
		sendFile(fileToSend, filename, category)
	verbose("Bye!")
#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
if __name__ == "__main__":
	verbose("\n\t%s \n\tversion %s \n\tby %s\n" % (__project__, __version__, __author__))
	config = ConfigParser.ConfigParser()
	checkFiles()
	config.read("quickSend2.conf")
	ftp = FTP_TLS()
	work()
