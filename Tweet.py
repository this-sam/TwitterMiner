class Tweet(object):
	
	global Settings, datetime, string, pprint, re
	from Settings import Settings
	import datetime, pprint, re
	
	def __init__(self, tweetDict):
		if Settings.DEBUG == True:
			pprint.pprint(tweetDict)
		
		#INITIALIZE tweet VARIABLES:	#+ --> feature implemented
		#    (just to list 'em all in one place)
				
		self.timestamp = ""				#+ timestamp of when tweet took place
		self.timestampAsDatetime = -1	#+ save the timestamp as a python datetime object
		
		#text variables
		self.text = ""					#+ text from tweet
		self.xText = ""				 	#+ converted (x'ed out text)
		self.isEmpty = False			#+ is there text?
		self.length = -1				#+ total length of text
		#chars and words are not very smartly implemented.
		self.numChars = -1				#+ total alpha characters in tweet
		self.numDigits = -1			#- total numeric characters in tweet
		self.numWords = -1				#+ total number of "words" (sep by spaces)
		self.avgWordLen = -1			#+ average length of words (no punctuation)
		self.isValid = False			#+in english? (drop any containing unicode
										# which can't be translated into ascii)
		
		self.hasPunctuation = False		#+ boolean has punctuation (yes/no)
		self.numPunctuation = -1		#+ how many punctuation characters?
		self.punctuation = []			#+ array containing all punctuation, in order
		
		self.hasTitleCase = False		#- any capital letters starting words?  (proper nouns, start of sentence... etc.)
		self.hasCapsWord  = False		#- any words of all capitals?
		self.capsSegments = []			#- array of sections of text that are all caps (punctuation included)
		self.capsRatio	  = -1			#+ ratio of capitalized to non-capitalized letters
		
		self.hasEmoticons = False		#- does this tweet contain emoticons?
		self.emoticons = []				#- array of emoticons used in this tweet
		
		#twitter elements
		self.totalEntities = -1  		#- entities are hashtags, urls & mentions
		self.hasHashtags = False		#+ does the tweet use hash tags?
		self.hashtags = []				#- array of hashtag items from tweet
		self.totalHashtags = -1 		#+ 
		self.urls = []					#-
		self.totalURLs	= -1 			#+
		self.hasURLs = False			#+
		self.userMentions = []			#-
		self.totalUserMentions = -1 	#+
		self.hasUserMentions = False	#+
		self.source	= ""				#-
		self.mobileSource = False		#-
		self.isRetweet = False			#+ what type of tweet ()
		self.wasRetweeted = False 		#+ was it retweeted
		self.retweetCount = -1			#+ hw many people retweeted it?
		
		#geo
		self.geo = ""					#-
		self.hasGeo = False				#-
		self.source = ""				#-
		
		#user
		self.name = ""					#-
		self.screenname = ""			#-
		self.created_at = ""			#-
		self.hasProfImage = False		#-
		self.hasBackgroundImage = False #-
		self.followersCount = -1 		#-
		self.favoritesCount = -1 		#-
		self.friendsCount = -1 			#-
		self.followingCount = -1 		#-
		self.hasDescription = False		#-
		self.statusesCount = -1 		#-
		
		self.featureVector = []			#+ and the moment you've all been waiting for...
		self.allFeatures = Settings.ALL_FEATURES
		
		
		#================================
		#begin to set tweet attributes
		self.text = self.__unicodeToString(tweetDict["text"])
		self.name = self.__unicodeToString(tweetDict["user"]["name"])
		self.isValid = self.text is not "" and\
					   self.name is not "" and\
					   re.search(",", self.name) is None and\
					   re.search("\n", self.name) is None


		#for now, if text can't be converted from unicode, ditch it.		
		if not self.isValid:
			return
		
		self.xText = self.__xOutText(self.text)		
		
		#Some twitter info:
		self.isRetweet = tweetDict["in_reply_to_screen_name"] == None
		self.numRetweets = tweetDict["retweet_count"]
		self.wasRetweeted = self.numRetweets > 0
		self.timestamp = tweetDict["created_at"]

		#Some text info
		self.length = len(self.text)
		words = self.__getWords(self.xText)
		
		self.numChars = self.__getNumChars(words)
		self.numWords = self.__getNumWords(words)
		self.numDigits = self.__getNumNumbers(self.xText)
		if self.numWords != 0:
			self.avgWordLen = self.numChars/self.numWords
		else:
			self.avgWordLen = 0
			
		if self.numChars != 0:
			self.capsRatio = self.__getCapsCount(words)/float(self.numChars)
		else:
			self.capsRatio = 0
			
		self.punctuation = self.__getPunctuation(self.xText)
		self.hasPunctuation = len(self.punctuation) != 0
		self.numPunctuation = len(self.punctuation)

		#twitter content info:
		self.totalHashtags = len(tweetDict["entities"]["hashtags"])
		self.hasHashtags = self.totalHashtags > 0
		self.totalURLs = len(tweetDict["entities"]["urls"])
		self.hasURLs = self.totalURLs > 0
		self.totalUserMentions = len(tweetDict["entities"]["user_mentions"])
		self.hasUserMentions = 	self.totalUserMentions > 0
		self.totalEntities = sum([self.totalURLs, self.totalUserMentions, self.totalHashtags])
		
		self.featureVector = self.selectFeatures(self.allFeatures)
		
		if Settings.DEBUG:
			self.__debug()
		#end constructor
	
	#====================================================
	#    PUBLIC FUNCTIONS
	def addFeature(self, featureName, featureValue):
		vars(self)[featureName] = featureValue
		self.allFeatures.append(featureName)
		self.featureVector.append(featureValue)
	
	def getFeatureSet(self):
		return self.allFeatures
	
	def getFeatureVector(self):
		if len(self.featureVector) == 0:
			self.featureVector = self.selectFeatures(self.allFeatures)
		return self.featureVector
	
	def selectFeatures(self, features):
		"""for each feature in the features (list of strings which represent variable names
		within the class), select the variable and add it to a the feature vector."""
		featureVector = []
		for feature in features:
			#check types:
			if not hasattr(self, feature):
				raise Exception("Tweet does not have feature "+feature)

			if type(vars(self)[feature]) == datetime.timedelta:
				seconds, microseconds = vars(self)[feature].seconds, vars(self)[feature].microseconds
				seconds += microseconds/1000000.
				featureVector.append(seconds)
			else:
				featureVector.append(vars(self)[feature])
				
		self.lastFeatureSet = features
		return featureVector
	
		
	#====================================================
	#    PRIVATE FUNCTIONS	
	def __getCapsCount(self, words):
		count = 0
		for word in words:
			for char in word:
				if char.isupper():
					count += 1
		return count
		

	def __getNumChars(self, words):
		count = 0
		for word in words:
			count += len(word)
		return count

	def __getNumNumbers(self, xText):
		count = 0
		for char in xText:
			if char.isdigit():
				count += 1
		return count

	def __getNumWords(self, words):
		return len(words)
	
			
	def __getPunctuation(self, text):
		punctuation = []
		for char in text:
			if not char.isalnum() and char != " ":
				punctuation.append(char)
		return punctuation
	
	def __getWords(self, text):
		#return all strings containing at least 1 letter
		#strip punctuation?
		sText = text.split(" ")
		chunks = []
		
		#find all individual elements which contain alpha characters
		for word in sText:
			isWord = False
			for char in word:
				if char.isalpha():
					isWord = True
			if isWord:
				chunks.append(word)
		
		words = []
		#now remove punctuation, split up two words concatenated by punctuation
		for word in chunks:
			#locate all punctuation within the chunk
			punc = re.split("[A-Za-z0-9]*", word)
			
			#chop out the punctuation, replacing it with spaces
			newWord = word
			for p in punc:
				if p is not "":
					newWord = newWord.replace(p, " ")
			
			#split the chunk into all possible words, also trims whitespace created by punctuation
			newWords = newWord.split(" ")
			
			#only add words to the list
			for newWord in newWords:
				if newWord is not "":
					words.append(newWord)
			
		return words
			
				
			
	def __unicodeToString(self, uni):
		"""UnicodeToString:
			Takes a unicode type object and attempts
			to convert it to an ascii string.
		"""
		try:
			text = str(uni)
		except UnicodeEncodeError:
			if Settings.DEBUG:
				print "Could not decode tweet text from unicode."
			return ""
		else:
			if Settings.DEBUG:
				print "Tweet successfully decoded:"
				print text
			return text	
			
			
	def __xOutText(self, text):
		xText = ""
		for char in text:
			if char.isalpha() and char.isupper():
				xText += 'X'
			elif char.isalpha():
				xText += 'x'
			else:
				xText += char
		return xText
			
			
	
			
			
			
			
			
			
			
