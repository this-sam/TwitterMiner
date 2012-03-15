#ettings file: contains all global settings

class Settings:
     DEBUG = False 
     
     #----------File Location Constants----------
     #ROOT_DIR = "/home/sam/Development/TwitterMiner/Tweets"
     #mac
     #ROOT_DIR = "/Volumes/Macintosh HD 2/Development/Thesis/Twitter/Tweets"
     #uvm srvr
     ROOT_DIR = '/users/s/b/sbbrown/Development/Thesis/TwitterMiner/'
     #CsCrew Mac
     #ROOT_DIR = '/Users/cscrew/Thesis/Files/'
     #PC
     #ROOT_DIR = "E:\\Development\\Thesis\\Twitter\\Tweets\\"
     
     #calculate where this file is from the directory of tweets
     SELF_DIR = ROOT_DIR.rsplit("/",1)[0]+"/"
     
     #male/female name lists
     MALE_FILE = SELF_DIR+"Resources/finalMale.txt"
     FEMALE_FILE = SELF_DIR+"Resources/finalFemale.txt"    