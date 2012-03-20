#Many types of events are contained during a conversation.  This class makes it
#easier to determine which type of event, etc.

class Tweet:
	
	global Settings, datetime, string
	from Settings import Settings
	from datetime import datetime

	
	def __init__(self, rawString):
		self.rawString = rawString
		splitString = self.rawString.split(',', 5)
		
		#INITIALIZE EVENT VARIABLES:	#+ --> feature implemented
		self.type = ""						#+ what type of event (list in Settings.py)
		self.username = ""				#+ username of person who caused event
		self.text = ""						#+ text in text box during event
		self.timestamp = ""				#+ timestamp of when event took place
		
		self.timestampAsDatetime = -1	#+ save the timestamp as a python datetime object
		
		self.isEmpty = False				#+ is there text?
		self.length = -1					#+ total length of text
		self.numChars = -1				#+ total characters in text box during event
		self.numWords = -1				#+ total number of "words" (sep by spaces)
		self.avgWordLen = -1				#+ average length of words (no punctuation)
		
		self.hasPunctuation = False	#- boolean has punctuation (yes/no)
		self.punctuation = []			#- array containing all punctuation, in order
		
		self.hasTitleCase = False		#- any capital letters starting words?  (proper nouns, start of sentence... etc.)
		self.hasCapsWord	= False		#- any words of all capitals?
		self.capsSegments = []			#- array of sections of text that are all caps (punctuation included)
		self.capsRatio	= -1				#- ratio of capitalized to non-capitalized letters
		
		self.hasEmoticons = False		#- does this event contain emoticons?
		self.emoticons = []				#- array of emoticons used in this event
		
		#begin to set event attributes
		self.username = splitString[0].strip()
		self.timestamp = splitString[1].strip()
		self.type = splitString[2].strip()
		self.text = splitString[3].strip()
		
		self.timestampAsDatetime = self.convertTimestamp(self.timestamp)
		
		self.length = len(self.text)
		self.isEmpty = (self.length==0)
		if (self.isEmpty == False):
			self.numChars = self.getNumChars()
			self.numWords = self.getNumWords()
			if self.numWords != 0:
				self.avgWordLen = self.numChars/self.numWords
			else:
				self.avgWordLen = 0
			
		
		if Settings.DEBUG:
			self.__debug()


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

	def getNumChars(self):
		strippedText = self.text.replace(" ", "")
		return len(strippedText)
		
	def getNumWords(self):
		s = self.text
		s = s.lower()
		numWords = 0
		for substr in s.split(" "): #REPLACE WITH REGEX FOR PUNCTUATION AND SPACES
			ct = substr.count('x')
			if ct > 0:
				numWords += 1
		return numWords
	
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
		print self.rawString
		print "USER:\n\t"+self.username
		print "TYPE:\n\t"+self.type
		print "TEXT:\n\t"+self.text
		print "TIME:\n\t",self.timestampAsDatetime
		print "BOOLEANS:"
		print "\tisEmpty:", self.isEmpty
		print "CALCULATED:"
		print "\tnumChars:", self.numChars
		print "\tnumWords:", self.numWords
		print "\tavgWordLen:", self.avgWordLen
		
if __name__ == '__main__':
	
	string = "A_01_4_02, 2011-09-29 21:37:28.291, snd, xxx x xxxxx xxx xxxxxxxx"
	event = Tweet(string)
	
	

