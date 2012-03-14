class Tweet(object):
	
	global Settings, datetime, string, pprint
	from Settings import Settings
	import datetime, pprint
	
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
		self.numChars = -1				#+ total characters in tweet
		self.numWords = -1				#+ total number of "words" (sep by spaces)
		self.avgWordLen = -1			#+ average length of words (no punctuation)
		self.isValid = False			#+in english? (drop any containing unicode
										# which can't be translated into ascii)
		
		self.hasPunctuation = False		#+ boolean has punctuation (yes/no)
		self.punctuation = []			#+ array containing all punctuation, in order
		
		self.hasTitleCase = False		#- any capital letters starting words?  (proper nouns, start of sentence... etc.)
		self.hasCapsWord  = False		#- any words of all capitals?
		self.capsSegments = []			#- array of sections of text that are all caps (punctuation included)
		self.capsRatio	  = -1			#- ratio of capitalized to non-capitalized letters
		
		self.hasEmoticons = False		#- does this tweet contain emoticons?
		self.emoticons = []				#- array of emoticons used in this tweet
		
		#twitter elements
		self.totalEntities = -1  		#- entities are hashtags, urls & mentions
		self.hashtags = []				#- array of hashtag items from tweet
		self.totalHashtags = -1 		#-
		self.urls = []					#-
		self.totalURLs	= -1 			#-
		self.userMentions = []			#-
		self.totalUserMentions = -1 	#-
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
		
		##begin to set tweet attributes
		self.text = self.__unicodeToString(tweetDict["text"])
		self.isValid = self.text != ""

		#for now, if text can't be converted from unicode, ditch it.		
		if not self.isValid:
			return
		
		self.xText = self.__xOutText(self.text)
		print self.text
		print self.xText
	
		self.length = len(self.text)
		self.isRetweet = tweetDict["in_reply_to_screen_name"] == None
		self.numRetweets = tweetDict["retweet_count"]
		self.wasRetweeted = self.numRetweets > 0
		self.timestamp = tweetDict["created_at"]


		self.numChars = self.__getNumChars(self.xText)
		self.numWords = self.__getNumWords(self.xText)
		if self.numWords != 0:
			self.avgWordLen = self.numChars/self.numWords
		else:
			self.avgWordLen = 0
			
		self.punctuation = self.__getPunctuation(self.xText)
		self.hasPunctuation = len(self.punctuation) == 0
		
		if Settings.DEBUG:
			self.__debug()
			
		self.__debug()
		
		
		

	def __getNumChars(self, text):
		strippedText = text.replace(" ", "")
		return len(strippedText)


	def __getNumWords(self, text):
		s = text
		s = s.lower()
		numWords = 0
		for substr in s.split(" "): #REPLACE WITH REGEX FOR PUNCTUATION AND SPACES
			ct = substr.count('x')
			if ct > 0:
				numWords += 1
		return numWords
	
			
	def __getPunctuation(self, text):
		punctuation = []
		for char in text:
			if not char.isalnum:
				punctuation.append(char)
		return punctuation
				
			
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
	
	

