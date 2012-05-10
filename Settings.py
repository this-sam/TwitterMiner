#===============================================================================
#
# Settings.py by Sam Brown
#
# Settings controls all global attributes that must be set for TwitterMiner to
# function properly.
#
#===============================================================================
class Settings:
     DEBUG = False 
     
     #----------File Location Constants----------
     ROOT_DIR = "/home/sam/Development/TwitterMiner/Tweets"
     
     #calculate where this file is from the directory of tweets
     SELF_DIR = ROOT_DIR.rsplit("/",1)[0]+"/"
     
     #male/female name lists
     MALE_FILE = SELF_DIR+"Resources/finalMale.txt"
     FEMALE_FILE = SELF_DIR+"Resources/finalFemale.txt"
     
     #--------Tweet Feature Vector Constants-----------
     ALL_FEATURES = ["numChars", "numDigits", "numWords", "avgWordLen", "hasPunctuation", "capsRatio",\
					 "totalEntities", "hasHashtags", "totalHashtags", "hasURLs", "totalURLs",\
					 "hasUserMentions", "totalUserMentions", "wasRetweeted", "isRetweet",\
                     "numPunctuation", "gender", "wordsLenLong"]
     
     LONGEST_WORD_LENGTH = 10
     
     #add the word counts to the feature vector
     for i in range(1, LONGEST_WORD_LENGTH+1):
          ALL_FEATURES.append("wordsLen"+str(i))
          ALL_FEATURES.append("ratioWordsLen"+str(i))