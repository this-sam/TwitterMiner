#===============================================================================
#
# GenderFinder.py by Sam Brown
#
# The GenderFinder handles paring names with gender.  Using two separate lists of
# male and female first names, the GenderFinder will return M/F/U for male, female,
# and unknown names.
#
#===============================================================================

class GenderFinder(object):
	
	global Settings
	from Settings import Settings
	
	_instance = None
	def __new__(cls, *args, **kwargs):
		"""Overwrite the __new__ function to create a singleton object."""
		#override the new method to use as a singleton
		if not cls._instance:
			cls._instance = super(GenderFinder, cls).__new__(
								  cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		"""Loads male/female name lists, cleans the lists and builds hash tables for quick lookup."""
		#load names
		self.maleNames = open(Settings.MALE_FILE, 'r').readlines()
		self.femaleNames = open(Settings.FEMALE_FILE, 'r').readlines()
		
		#clean them up
		for i in range(len(self.maleNames)):
			self.maleNames[i] = self.maleNames[i].strip()
		
		for i in range(len(self.femaleNames)):
			self.femaleNames[i] = self.femaleNames[i].strip()
		
		#load the names into hash table into memory
		self.maleHash = self.__generateHashTable(self.maleNames)
		self.femaleHash = self.__generateHashTable(self.femaleNames)
		
	
	def lookupGender(self, name):
		"""Determine which gender a name belongs to.  Return M for male, F for female and U for undetermined."""
		
		#if it's too short to look up, don't bother
		if len(name)<2:
			return 'U'

		kOuter = name[0].upper()
		kInner = name[1].upper()

		#first check male list
		isMale = False

		#read through only the necessary lines
		startLoc, endLoc = self.__getSearchRange(kOuter, kInner, self.maleHash)
		if Settings.DEBUG:
			print name,":",
		for mName in self.maleNames[startLoc:endLoc+1]:
			if Settings.DEBUG:
				print mName,
			if name.upper() == mName:
				isMale = True
				if Settings.DEBUG:
					print "\n---------------------->It's a BOY!"
				break

		#now check the female list
		isFemale = False
		#read through only the necessary lines
		if Settings.DEBUG:
			print name, ":",
		startLoc, endLoc = self.__getSearchRange(kOuter, kInner, self.femaleHash)
		for fName in self.femaleNames[startLoc:endLoc+1]:
			if Settings.DEBUG:
				print fName,
			if name.upper() == fName:
				isFemale = True
				if Settings.DEBUG:
					print "\n---------------------->It's a GIRL!"
				break

		if isMale and not isFemale:
			return 'M'
		elif isFemale and not isMale:
			return 'F'
		else:
			return 'U'


	def __generateHashTable(self, words):
		"""Generates a 3-layer hash table from a SORTED list of words."""
		hash = {}
		for i in range(len(words)):
			#if you're not 2 letters long, i don't care about you.
			if len(words[i]) < 2:
				break
			
			#use the first two letters of each name to speed up lookups
			key = words[i][0:2]
			
			#build a hash table of char1-->char2-->index in array
			if key[0] not in hash:
				hash[key[0]] = {key[1]:i}
			elif key[1] not in hash[key[0]]:
				hash[key[0]][key[1]] = i
		
		return hash
	
	def __getSearchRange(self, kOuter, kInner, hashtable):
		"""Use the hash table to determine where in the names file a particular name might be located."""
		startLoc = -1
		if kOuter in hashtable and kInner in hashtable[kOuter]:
			startLoc = hashtable[kOuter][kInner]
		
		endLoc = -1
		if startLoc is not -1:
			#loop through to find the place to stop searching (the
			#alphabetically next entry in the hash table)
			
			#first don't go somewhere not on the table or past the alphabet
			while endLoc == -1 and ord(kOuter)<=90 and kOuter in hashtable:
				
				#step to next letter of the alphabet
				kInner = chr(ord(kInner)+1) 
				#continue stepping through the alphabet until either we found it
				#or we need to move on to the next outer level of the table
				while ord(kInner) <= 90 and kInner not in hashtable[kOuter]:
					kInner = chr(ord(kInner)+1)
					
				if kInner in hashtable[kOuter]:
					endLoc = hashtable[kOuter][kInner]
				else:
					kOuter = chr(ord(kOuter)+1)
					
		return (startLoc, endLoc)
	
if __name__ == '__main__':
	"""Testing main function. Demonstrates how object is to be used."""
	gf = GenderFinder()
	print gf.lookupGender("Sam")
	gf2 = GenderFinder
	print id(gf) == id(gf2)