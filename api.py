#from flask import Flask, render_template
import urllib2, json, requests

#henry zheng account

def get_songs(user):
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=" + user + "&api_key=9ec1ef2aeee03ef02b3158df6967d577&format=json"
    lastfm = requests.get(url)

    # lastfm = urllib2.urlopen(url)
    dL = json.loads(lastfm.text)
    dL_lovedtracks = dL['lovedtracks']
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

#james smith account
api_base = "http://api.musixmatch.com/ws/1.1/{0}?{1}&apikey=7169e60f579305a0c080332a16b41537"#formatting strings for the command and parameters

def get_song_id(track, artist):
    url = api_base.format("track.search", "q_track={0}&q_artist={1}&page_size=5&page=1&s_track_rating=desc".format(track.replace(" ", "%20"), artist.replace(" ", "%20")))
    #u = urllib2.urlopen(url)
    #msg = u.read()
    msg = requests.get(url)
    search_dict = json.loads(msg.text)
    if search_dict["message"]["body"]["track_list"] == []:
        return '0'
    return search_dict["message"]["body"]["track_list"][0]["track"]["track_id"]

def get_lyrics(track_id):
    url = api_base.format("track.lyrics.get","track_id={}".format(track_id))
    # u = urllib2.urlopen(url)
    # msg = u.read()
    #print msg
    msg = requests.get(url)
    lyrics_dict = json.loads(msg.text)
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

    # for x in range(0,len(retList)-1):
    #     if retList[0]['lyrics'] == '0':
    #         print x
    #         print retList[x]
    #         del retList[x]
    #     print "***" + str(x) + "***"
    # #'''

    i = 0
    while (i < len(retList)):
        if retList[i]['lyrics'] == '0':#iterates through list and if no lyrics removes it; does not increment because it moves to next automatically through deletion
            #print "\nZERO\n"
            del retList[i]
        else:
            #print "\n***" + str(i) + "***\n"
            i += 1
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
        print tone
        tone_name = tone['tone_name']
        if tone_name is not 'None':
            print tone_name

print "\n===== LYRICS ======\n"
# print get_lyrics_all()[1]['lyrics']
print "\n===========\n"

analyze_single(get_lyrics_all()[1]['lyrics'])
# analyze_single('''49
# Ever feel kinda down and out, you don't know just what to do
# Livin' all of your days in darkness let the sun shine through
# Ever feel that somehow, somewhere you've lost your way
# And if you don't get help quick you won't make it through the day
# Could you call on Lady Day, could you call on John Coltrane
# ...
#
# ******* This Lyrics is NOT for Commercial use *******
# (1409616471235)
# ''')

def get_youtube_url(song_dict):
    artist = song_dict['dL_artist'].replace(" ", "+")#replace spaces in query with +
    title = song_dict["dL_name"].replace(" ", "+")
    query = artist + "+" + title
    key = "AIzaSyATP2BxeFJ1vx1o9k-48pLcBcAMopDf3PY"
    url = "https://www.googleapis.com/youtube/v3/search?key=%s&part=snippet&q=%s" % (key, query)#builds url
    response = requests.get(url)
    results_dict = json.loads(response.text)#creates dict of response

    video_id = results_dict['items'][0]['id']['videoId']#extracts video query id from the dict
    return "https://www.youtube.com/watch?v=" + video_id

song = get_lyrics_all()[2]
print "=====song: %s by %s\n" % (song['dL_name'], song['dL_artist'])
print get_youtube_url(song)

'''
@form_site.route('/')
def root():
    return render_template('base.html', title=d['title'], date=d['date'], copyright=d['copyright'], hdurl=d['hdurl'], explanation=d['explanation'])

if __name__ == '__main__':
    form_site.debug = True
    form_site.run()

'''
