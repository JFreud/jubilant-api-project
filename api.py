#from flask import Flask, render_template
import urllib2, json, requests

#henry zheng account

def get_songs(user):
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=" + user + "&api_key=9ec1ef2aeee03ef02b3158df6967d577&format=json"
    lastfm = urllib2.urlopen(url)
    dL = json.loads(lastfm.read())
    dL_lovedtracks = dL['lovedtracks']
    dL_track = dL_lovedtracks['track']
    retList = []

    
    for track in dL_track:
        dict = {}
        dict['dL_name'] = track['name']
        dict['dL_artist'] = track['artist']['name']

        #print dict
        retList.append(dict)

    return retList

#james smith account
api_base = "http://api.musixmatch.com/ws/1.1/{0}?{1}&apikey=7169e60f579305a0c080332a16b41537"#formatting strings for the command and parameters

def get_song_id(track, artist):
    url = api_base.format("track.search", "q_track={0}&q_artist={1}&page_size=5&page=1&s_track_rating=desc".format(track.replace(" ", "%20"), artist.replace(" ", "%20")))
    u = urllib2.urlopen(url)
    msg = u.read()
    search_dict = json.loads(msg)
    if search_dict["message"]["body"]["track_list"] == []:
        return '0'
    return search_dict["message"]["body"]["track_list"][0]["track"]["track_id"]

def get_lyrics(track_id):
    url = api_base.format("track.lyrics.get","track_id={}".format(track_id))
    u = urllib2.urlopen(url)
    msg = u.read()
    #print msg
    lyrics_dict = json.loads(msg)
    if lyrics_dict["message"]["body"] == []:
        return '0'
    body = lyrics_dict["message"]["body"]["lyrics"]["lyrics_body"]

    if body == "":
        return '0'
    else:
        return body

        
user_info = "rj"
#print get_songs(user_info)

    
def get_lyrics_all():
    retList = get_songs(user_info)
    for song in retList:
        lyrics = get_lyrics(get_song_id(song['dL_name'], song['dL_artist']))
        '''
        if 'lyrics' in song.keys():# or lyrics == None:
            del retList[retList.index(song)]
        else:
            song['lyrics'] = lyrics
        '''
        song['lyrics'] = lyrics
    #'''
    print len(retList)-1
    for x in range(0,len(retList)-1):
        if retList[0]['lyrics'] == '0':
            print x
            print retList[x]
            del retList[x]
        print "***" + str(x) + "***"
    #'''
    return retList

print get_lyrics_all()
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
    url = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21&sentences=false&text=' + urllib2.quote(text.encode('utf-8'))
    req = requests.get(url, auth=('1040bc05-8ffa-4577-a465-43d95b55737d', '0xvV0yqEOsyy'))
    json = req.json()
    tones = json['document_tone']['tones']
    for tone in tones:
        #print tone
        tone_name = tone['tone_name']
        if tone_name is not 'None':
            print tone_name

print analyze_single(lyrics)
     
'''
@form_site.route('/')
def root():
    return render_template('base.html', title=d['title'], date=d['date'], copyright=d['copyright'], hdurl=d['hdurl'], explanation=d['explanation'])
    
if __name__ == '__main__':
    form_site.debug = True
    form_site.run()

'''
