import requests, base64; from urllib.parse import urlencode; from datetime import datetime

# use auth token to generate a refresh token and store it in the config
def authScript(clientId, clientSecret, redirectUri):

    # request refresh token using auth url
    print("\033[91merror: no refresh token found\n\033[0m")
    print("authorize this program by going to: https://accounts.spotify.com/authorize?" + str(urlencode({"client_id": clientId, "response_type": "code", "redirect_uri": redirectUri, "scope": "user-read-currently-playing user-modify-playback-state"})))
    authorizationCode = input("enter the authorization code found in the redirected url after \"code=\": ")
    response = requests.post("https://accounts.spotify.com/api/token", auth = (clientId, clientSecret), data = {"grant_type": "authorization_code", "code": authorizationCode, "redirect_uri": redirectUri})

    # making sure the user didn't fuck up
    if response.ok:
        print("\033[92m\nprogram authorized, now will run as normal\n\033[0m")
        refreshToken = response.json()["refresh_token"]
    
        # writing refresh token to config
        file = open("files/config.ini", "r")
        lines = file.readlines()
        file.close()

        file = open("files/config.ini", "w")
        for line in lines:
            if line.startswith("refresh token ="):
                line = "refresh token = " + refreshToken + "\n"
            file.write(line)
        file.close()
        return refreshToken
    
    # the user fucked up, tell them that they did
    else:
        print("\033[91m\nsomething went wrong! make sure your application info is correct and that you're pasting the entire auth code then try running this script again\033[0m")
        quit()

# generate an access token
def genAccessToken(clientId, clientSecret, refreshToken):
    response = requests.post("https://accounts.spotify.com/api/token", headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic " + base64.b64encode(f"{clientId}:{clientSecret}".encode()).decode()}, data = {"grant_type": "refresh_token", "refresh_token": refreshToken})
    accessToken = response.json()["access_token"]
    return int(datetime.now().timestamp()), accessToken 

# print currently playing song
def getPlayingSong(accessToken):
    request = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers={"Authorization": "Bearer " + accessToken})
    if request.ok and request.content:
        data = request.json()
        return data["item"]["name"], data["item"]["album"]["artists"][0]["name"], data["item"]["album"]["name"]
    else:
        return "error", "error", "error"