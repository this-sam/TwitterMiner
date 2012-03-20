#==========================================================
#TODO:
#	-- Make a globals class so that I can globally set debug, parameters
#	-- Lots of other things that i won't forget because i need to do them
#  -- Look into measuring where in the sentence the word is located that is edited
#      --> statistical analysis on sentences... from twitter, etc.?  db of
#			  messenger convos?

class TwitterMiner:
	
	global re, pprint
	import os, pprint, re
	
	global Tweet, Settings
	from Tweet import Tweet
	from Settings import Settings

	
	def __init__(self):
		"""Initialize TwitterMiner Class
		"""
		#log errors
		self.errors = []
		
		#get input files
		#store files in dictionary --> USERNAME =>
		self.surveyFiles, self.userFiles = self.__getFiles()
		print self.surveyFiles, self.userFiles
		
		self.chats = self.__makeChats()
		
		#make sure we loaded files
		if len(self.chats) > 0:
			#Write Message Feature File
			self.featureVectors = self.getMessageFeatureVectors()
			self.featureSet = self.chats[0].userA.messages[0].getFeatureSet()
			self.printToCSV(self.featureVectors, self.featureSet, "MessageFeatures.csv")
						
			#Write User Feature File
			self.featureVectors = self.getUserFeatureVectors()
			self.featureSet =  self.chats[0].userA.getFeatureSet()
			self.printToCSV(self.featureVectors, self.featureSet, "UserFeatures.csv")
		else:
			print "No chat files could be found."
		
		if Settings.DEBUG:
			self.__debug()





#===============================================
#--------------Private Functions----------------
	def __getFiles(self):
		"""
		Load 
		"""
		surveyFiles = []
		userFiles = []
		
		#walk the file directory
		for dirpath, dirnames, filenames in TwitterMiner.os.walk(Settings.ROOT_DIR):
			for f in filenames:
				file = TwitterMiner.os.path.join(dirpath, f)
				
				if (re.search("[A-D]_[0-9_]*.txt",file) != None):
					#trim file name and search string
					file = file[len(Settings.ROOT_DIR):]
					userFiles.append(file)
				elif (re.search(".csv",file) != None):
					surveyFiles.append(file)
					
		return surveyFiles, userFiles


















#==============================================================================
# FROM ATTRIBUTE SELECTOR CLASS
#===============================================
#--------------Public  Functions----------------

	def getUserFeatureVectors(self):
		featureVectors = []			
		for chat in self.chats:
			featureVectors.append(chat.userA.featureVector)
			featureVectors.append(chat.userB.featureVector)
		return featureVectors
	
	def getMessageFeatureVectors(self):
		featureVectors = []			
		for chat in self.chats:
			for message in chat.userA.messages+chat.userB.messages:
				featureVectors.append(message.featureVector)
		return featureVectors

	def printToCSV(self, featureVectors, featureSet, fileName = "Features.csv", withHeader=True, overwrite=True):
		if overwrite:
			f = open(fileName, 'w')
		else:
			f = open(fileName, 'a')
		
		if withHeader:
			for heading in featureSet:
				f.write(heading+",")
			f.write("\r\n")
		
		for vector in featureVectors:
			row = ""
			for element in vector:
				row+=str(element)+","
			f.write(row+"\r\n")
		f.close()
		
			
			

	

	def __makeChats(self):
		"""Create conversations by loading users from survey and message files
		
		creates an array of chats
		"""
		surveys = []
		users = {}
		chats = []
		
		for surveyFile in self.surveyFiles:
			survey = open(surveyFile, 'r')
			date = surveyFile.split('/')[0]
			
			#create a new Survey and user for each line in the survey file
			#add the users to a temporary array so that they can be added into chats
			tmpUsers = {}
			for line in survey:
				#temporary hack to prevent out of memory errors
				#if len(tmpUsers) > 20:
				#	break
				
				surveys.append(Survey(line))
				userFile = surveys[-1].getUserFilename()
				userFName = Settings.ROOT_DIR+userFile
				
				#handle uncertain filenames
				try:
					userEventString = open(userFName, 'r').read()
					user = User(userEventString, surveys[-1])
					tmpUsers[user.index] = user
				except IOError:
					print "Expected file "+userFile+" was not found."
				#prevent memory leaks
				#if len(tmpUsers) >= 14:
				#	break
				
			#pair users and create chats	
			for username, user in tmpUsers.iteritems():
				if ((user.classification == 'A') or (user.classification == 'C')):
					#handle unpaired users
					try:
						chats.append(Chat(user, tmpUsers[user.partnerIndex]))
					except Exception:
						print "User "+user.username+" could not find their partner."
		return chats			


	def __debug(self):
		print "Dumping Object TwitterMiner"
		pprint.pprint(self.surveyFiles)
		pprint.pprint(self.userFiles)
		pprint.pprint(self.errors)


if __name__ == '__main__':
	selector = TwitterMiner()
	 
	 
	 
