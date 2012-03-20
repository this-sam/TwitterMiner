class GenderFinder(object):
	
	global Settings
	from Settings import Settings
	
	def __init__(self):
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
		"""Determine which gender a name belongs to.  Return M for male, F for
		female and U for undetermined."""
		
		#if it's too short to look up, don't bother
		if len(name)<2:
			return 'U'
		
		key1 = name[0].upper()
		key2 = name[1].upper()
		
		#first check male list
		isMale = False
		startLoc = -1
		if key2 in self.maleHash[key1]:
			startLoc = self.maleHash[key1][key2]
		
		if startLoc is not -1:
			for key, val in self.maleHash[key1].iteritems():
				print key, val
			
		
		#now check the female list
		isFemale = False
		
		if isMale and not isFemale:
			return 'M'
		elif isFemale and not isMale:
			return 'F'
		else:
			return 'U'
		
	
	def __generateHashTable(self, words):
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
				
	
if __name__ == '__main__':
	gf = GenderFinder()
	print gf.lookupGender("Ellen")