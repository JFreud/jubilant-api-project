# Inside Out the Musical
### by zeBois
#### Daniel Chernovolenko, Jerome Freudenberg, Jonathan Quang, Henry Zheng<br>SoftDev1 pd8<br>Project 01 -- Get your hands off of me, you dirty APIs!

### Description

Our website will take a user input on how they’re feeling/what mood of music they want to listen to as well as their last.fm username. The website will then access their “loved” songs on last.fm and use musixmatch to look up the lyrics. Then, the lyrics will be input into the watson tone analyzer and the tone of the song will be determined. We then return a playlist of their “loved” songs that match the tone of music they selected, and embed a youtube video of the song in the output.

## Launch Instructions

1. Enter your terminal and go into the directory that you want to have this program in
2. Enter this command to clone our repo
```
https://github.com/JFreud/jubilant-api-project.git
```
3. Run your virtualenv from wherever you have it (if needed)
```
. <PATH_TO_VIRTUALENV>/bin/activate
```
4. Go into the jubilant-api-project folder using this command
```
cd jubilant-api-project/
```
5. Run the program
```
python app.py
```
6. Go to localhost:5000 in your web browser and enjoy the site!


## API Key Instructions

#### last.fm
1. Login to last.fm / Create a last.fm account
1. Create an API account [here](https://www.last.fm/api/account/create)
    * Optional fields except for email and application name
2. Use your key! (No quotas unless streaming music)
#### musixmatch
1. Head to their [developer site](https://developer.musixmatch.com/plans)
2. Select plan
3. Make account and fill out required fields
4. Go back to the developer page and press on the plan you chose again
5. Press "Applications"
6. See key next to name of app
5. Use your key! (2k API calls daily and only 30% of lyrics)
#### Watson Tone Analyzer
1. Create an IBM Cloud account [here](https://console.bluemix.net/registration/?target=%2Fdeveloper%2Fwatson%2Fcreate-project%3Fservices%3Dtone_analyzer%26hideTours%3Dtrue&cm_mmc%3DOSocial_Tumblr-_-Watson%2BCore_Watson%2BCore%2B-%2BPlatform-_-WW_WW-_-wdc-ref%26cm_mmc%3DOSocial_Tumblr-_-Watson%2BCore_Watson%2BCore%2B-%2BPlatform-_-WW_WW-_-wdc-ref%26cm_mmca1%3D000000OF%26cm_mmca2%3D10000409&cm_mc_uid=85682610252115107975529&cm_mc_sid_50200000=1511628693&cm_mc_sid_52640000=1511628693)
2. Go to add a new service and choose Watson Tone Analyzer
3. Go to Service credentials
4. Add a new key and voila.
5. Use your key(2,500 API calls per month for free)
    * Only one API service at a time for free
    * Disabled after 30 days of inactivity
#### YouTube
1. Make a google account
2. Create a project in the [Google Developers Console](https://console.developers.google.com)
3. If you are trying to access user data, you need [authorization credentials](https://developers.google.com/youtube/registering_an_application)
4. [Open the API Library](https://console.developers.google.com/apis/library?project=_) and make sure it is enabled
5. Use your key! (default quota allocation of 1 million units per day)

## Dependencies
* `from flask import Flask, render_template, request, session, redirect, url_for`
  * requires `pip install flask`
* [`python2.7`](https://www.python.org/download/releases/2.7/)
* `import requests, json`
  * requires `pip install requests`

## File Structure
```
data/
  |  songs.db
static/
  css/
    |  bodystylesheet.css
    |  loginstylesheet.css
  images/
    |  background.jpg
templates/
  |  accountErrorPage.html
  |  base.html
  |  home.html
  |  input.html
  |  login.html
  |  loginbase.html
  |  output.html
  |  register.html
  |  uniTemp.html
utils/
  |  api.py
  |  database.py
app.py
changes.txt
design.pdf
devlog.txt
log.sh
README.md
```
