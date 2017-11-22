import sqlite3

def createTable():
	f="data/songs.db"
	db=sqlite3.connect(f)
	c=db.cursor()
	command = "CREATE TABLE IF NOT EXISTS login (username TEXT, password TEXT);"   #creates users table if it doesnt exist
	c.execute(command)
	command = "CREATE TABLE IF NOT EXISTS userSongs(username TEXT, lastFM TEXT, tone TEXT, playlists BLOB );"  #creates posts table if it doesnt exist
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

def inserIntoUserSongs(userStr,lastFMStr,toneStr,playlistStr):
	f="data/songs.db"
	db=sqlite3.connect(f)
	c=db.cursor()
	command= "INSERT INTO userSongs VALUES('%s','%s','%s','%s');"%(userStr,lastFMStr,toneStr,playlistStr)
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
                        return True
        return False
