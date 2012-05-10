#===============================================================================
#
# Tweet.py by Sam Brown
#
# An object represntation of each individual tweet.  This class handles all functions
# and calculations involved with turning tweets into feature vectors.
#
#===============================================================================

class Tweet(object):
	
	global Settings, GenderFinder
	from Settings import Settings
	from GenderFinder import GenderFinder
	
	global datetime, string, pprint, re
	import datetime, pprint, re
	
	def __init__(self, tweetDict, genderFinder = GenderFinder()):
		"""Initialize all tweet variables to default values, then set them."""
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
		
		self.numChars = -1				#+ total alpha characters in tweet
		self.numDigits = -1				#- total numeric characters in tweet
		self.numWords = -1				#+ total number of "words" (sep by spaces)
		self.avgWordLen = -1			#+ average length of words (no punctuation)
		self.isValid = False			#+in english? (drop any containing unicode
										# which can't be translated into ascii)
		
		self.hasPunctuation = False		#+ boolean has punctuation (yes/no)
		self.numPunctuation = -1		#+ how many punctuation characters?
		self.punctuation = []			#+ array containing all punctuation, in order
		
		self.capsRatio	  = -1			#+ ratio of capitalized to non-capitalized letters

		self.longestWordLength = 10		#count words of length 10 and under
		for i in range(1, Settings.LONGEST_WORD_LENGTH+1):
			vars(self)["wordsLen"+str(i)] = 0
			vars(self)["ratioWordsLen"+str(i)] = 0
		self.wordsLenLong = 0			#all words longer than longestWordLength
		
		#twitter elements
		self.hasHashtags = False		#+ does the tweet use hash tags?
		self.totalHashtags = -1 		#+ 
		self.totalURLs	= -1 			#+
		self.hasURLs = False			#+
		self.totalUserMentions = -1 	#+
		self.hasUserMentions = False	#+
		self.isRetweet = False			#+ what type of tweet ()
		self.wasRetweeted = False 		#+ was it retweeted
		self.retweetCount = -1			#+ hw many people retweeted it?
		
		#user
		self.name = ""					#+
		self.gender = 'U'				#+ M/F for male, female, U for unknown
		self.screenname = ""			#+
		
		self.featureVector = []			#+ and the moment you've all been waiting for...
		self.allFeatures = Settings.ALL_FEATURES
		
		#================================
		#begin to set tweet attributes
		self.text = self.__unicodeToString(tweetDict["text"])
		self.name = self.__unicodeToString(tweetDict["user"]["name"]).upper()
		self.gender = self.__getGenderFromName(self.name, genderFinder)
		self.isRetweet = tweetDict["in_reply_to_screen_name"] == None
		
		self.isValid = self.text is not "" and\
					   self.name is not "" and\
					   self.gender is not 'U' and\
					   re.search(",", self.name) is None and\
					   re.search("\n", self.name) is None and\
					   self.isRetweet == False

		#If the tweet does not meet all of the validation criteria, stop setting its values.	
		if not self.isValid:
			return
		
		#Create x'ed out text
		self.xText = self.__xOutText(self.text)		
		
		#Set some twitter info:
		self.numRetweets = tweetDict["retweet_count"]
		self.wasRetweeted = self.numRetweets > 0
		self.timestamp = tweetDict["created_at"]

		#Set some text info
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
			
		#get the count of words of each length
		self.__setWordLengthCounts(words)
		self.__setWordLengthRatios(words)
			
		#caluclate information about punctuation
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
		
		#last but not least, select those features!
		self.featureVector = self.selectFeatures(self.allFeatures)
		
		if Settings.DEBUG:
			print "Constructor:",self.name, self.gender
			print "Feature Vector:",self.featureVector[0], self.featureVector[-1]
		
		if Settings.DEBUG:
			self.__debug()
		#end constructor
	
	#====================================================
	#    PUBLIC FUNCTIONS
	def addFeature(self, featureName, featureValue):
		"""Creates a new local variable from string featureName with value featureValue.
		This local variable is automatically added to the current feature set and feature vector.
		"""
		vars(self)[featureName] = featureValue
		self.allFeatures.append(featureName)
		self.featureVector.append(featureValue)
	
	def getFeatureSet(self):
		"""Returns the set of all feature names for the Tweet object."""
		return self.allFeatures
	
	def getFeatureVector(self):
		"""Returns the set of all features (feature vector) for the Tweet object."""
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
				if Settings.DEBUG:
					print "SelectFeatures:", featureVector[0], featureVector[-1]
				
		self.lastFeatureSet = features
		return featureVector
	
		
	#====================================================
	#    PRIVATE FUNCTIONS	
	def __getCapsCount(self, words):
		"""Counts the number of capital letters in an array of words."""
		count = 0
		for word in words:
			for char in word:
				if char.isupper():
					count += 1
		return count
	
	def __getGenderFromName(self, name, genderFinder):
		"""Uses the GenderFinder object to match a twitter-user's name to their gender."""
		nameParts = re.split("[^A-Za-z]+", name)
		gender = genderFinder.lookupGender(nameParts[0])
		
		if Settings.DEBUG:
			print "\n__getGender...:",name, ":"+gender
		
		return gender


	def __getNumChars(self, words):
		"""Counts the number of characters contained in a list of words."""
		count = 0
		for word in words:
			count += len(word)
		return count

	def __getNumNumbers(self, xText):
		"""Counts the number of digits contained in a string."""
		count = 0
		for char in xText:
			if char.isdigit():
				count += 1
		return count

	def __getNumWords(self, words):
		"""Returns the number of words in an array of words."""
		return len(words)
	
			
	def __getPunctuation(self, text):
		"""Returns all punctuation contained in a given string."""
		punctuation = []
		for char in text:
			if not char.isalnum() and char != " ":
				punctuation.append(char)
		return punctuation
	
	def __getWords(self, text):
		"""Splits a string into words, removing any which don't contain alphabetical characters."""
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
	
	def __setWordLengthCounts(self, words):
		"""For each of he word lengths that we are counting, count how many words in the text are that length.  Set the values."""
		for word in words:
			length = len(word)
			if length <= Settings.LONGEST_WORD_LENGTH:
				vars(self)["wordsLen"+str(length)] += 1
			else:
				self.wordsLenLong += 1
				
	def __setWordLengthRatios(self, words):
		"""For each of he word lengths that we are counting, set the ratio of all words that that length makes up."""
		numWords = len(words)
		if numWords == 0:
			return None
		
		for i in range(1, Settings.LONGEST_WORD_LENGTH+1):
			wordCount = vars(self)["wordsLen"+str(i)]
			wordRatio = wordCount/(numWords*1.0)
			vars(self)["ratioWordsLen"+str(i)] = wordRatio
			
		
	def __unicodeToString(self, uni):
		"""Takes a unicode type object and attempts to convert it to an ascii string."""
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
		"""Takes a string of characters and "x'es" out alpha characters into x or X depending on case."""
		xText = ""
		for char in text:
			if char.isalpha() and char.isupper():
				xText += 'X'
			elif char.isalpha():
				xText += 'x'
			else:
				xText += char
		return xText
	
	def __debug(self):
		"""Prints all local variables."""
		print "Dumping Object Tweet"
		pprint.pprint(self.__dict__)
	
	

