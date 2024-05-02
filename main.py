# set up flask and socketio
print("initializing... do not visit the web UI")
import logging, os, configparser, time, libraries.spotifyApiHelpers as spotifyApiHelpers, libraries.webUiHelpers as webUiHelpers, sys, threading, socket; from datetime import datetime; from flask import Flask, render_template, jsonify, request, redirect, url_for, render_template_string; from flask_socketio import SocketIO; from lyricsgenius import Genius; 
app = Flask(__name__)
app.logger.disabled = True
logging.getLogger('werkzeug').disabled = True
socketio = SocketIO(app, logger = False, engineio_logger = False)

# read config
config = configparser.ConfigParser()
config.read("files/config.ini")

# get app settings
port = config.get("app", "port")
refreshRate = int(config.get("app", "refresh rate"))
cacheSize = int(config.get("app", "cache size"))

# get credentials
refreshToken = config.get("spotify", "refresh token")
clientId = config.get("spotify", "client id")
clientSecret = config.get("spotify", "client secret")
redirectUri = config.get("spotify", "redirect uri")

# check for customization
fontSize = config.get("customization", "font size")
fontColor = config.get("customization", "font color")
backgroundColor = config.get("customization", "background color")

# other variables
pageOpen = False
accessToken, accessTokenTimestamp, track, artist, album, lyrics, lastTrack, lastArtist = None, None, None, None, None, None, None, None

# try to initialize genius client
try:
    genius = Genius(config.get("genius", "client access token"), verbose = False, skip_non_songs = False)
except:
    print("\033[91merror: genius access token incorrect\n\033[0m")
    quit()

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
        try:
            track, artist, album = spotifyApiHelpers.getPlayingSong(accessToken)
        except:
            track, artist, album = "error", "error", "error"
        if track == "error" and artist == "error" and album == "error":
            lyrics = "whoops! no lyrics can be found for the current song"
        else:
            
            # ok genius doesn't actually deserve the API abuse so this should only search songs and format it when spotify says it's a different song
            if lastTrack != track or lastArtist != artist or track is None:
                
                # check if the lyrics are already stored
                if track not in os.listdir("files/cache"):

                    # search for lyrics
                    error = False
                    try:
                        lyrics = genius.search_song(track, artist).lyrics
                    except:
                        error = True
                        lyrics = "whoops! no lyrics can be found for the current song"

                    # format lyrics if there are any
                    if not error:
                        lyrics = webUiHelpers.formatGeniusLyrics(lyrics, artist)
                        
                        # check if cache limit is being reached
                        cache = os.listdir("files/cache")
                        path = ["files/cache/{0}".format(x) for x in cache]
                        if len(cache) >= cacheSize:
                            oldestFile = min(path, key = os.path.getctime)
                            os.remove(oldestFile)

                        # save to cache
                        file = open("files/cache/" + track.replace("/", "//"), "w", encoding = "utf-8")
                        file.write(lyrics)
                        file.close()

                # load stored lyrics
                else:
                    file = open("files/cache/" + track.replace("/", "//"), "r", encoding = "utf-8")
                    lyrics = file.read()
                    file.close()
                
        # stop checking lyrics once page is closed
        if pageOpen == False:
            break
        time.sleep(refreshRate)


# load index html for showing lyrics
@app.route("/")
def index():
    return render_template("index.html", port = port, refreshRate = refreshRate, cacheSize = cacheSize, fontSize = fontSize, fontColor = fontColor, backgroundColor = backgroundColor)

# write settings to config
@app.route("/saveSettings", methods=["POST"])
def saveSettings():
    global port, refreshRate, cacheSize, fontSize, fontColor, backgroundColor
    if request.form["port"] and request.form["port"] != port:
        webUiHelpers.updateConfig("port", request.form["port"])
        port = request.form["port"]
    if request.form["refreshRate"] and request.form["refreshRate"] != refreshRate:
        webUiHelpers.updateConfig("refresh rate", request.form["refreshRate"])
        refreshRate = int(request.form["refreshRate"])
    if request.form["cacheSize"] and request.form["cacheSize"] != cacheSize:
        webUiHelpers.updateConfig("cache size", request.form["cacheSize"])
        cacheSize = int(request.form["cacheSize"])
    if request.form["fontSize"] and request.form["fontSize"] != fontSize:
        webUiHelpers.updateConfig("font size", request.form["fontSize"])
        fontSize = request.form["fontSize"]
    if request.form["fontColor"] and request.form["fontColor"] != fontColor:
        webUiHelpers.updateConfig("font color", request.form["fontColor"])
        fontColor = request.form["fontColor"]
    if request.form["backgroundColor"] and request.form["backgroundColor"] != backgroundColor:
        webUiHelpers.updateConfig("background color", request.form["backgroundColor"])
        backgroundColor = request.form["backgroundColor"]
    return redirect(url_for("index"))

# remove all files in the cache directory
@app.route("/clearCache", methods=["POST"])
def clearCache():
    for file in ["files/cache/{0}".format(x) for x in os.listdir("files/cache")]:
        os.remove(file)
    return redirect(url_for("index"))

# set all settings back to their initial values
@app.route("/resetSettings", methods=["POST"])
def resetSettings():
    global port, refreshRate, cacheSize, fontSize, fontColor, backgroundColor
    webUiHelpers.updateConfig("port", "3232")
    port = "3232"
    webUiHelpers.updateConfig("refresh rate", "10")
    refreshRate = 10
    webUiHelpers.updateConfig("cache size", "100")
    cacheSize = 100
    webUiHelpers.updateConfig("font size", "40")
    fontSize = "40"
    webUiHelpers.updateConfig("font color", "#ffffff")
    fontColor = "#ffffff"
    webUiHelpers.updateConfig("background color", "#080a0a")
    backgroundColor = "#080a0a"
    return redirect(url_for("index"))

# replace html with current lyrics
@app.route("/update")
def update_content():
    global lyrics
    return jsonify(content=lyrics.replace("\n", "<br>"))

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
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("\033[F\033[Kweb UI can be found at http://localhost:" + str(port) + " or http://" +  s.getsockname()[0] + ":" + str(port))
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    socketio.run(app, host="0.0.0.0", port=port, debug=False, log_output=False, allow_unsafe_werkzeug=True)
except:
    print("\033[91merror: issue serving app, are you connected to the internet?\033[0m")
