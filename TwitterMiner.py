class TwitterMiner(object):
	
	global re, pprint
	import os, pprint, re
	
	global json
	import simplejson as json
	
	global Tweet, Settings
	from Tweet import Tweet
	from Settings import Settings
	
	def __init__(self):
		"""Initialize TwitterMiner Class
		"""
		#Tools:
		self.decoder = json.JSONDecoder()
		
		#get input files
		self.jsonFiles = self.getFiles()
		
		if Settings.DEBUG:
			print self.jsonFiles
		
		file, line = self.jsonFiles[0], 0
		fhandle = open(file, 'r')

		#loop through tweets
		ct = 0
		for line in fhandle.readlines():
			line = unicode(line)
			nextTweet, self.nextLine = self.getTweetDict(line)
			if "user" in nextTweet:
				if nextTweet["user"]["lang"] == "en":
					#temporary
					ct +=1
					if ct>100:
						break
					#print each line, formatted nicely.
					print "\n----------------Tweet "+str(ct)+"------------------------------\n"
					tweet = Tweet(nextTweet)
					
		
		if Settings.DEBUG:
			print nextTweet
		##make sure we loaded files
		#if len(self.chats) > 0:
		#	#Write Message Feature File
		#	self.featureVectors = self.getMessageFeatureVectors()
		#	self.featureSet = self.chats[0].userA.messages[0].getFeatureSet()
		#	self.printToCSV(self.featureVectors, self.featureSet, "MessageFeatures.csv")
		#				
		#	#Write User Feature File
		#	self.featureVectors = self.getUserFeatureVectors()
		#	self.featureSet =  self.chats[0].userA.getFeatureSet()
		#	self.printToCSV(self.featureVectors, self.featureSet, "UserFeatures.csv")
		#else:
		#	print "No chat files could be found."
		
		if Settings.DEBUG:
			self.__debug()


	def getTweetDict(self, tweetString):
		decodeTuple = self.decoder.raw_decode(tweetString)
		return decodeTuple
	

	def getFiles(self):
		"""
		Load files from Settings.ROOT_DIR
		"""
		jsonFiles = []
		
		#walk the file directory
		for dirpath, dirnames, filenames in TwitterMiner.os.walk(Settings.ROOT_DIR):
			for f in filenames:
				file = TwitterMiner.os.path.join(dirpath, f)
				
				#only grab json files
				if (re.search(".json",file) != None):
					jsonFiles.append(file)
	
		return jsonFiles











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
		pprint.pprint(self.jsonFiles)


if __name__ == '__main__':
	miner = TwitterMiner()
	 
	 
	 
