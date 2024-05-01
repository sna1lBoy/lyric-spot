# lyric spot installation tutorial

# step 0: prepare python
lyric spot is developed with python 3.11.7 and the external libraries flask 3.0.0, flask-socketio 5.3.6, requests 2.31.0, lyricsgenius 3.0.1, and urllib3 2.0.4

lyric spot will more than likely run normally if you either already have a somewhat recent python release and keep PIP and it's installs up to date or you newly downloaded the recent python release and all the required libraries because you didn't already have python and/or the libraries installed. however, if you're having issues with installation or want to set up a virtual environment for lyric spot then those are the specs.

if you want to know more in-depth about setting up python, please refer to the python organization's documentation about their software (especially the ones on [downloading python](https://wiki.python.org/moin/BeginnersGuide/Download) and [virtual environments](https://docs.python.org/3/tutorial/venv.html))

# step 1: download the source code
because lyric spot is based in python, the same code can be run the same way regardless of device as long as python is installed correctly. if you want a copy of the documentation or a quick and dirty install then download the zip from the top of the github repo and unzip it, otherwise you can find the source code without the fluff inside the releases section so download and extract that tarball instead. to download with the console, use `curl` or `wget` to download the source code and `tar` to extract

```
// example headless download
wget https://github.com/sna1lBoy/lyric-spot/releases/latest/download/lyricSpot.tar.gz
tar -xvzf lyricSpot.tar.gz
```

# step 2: fill in config.ini
if you open the `files` directory in the source code file, you'll find `config.ini` which will look like this

```
[app]
port = 3232
refresh rate = 10
cache size = 100

[spotify]
refresh token = 
client id = 
client secret = 
redirect uri = http://localhost:8888/callback

[genius]
client access token = 
```
four of these values are pre-defined for you and don't need to be changed unless you have a specific reason to
- port: the port number to find lyric spot on; change it if it contradicts with another program
- refresh rate: how often lyric spot makes the API calls needed to see if it needs to update the webpage (in seconds); try and go as big of an integer as comfortably possible if you want to fiddle with it, otherwise 10 seconds was perfect in my testing
- cache size: how many song lyrics is lyric spot allowed to store on the device, especially useful if you like to listen to things on loop; a song file is roughly 10KB so this is allocating about 1MB towards lyric spot but lower it if that's too much
- redirect uri: for spotify auth protocol; again change it if it conflicts with something

of the four undefined values, you only need to add values for three of them. for the first two, client id and secret, we need to set up a spotify application. visit https://developer.spotify.com/ and sign up/in. go to your dashboard and click "create app", then you'll be prompted to fill in many info boxes but lyric spot only cares about one. give the app whatever name and description you want and then scroll down to "redirect URI". in this box paste the URI you have set in the config. now create the app and go into it's settings and you should see the client ID. paste that into the config and click to reveal the client secret and do the same thing.

the last value is the client access token, which is much simpler. go to https://genius.com/api-clients and sign in/up. create a new client and give it a name and url (i used the same one as spotify), then click to generate an access token and paste it into the config.

# step 3: authorize the application
now that you've given lyric spot the info it needs to run correctly, it's finally time to run it! ...but wait, there's more! you'll need to generate an authorization code so spotify knows you give lyric spot permission to make API calls. when first booted, lyric spot will see that you left the refresh token blank and ask you to visit an accounts.spotify link. a few seconds after you open it, you should be redirected to a blank page. but check the url and you should see "code" near the beginning of it. copy everything after the equals sign and paste it into the console. if you did that as well as step 2 correctly, you should get a green message saying lyric spot is now continuing normally and you're free to visit the web UI at the printed address. otherwise, make sure your spotify application is set up correctly with the config and try again.

# step 4: optional side quests
now you've successfully set up lyric spot on one of your devices and can access it on the same network from any device with a web browser. but what if you didn't have to manually launch it every time you turned on the host device? or what if you could access it outside your home network? this is were services and tunnels come in to play. if you're interested in these ideas, here are some materials to get you started:
- https://www.wireguard.com/quickstart/
- https://www.procustodibus.com/blog/2021/04/wireguard-point-to-site-port-forwarding/
- https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files