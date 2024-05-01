# set up flask and socketip
print("initializing... do not visit the web UI")
import logging, os, configparser, time, libraries.spotifyApiHelpers as spotifyApiHelpers, sys, threading, socket; from datetime import datetime; from flask import Flask, render_template, jsonify; from flask_socketio import SocketIO; from lyricsgenius import Genius
app = Flask(__name__)
app.logger.disabled = True
logging.getLogger('werkzeug').disabled = True
socketio = SocketIO(app, logger = False, engineio_logger = False)

# read config and set up variables
config = configparser.ConfigParser()
config.read("files/config.ini")
port = config.get("app", "port")
refreshRate = int(config.get("app", "refresh rate"))
cacheSize = int(config.get("app", "cache size"))
refreshToken = config.get("spotify", "refresh token")
clientId = config.get("spotify", "client id")
clientSecret = config.get("spotify", "client secret")
redirectUri = config.get("spotify", "redirect uri")
genius = Genius(config.get("genius", "client access token"), verbose = False, skip_non_songs = False)
pageOpen = False
accessToken, accessTokenTimestamp, track, artist, album, lyrics, lastTrack, lastArtist = None, None, None, None, None, None, None, None

# initial script authorization
if refreshToken == "":
    refreshToken = spotifyApiHelpers.authScript(clientId, clientSecret, redirectUri)

# constant loop to check current song and find lyrics while page is open
def lyricsLoop():
    global accessTokenTimestamp, accessToken, track, artist, album, lyrics, lastTrack, lastArtist
    while (True):
        
        # see if a new token needs to be genned, as of april 2024 this needs to be done every hour (3600 seconds)... if you're viewing this code at any other time who the fuck knows
        if accessTokenTimestamp is None or int(datetime.now().timestamp()) - accessTokenTimestamp >= 3600:
            accessTokenTimestamp, accessToken = spotifyApiHelpers.genAccessToken(clientId, clientSecret, refreshToken)

        # get current lyrics, if any, and send it to the webpage
        lastTrack, lastArtist = track, artist
        track, artist, album = spotifyApiHelpers.getPlayingSong(accessToken)
        if track == "error" and artist == "error" and album == "error":
            lyrics = "whoops! no lyrics can be found for the current song"
        else:
            
            # ok genius doesn't actually deserve the API abuse so this should only search songs and format it when spotify says it's a different song
            if lastTrack != track or lastArtist != artist:
                
                # check if the lyrics are already stored
                if track not in os.listdir("files/cache"):
                    # search for lyrics
                    lyrics = genius.search_song(track, artist).lyrics
                    index = lyrics.find("Lyrics")

                    # remove header
                    if index != -1:
                        lyrics = lyrics[index + len("Lyrics"):]
                    
                    # remove embed tag
                    lyrics = lyrics[:-5]
                    while (True):
                        if lyrics[len(lyrics)-1].isdigit():
                            lyrics = lyrics[:-1]
                        else:
                            break
                    
                    # check if cache limit is being reached
                    cache = os.listdir("files/cache")
                    path = ["files/cache/{0}".format(x) for x in cache]
                    if len(cache) >= cacheSize:
                        oldestFile = min(path, key = os.path.getctime)
                        os.remove(oldestFile)

                    # save to cache
                    file = open("files/cache/" + track, "w", encoding = "utf-8")
                    file.write(lyrics)
                    file.close()

                # load stored lyrics
                else:
                    file = open("files/cache/" + track, "r", encoding = "utf-8")
                    lyrics = file.read()
                    file.close()
                

        # stop checking lyrics once pace is closed
        if pageOpen == False:
            break
        time.sleep(refreshRate)

# load index html for showing lyrics
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/update')
def update_content():
    global lyrics
    return jsonify(content=lyrics.replace('\n', '<br>'))

# sockets so that the lyric loop only runs when this page is open to minimize api abuse (spotify deserves it lmao have you seen the api flow chart? (https://developer.spotify.com/images/documentation/web-api/auth-code-flow.png) but i don't want them banning my ass lol)
@socketio.on("connect")
def handle_connect():
    global pageOpen
    if not pageOpen:
        pageOpen = True
        threading.Thread(target=lyricsLoop).start()
@socketio.on("disconnect")
def handle_disconnect():
    global pageOpen
    pageOpen = False

# if there's no issues during setup, tell the user how to find the app and run it
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print("\033[F\033[Kweb UI can be found at http://localhost:" + str(port) + " or http://" +  s.getsockname()[0] + ":" + str(port))
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
socketio.run(app, host="0.0.0.0", port=port, debug=False, log_output=False)