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
		

		
		if Settings.DEBUG:
			self.__debug()

	#==========================================
	# Public Functions
	
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

	def getTweetDict(self, tweetString):
		try:
			decodeTuple = self.decoder.raw_decode(tweetString)
		except json.decoder.JSONDecodeError:
			if Settings.DEBUG:
				print "This tweet broke it."
				pprint.pprint(tweetString)
		else:
			return decodeTuple
		return ({}, 0)
	
	def mineTweets(self):
		#tweets contained in self.jsonFiles[0]
		
		fOut = open("Features.csv", 'w')
		self.__writeLine(fOut, Settings.ALL_FEATURES)
		
		for jFile in self.jsonFiles:
			fIn = open(jFile, 'r')
			#loop through tweets
			for line in fIn.readlines():
				line = unicode(line)
				tweetDict, line = self.getTweetDict(line)
				#make sure it's an actual tweet, and in english
				tweet = self.__makeTweet(tweetDict)
				if tweet != False and tweet.isValid:
					self.__writeLine(fOut, tweet.getFeatureVector())
			fIn.close()
		fOut.close()
		
						
	#==========================================
	# Private Functions

	def __makeTweet(self, tweetDict):
		if "user" in tweetDict:
			if tweetDict["user"]["lang"] == "en":
				tweet = Tweet(tweetDict)
				return tweet
		return False

	def __writeLine(self, fHandle, array):
		row = ""
		for element in array:
			row+=str(element)+","
		fHandle.write(row+"\r\n")









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
	miner.mineTweets()
	 
	 
	 
