#A message refers to an individual line from the final chat transcript.
#This constitutes either a finished, sent message or a message that was composed
#and then fully deleted.

class Message:
	
	global Settings, Event, datetime
	from Settings import Settings
	from Event import Event
	import datetime
	
	def __init__(self, events = []):
		if Settings.DEBUG:
			print "Initializing Object Message"
			
		self.events = events
		self.generateEventLookupTables()
	
		#INITIALIZE MESSAGE VARIABLES:#+ --> feature implemented, I=generated on init, L = gen later
		self.timeLastSent= ""			#+ timestamp of previously sent/deleted message (datetime)(L)
		self.timeStarted = ""			#+ timestamp of composition start (datetime)
		self.timeEnded	  = ""			#+ timestamp of message sent (datetime)
		
		self.compositionTime = -1 		#+ how long to write (timedelta)
		self.compositionDelay = -1		#+ how long after recieve previous (timedelta)(L)
		self.totalEvents = -1			#+ how many events went into this message
		self.sendDelay = -1				#+ how long did user wait before sending/deleting
		
		self.sent = False					#+ was this message ever actually sent?
		
		self.totalDeletions = -1		#+ how many times were things deleted
		self.totalDeletedChars = -1	#- how many total characters were deleted
		self.finalLength = -1			#+ final length of message before sent or no more insertions
		self.totalWords = -1				#+ number of words in message
		self.totalChars = -1				#+ number of letters/numerals (non whitespace chars)
		
		self.charsPerMin = -1			#+ characters per minute
		self.wordsPerMin = -1			#+ words per minute
		
		self.numPauses = -1				#- how many times the user paused for at least 1/2 second
		self.hasPunctuation = False	#- did the user use punctuation?
		
		self.hasTitleCase = False		#- did the user capitalize some words? (names, sentence start)
		self.hasCapsWord = False 		#- any words of all capitals?
		self.capsSegments = []			#- what chunks are all caps?
		self.capsRatio	= -1				#- ratio of capitalized to non-capitalized letters
		
		self.hasEmoticons = False		#- does this event contain emoticons?
		self.emoticons = []				#- array of emoticons used in this event
		
		#VARS SET BY USER CLASS
		self.userGender = ""				#+ gender of user
		
		
		self.featureVector = []			#- and the moment you've all been waiting for...
		self.allFeatures = ["sent","compositionTime", "compositionDelay", "totalEvents", "sendDelay", \
								  "totalDeletions", "finalLength", "totalWords", "totalChars",\
								  "charsPerMin", "wordsPerMin"]
								  #Added by USER class:
								  #GENDER
		
		
		#begin setting Message variables		
		self.timeStarted = self.events[0].timestampAsDatetime
		self.timeEnded = self.events[-1].timestampAsDatetime
		
		self.compositionTime = self.timeEnded - self.timeStarted
		self.totalEvents = len(events)
		self.sendDelay = self.getSendDelay()
		
		self.sent = self.events[-1].type == 'snd'
		
		self.totalDeletions = self.getTotalDeletions()
		self.finalLength = len(self.events[-1].text)
		self.totalWords = len(self.events[-1].text.split(" "))
		self.totalChars = len(self.events[-1].text.replace(" ",""))
		
		self.charsPerMin = self.getCharactersPerMinute()
		self.wordsPerMin = self.getWordsPerMinute()
		
		self.featureVector = self.selectFeatures(self.allFeatures)
	
		if Settings.DEBUG:
			self.__debug()

#---------------------------------------------
#Getter functions!
	def getCharactersPerMinute(self):
		if self.charsPerMin == -1 and self.compositionTime.seconds != 0:
			return self.totalChars/(self.compositionTime.seconds/60.0)
		else:
			return self.charsPerMin

	def getSendDelay(self):
		if self.sendDelay == -1:
			for i in range(len(self.events)-1, 0, -1):
				if self.events[i].text != self.events[-1].text:
					return self.events[-1].timestampAsDatetime - self.events[i].timestampAsDatetime
			return datetime.timedelta(seconds=0)
		else:
			return self.sendDelay
		
	def getTotalDeletions(self):
		if self.totalDeletions == -1:
			totalDeletions = 0
			if "bkb" in self.eventLookupTables:
				totalDeletions += len(self.eventLookupTables["bkb"])
			if "deb" in self.eventLookupTables:
				totalDeletions += len(self.eventLookupTables["deb"])
			return totalDeletions
		else:
			return self.totalDeletions
	
	def getWordsPerMinute(self):
		if self.wordsPerMin == -1 and self.compositionTime.seconds != 0:
			return self.totalWords/(self.convertTimedeltaToMinutes(self.compositionTime))
		else:
			return self.wordsPerMin
	
	def getFeatureSet(self):
		return self.allFeatures

	def selectFeatures(self, features):
		"""for each feature in the features (list of strings which represent variable names
		within the class), select the variable and add it to a the feature vector."""
		featureVector = []
		for feature in features:
			#check types:
			if not hasattr(self, feature):
				raise Exception("Message does not have feature "+feature)

			if type(vars(self)[feature]) == datetime.timedelta:
				seconds, microseconds = vars(self)[feature].seconds, vars(self)[feature].microseconds
				seconds += microseconds/1000000.
				featureVector.append(seconds)
			else:
				featureVector.append(vars(self)[feature])
				
		self.lastFeatureSet = features
		return featureVector
	

#---------------------------------------------
#Setter functions!
	def addEvent(self, event):
		self.events.append(event)
		
		
	def addEventFromString(self, eventString):
		e = Event(eventString)
		self.events.append(event)
		
		
	def addFeature(self, featureName, featureValue):
		vars(self)[featureName] = featureValue
		self.allFeatures.append(featureName)
		self.featureVector.append(featureValue)
		
		
	def generateEventLookupTables(self):
			self.eventLookupTables = {}
			#prepare eventLookupTables with defined event types
			for type in Settings.EVENT_TYPES:
				self.eventLookupTables[type] = []
			
			#create the arrays in the lookupTable
			for i in range(len(self.events)):
				self.eventLookupTables[self.events[i].type].append(i)
				
			
	def setTimeLastSent(self, timeLastSent):
		self.timeLastSent = timeLastSent
		self.compositionDelay = self.timeStarted - self.timeLastSent
		
		
	def sortEvents(self):
		self.events.sort()
		
#---------------------------------------------
#Misc functions!
	def convertTimedeltaToMinutes(self, delta):
		seconds = delta.seconds+delta.microseconds/1000000.0
		return seconds/60.0

	def __debug(self):
		print "Dumping Object Message"
		