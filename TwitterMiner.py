#===============================================================================
#
# TwitterMiner.py by Sam Brown
#
# This class serves as the "driver" for the Twitter feature extraction process.
# Parses through all .json files in a directory (specified in Settings.py) and
# outputs all that meet the selection criteria into Features.csv.  Also handles
# matching tweets with gender through the GenderFinder class.
#
#===============================================================================

class TwitterMiner(object):
	
	global re, pprint
	import os, pprint, re
	
	global json
	import simplejson as json
	
	global Tweet, Settings, GenderFinder
	from Tweet import Tweet
	from Settings import Settings
	from GenderFinder import GenderFinder
	
	def __init__(self):
		"""Load json decoder, find all input files"""
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
		"""Load files from Settings.ROOT_DIR"""
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
		"""Turn a string in JSON format (line in the .json file) into a python dictionary."""
		try:
			decodeTuple = self.decoder.raw_decode(tweetString)
		except json.decoder.JSONDecodeError:
			if Settings.DEBUG:
				print "This tweet broke it:",
				pprint.pprint(tweetString)
		else:
			return decodeTuple
		return ({}, 0)
	
	def mineTweets(self):
		"""Parses through tweets and writes them to an output file one at a time.
		
		Notes: Could be sped up through use of an output buffer, but watch out
		for memory overhead.
		"""
		#for matching gender, dontcha know
		genderFinder = GenderFinder()
		
		#tweets contained in self.jsonFiles[0]
		
		fOut = open("Features.csv", 'w')
		self.__writeLine(fOut, Settings.ALL_FEATURES)
		
		print "TweetMiner\nMining..."
		tweetCount = 0
		#loop through each file
		for jFile in self.jsonFiles:
			fIn = open(jFile, 'r')
			#loop through tweets
			for line in fIn.readlines():
				line = unicode(line)
				tweetDict, line = self.getTweetDict(line)
				#make sure it's an actual tweet, and in english
				tweet = self.__makeTweet(tweetDict, genderFinder)
				if tweet != False and tweet.isValid:
					tweetCount += 1
					self.__writeLine(fOut, tweet.getFeatureVector())
			fIn.close()
		fOut.close()
		
						
	#==========================================
	# Private Functions

	def __makeTweet(self, tweetDict, genderFinder):
		"""Creates a Tweet object from a dictionary.  Requires the genderFinder object
		so that each Tweet can be matched to a gender."""
		if "user" in tweetDict:
			if tweetDict["user"]["lang"] == "en":
				tweet = Tweet(tweetDict, genderFinder)
				return tweet
		return False

	def __writeLine(self, fHandle, array):
		"""Writes a comma-separated line to a file from an array."""
		row = ""
		if Settings.DEBUG:
			print "Writeline: " + str(array[0]) + ":"+str(array[-1])
		for element in array:
			row+=str(element)+","
		fHandle.write(row[0:-1]+"\r\n")

	def __debug(self):
		"""Print all TwitterMiner variables."""
		print "Dumping Object TwitterMiner"
		pprint.pprint(self.jsonFiles)

if __name__ == '__main__':
	miner = TwitterMiner()
	miner.mineTweets()
	 
	 
	 
