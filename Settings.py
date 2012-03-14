#ettings file: contains all global settings

class Settings:
     DEBUG = False 
     
     #----------File Location Constants----------
     ROOT_DIR = "/home/sam/Development/TwitterMiner/Tweets"
     #mac
     #ROOT_DIR = "/Volumes/Macintosh HD 2/Development/Thesis/Twitter/Tweets"
     SELF_DIR = ROOT_DIR.rsplit("/",1)[0]+"/"
     #uvm srvr
     #ROOT_DIR = '/users/s/b/sbbrown/Development/Thesis/Chat/Files/'
     #CsCrew Mac
     #ROOT_DIR = '/Users/cscrew/Thesis/Files/'
     #PC
     #ROOT_DIR = "E:\\Development\\Thesis\\Twitter\\Tweets\\"
