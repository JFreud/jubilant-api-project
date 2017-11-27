import sqlite3, json

def createTable():
	f="data/songs.db"
	db=sqlite3.connect(f)
	c=db.cursor()
	command = "CREATE TABLE IF NOT EXISTS login (username TEXT, password TEXT);"   #creates users table if it doesnt exist
	c.execute(command)
	command = "CREATE TABLE IF NOT EXISTS userSongs(username TEXT, lastFMuser TEXT, tone TEXT, artist TEXT, song TEXT, url TEXT );"  #creates posts table if it doesnt exist
	c.execute(command)
	db.commit()
	db.close()       #closes and commits changes

def insertIntoLoginTable(userStr,passwordStr):
	f="data/songs.db"
	db=sqlite3.connect(f)         #connects to Datebase to allow editing
	c=db.cursor()
	command = "INSERT INTO login VALUES('%s','%s');"%(userStr,passwordStr)
	c.execute(command)
	db.commit()
	db.close()

def removeSpecialChar(theString): 
	charThatBreakDB = "'" + '"' + '!?#,.' 
	outStr ="" 
	charList=list(theString) 
	for character in charList: 
		if not(character in charThatBreakDB): 
			outStr += character 
	return outStr
	
def insertIntoUserSongs(userStr,lastFMStr,apiDict):
	f="data/songs.db"
	db=sqlite3.connect(f)
	c=db.cursor()
	for entry in apiDict:
		toneStr= str(entry['tones']).strip('[]').replace("'","").replace("u","")
		nameStr = removeSpecialChar(entry['dL_name'])
		artistStr = removeSpecialChar(entry['dL_artist'])
		command = "INSERT INTO userSongs VALUES('%s','%s','%s','%s','%s','%s');"%(userStr,lastFMStr,toneStr,artistStr, nameStr,entry['url'])
		c.execute(command)
	db.commit()
	db.close()

def isStringInTableCol(searchString,table,column):
		f="data/songs.db"
		db=sqlite3.connect(f)
		c=db.cursor()
		command= "SELECT " + column + " FROM " +  table + ";"
		colData=c.execute(command)
		for entry in colData:
			for deeperEntry in entry:
				if searchString==deeperEntry:
					db.commit()
					db.close()
					return True
		db.commit()
		db.close()					
		return False

def isMatchUserAndPass(username,password):
		f="data/songs.db"
		db=sqlite3.connect(f)
		c=db.cursor()
		command = 'SELECT password FROM login WHERE username="' + username + '";'
		dbData=c.execute(command)
		try:
			for entry in dbData:
				if entry[0]==password:
					db.commit()
					db.close()
					return True
		except:
			pass
		db.commit()
		db.close()
		return False

def songsWithMatchingTone(username,lastFM,theTone):
		f="data/songs.db"
		db=sqlite3.connect(f)
		c=db.cursor()
		command="SELECT tone, artist, song, url FROM userSongs WHERE username = '%s' AND lastFMuser = '%s';"%(username, lastFM)
		c.execute(command)
		resultantList = c.fetchall()
		parentRetList=[]
		childRetDict={}
		for entry in resultantList:
			if theTone in entry[0]:
				childRetDict['artist']=entry[1]
				childRetDict['song']=entry[2]
				childRetDict['url']=entry[3]
				parentRetList.append(childRetDict)
				childRetDict={}
		return parentRetList
		