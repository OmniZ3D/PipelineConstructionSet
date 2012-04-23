'''
Author: jason
Created: Apr 15, 2012
Module: startup.pcsGlobalSetup
Purpose: Adds paths to Mobu env
'''
#import getpass #@UnresolvedImport
import os
import platform #@UnresolvedImport
import re #@UnresolvedImport
import sys
import xml.etree.ElementTree as ET #@UnresolvedImport
import inspect #@UnresolvedImport

# assumes system/user PYTHONPATH contains path to ./PipelineConstructionSet/python
import common.core.globalVariables as gv

#--------------------------------------------
# get extra relative paths to add for MotionBuilder
pcsXML = ET.parse('%s/pcsSchema.xml' % gv.schemaLocation)
pcsXMLcore = pcsXML.getiterator('Core')[0]
mobuRelPaths = eval(pcsXMLcore.get('MoBuPaths'))

#--------------------------------------------
# get bitVersion
bit = 'win32'
if platform.architecture()[0] == '64bit': bit = 'win64'

#--------------------------------------------
# add to sys.path
for mobuRelPath in mobuRelPaths:
	
	# add correct bit sub-folder
	if re.search('perforce', mobuRelPath):
		mobuRelPath = '%s/%s' % (mobuRelPath, bit)

	# add correct bit sub-folder
	if re.search('PIL', mobuRelPath):
		mobuRelPath = '%s/%s' % (mobuRelPath, bit)
	
	# add paths from userXML toolpath
	sys.path.append('%s/python/moBu/%s' % (gv.toolsLocation, mobuRelPath))

#--------------------------------------------
# start debugging
import common.diagnostic.wingdbstub #@UnusedImport

#--------------------------------------------
from common.diagnostic.pcsLogger import moBuLogger
# do main import loop
try:
	from moBu.core.sysGlobalMenu import MobuArtMonkeyMenu
except:
	moBuLogger.info(sys.exc_info())
	moBuLogger.errorDialog("Failed to import moBu and start ArtMonkey")
	print "Failed to import moBu. Error: "
	print sys.exc_info()

#--------------------------------------------
# start ArtMonkey Global menu
try:
	MobuArtMonkeyMenu().createTool()
except:
	moBuLogger.error("Failed to create Art Monkey menu")

#--------------------------------------------
# report run from location
def tempFunc():
	pass
fileLocation = os.path.dirname(inspect.getsourcefile(tempFunc))
moBuLogger.info("Ran pcsGlobalSetup.py from '%s'" % fileLocation)