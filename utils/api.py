#from flask import Flask, render_template
import requests, json

#==============================================================================
# - should add way of getting youtube embeded video links from youtube api
#     url = "https://gdata.youtube.com/feeds/api/videos?q=SEARCH_QUERY&key=YOUR_API_KEY&orderby=viewCount&max-results=50&v=2&alt=json"

#     url = "https://gdata.youtube.com/feeds/api/videos?q=SEARCH_QUERY&key=AIzaSyATP2BxeFJ1vx1o9k-48pLcBcAMopDf3PY&orderby=viewCount&max-results=1&v=3&alt=json"
#==============================================================================

#henry zheng account

key_obj = open("keys.txt")
keys = key_obj.readline().replace("\n", "").split(",")
key_obj.close()
#print keys
LASTFM_KEY = keys[0]
MUSIXMATCH_KEY = keys[1]
WATSON_KEY = keys[2]
YOUTUBE_KEY = keys[3]


def get_songs(user):
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=" + user + "&api_key=%s&format=json" % (LASTFM_KEY)
    lastfm = requests.get(url)

    dL = json.loads(lastfm.text)
    try:
    	dL_lovedtracks = dL['lovedtracks']
    except:
    	return []
    dL_track = dL_lovedtracks['track']
    retList = []

    #print r.text

    for track in dL_track:
        dict = {}
        dict['dL_name'] = track['name']
        dict['dL_artist'] = track['artist']['name']

        #print dict
        retList.append(dict)

    return retList


#api_base = "http://api.musixmatch.com/ws/1.1/{0}?{1}&apikey=7169e60f579305a0c080332a16b41537"#formatting strings for the command and parameters

def get_song_id(track, artist):
	api_base = "http://api.musixmatch.com/ws/1.1/{0}?{1}&apikey=" + MUSIXMATCH_KEY#formatting strings for the command and parameters
	try: #accounts for the occasional foreign character
		url = api_base.format("track.search", "q_track={0}&q_artist={1}&page_size=5&page=1&s_track_rating=desc".format(track.replace(" ", "%20"), artist.replace(" ", "%20")))
	except:
		return None
	msg = requests.get(url)
	search_dict = json.loads(msg.text)
	if search_dict["message"]["body"]["track_list"] == []:
		return None
	return search_dict["message"]["body"]["track_list"][0]["track"]["track_id"]

def get_lyrics(track_id):
	api_base = "http://api.musixmatch.com/ws/1.1/{0}?{1}&apikey=" + MUSIXMATCH_KEY#formatting strings for the command and parameters
	url = api_base.format("track.lyrics.get","track_id={}".format(track_id))
	msg = requests.get(url)
	lyrics_dict = json.loads(msg.text)
	if lyrics_dict["message"]["body"] == []:
		return None
	body = lyrics_dict["message"]["body"]["lyrics"]["lyrics_body"]
    #body.split("*")
    #print body


	if body == "":
		return None
	else:
		return body


#user_info = "rj"
#print get_songs(user_info)


def get_lyrics_all(user):
	user_info = user
	retList = get_songs(user_info)
	for song in retList:
		lyrics = get_lyrics(get_song_id(song['dL_name'], song['dL_artist']))
		song['lyrics'] = lyrics

	i = 0
	while (i < len(retList)):
		if retList[i]['lyrics'] is None:#iterates through list and if no lyrics removes it; does not increment because it moves to next automatically through deletion
			del retList[i]
		else:
			retList[i]['lyrics'] = retList[i]['lyrics'].split("*")[0]
			#print retList[i]['lyrics']
			i += 1

	return retList

#print get_lyrics_all()
#print get_lyrics_all()[0]

'''
song_id = get_song_id(dL_name, dL_artist)
print song_id
print get_lyrics(song_id)
lyrics = get_lyrics(song_id)
'''

#sd8.Watson

#sasha fomina account
# Returns the json for analysis of a single string of any length
def analyze_single(text):
	#url = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21&sentences=false&text=' + urllib2.quote(text.encode('utf-8'))
	url = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21&sentences=false&text=' + text
	#req = requests.get(url, auth=('1040bc05-8ffa-4577-a465-43d95b55737d', '0xvV0yqEOsyy'))
	req = requests.get(url, auth=('9ce3e140-1d9f-44f7-8f6f-0ea156d8eacc',WATSON_KEY))
	json = req.json()
	#print json
	tones = json['document_tone']['tones']
	tonesList = []
	for tone in tones:
		#print tone
		tone_name = tone['tone_name']
		if tone_name is not 'None':
			#print tone_name
			tonesList.append(tone_name)
	return tonesList

def analyze_all(user):
    retList = get_lyrics_all(user)
    for song in retList:
        song['tones'] = analyze_single(song['lyrics'])
    i = 0
    while (i < len(retList)):
        if retList[i]['tones'] == []:#iterates through list and if no tones removes it; does not increment because it moves to next automatically through deletion
            del retList[i]
        else:
            i += 1

    return retList

#print analyze_all()

def get_tone(tone):
    allList = analyze_all()
    #print allList
    retList = []
    for song in allList:
        #print song['dL_name']
        #print song['tones']
        if tone in song['tones']:
            #print "***"
            retList.append(song)
    #print len(retList)
    return retList

#print len(get_tone('Anger'))
#print len(get_tone('Disgust'))
#print len(get_tone('Fear'))
#print len(get_tone('Joy'))
#print len(get_tone('Sadness'))

#print len(get_tone('Analytical'))
#print len(get_tone('Confident'))
#print len(get_tone('Tentative'))

#jeromes account
def get_youtube_url(song_dict):
	artist = song_dict['dL_artist'].replace(" ", "+")#replace spaces in query with +
	title = song_dict["dL_name"].replace(" ", "+")
	query = artist + "+" + title
	url = "https://www.googleapis.com/youtube/v3/search?key=%s&part=snippet&q=%s" % (YOUTUBE_KEY, query)#builds url
	response = requests.get(url)
	results_dict = json.loads(response.text)#creates dict of response
	try:
		video_id = results_dict['items'][0]['id']['videoId']#extracts video query id from the dict
		return "https://www.youtube.com/watch?v=" + video_id
	except:
		pass
		return "https://www.youtube.com/watch?v=aDm5WZ3QiIE"


def buildDictForDB(user):
	allList=analyze_all(user)
	for songData in allList:
		songData['url']=get_youtube_url(songData)
		#print songData
	return allList

if __name__ == "__main__":
	print buildDictForDB("joi")

'''
@form_site.route('/')
def root():
    return render_template('base.html', title=d['title'], date=d['date'], copyright=d['copyright'], hdurl=d['hdurl'], explanation=d['explanation'])

if __name__ == '__main__':
    form_site.debug = True
    form_site.run()

'''