#====================================================
#------------LEFTOVERS FROM EVENT ---------------
#---------------------------------------------
#Getter functions!
#getters will either calculate a value, or return the calculated
#value if the field has already been calculated.
	
	def getAvgWordLength(self):
		s = self.text
		s = s.lower()
		ct = s.count('x')
		numWords = getNumWords()
		avgWordLength = ct/numWords

	def getEmoticons(self):
		pass
	
	def getLength(self):
		pass


		

	
	def getPunctuation(self):
		pass
	
	def getSentenceType(self):
		#exclamation, question, response, incomplete? ==> research
		pass
	
	def convertTimestamp(self, timestamp):
		splitTimestamp = timestamp.split(" ")
		date = splitTimestamp[0]
		time = splitTimestamp[1]
		
		splitDate = date.split("-")
		year, month, day = int(splitDate[0]), int(splitDate[1]), int(splitDate[2])
		
		splitTime = time.split(":")
		hours, minutes = int(splitTime[0]), int(splitTime[1])
		seconds, miliseconds = int(splitTime[2].split(".")[0]), int(splitTime[2].split(".")[1])
		
		convertedTimestamp = datetime(year, month, day, hours, minutes, seconds, miliseconds*1000)
		return convertedTimestamp
	
	
	def __debug(self):
		print "Dumping Object Tweet"
		pprint.pprint(self.__dict__)
		
if __name__ == '__main__':
	pass
	#string = "A_01_4_02, 2011-09-29 21:37:28.291, snd, xxx x xxxxx xxx xxxxxxxx"
	#tweet = Tweet(string)
	
	

