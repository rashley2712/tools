""" Some functions to aid the setting and retrieving of config files saved in the user's home directory """

import os, json, numpy

class configClass:
	def __init__(self, name="unknownapp"):
		self._appName = name
		self._filename = getUserHome() +"/.config/" + self._appName + "/" + self._appName + ".conf"
		createConfigFolder(self._appName)
		self._alreadyExists = False
		# print "DEBUG: config file is at:", self._filename
		self.load()
		
	def getProperty(self, name):
		try:
			property = getattr(self, name)
		except AttributeError:
			property = None
		return property	

	def setProperty(self, key, value):
		setattr(self, key, value)
		
					
	def load(self):
		filename = self._filename
		if os.path.exists(filename):
			self._alreadyExists = True
		else:
			print "DEBUG: The configfile, %s, does not exist yet."%filename
			return False
	
		inputfile = open(filename, "r")
		jsonObject = json.load(inputfile)
		for key in jsonObject.keys():
			keyString = str(key)
			value = jsonObject[key]
			if type(value) is unicode: 
				value = str(value)
			if type(value) is list:
				value = numpy.array(value)
			setattr(self, key, value)
		inputfile.close()
		return True
		
	def save(self):
		filename = self._filename
		object = {}
		for key in self.__dict__.keys():
			if key[0]=='_': continue         # Don't write properties that start with an underscore
			data = getattr(self, key)
			# print key, type(data)
			if type(data)==numpy.float32:
				data = float(data)
			if type(data)==numpy.ndarray:
				data = numpy.array(data).tolist()
			if type(data)==list:
				data = numpy.array(data).tolist()
			object[key] = data
			
		outputfile = open(filename, 'w')
		json.dump(object, outputfile, indent = 4)
		outputfile.close()	

def getUserHome():
	homeDir = os.path.expanduser('~')
	# print "DEBUG: The user's home directory is %s."%homeDir
	return homeDir

def createConfigFolder(appName):
	homeDir = getUserHome()
	
	configPath = homeDir + "/.config"
	if not os.path.exists(configPath):
		os.mkdir(configPath)
		print "DEBUG: Creating directory %s"%configPath
		
	fullConfigPath = configPath + "/" + appName
	if not os.path.exists(fullConfigPath):
		os.mkdir(fullConfigPath)
		print "DEBUG: Creating directory %s"%fullConfigPath
	

	
		
