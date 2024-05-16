# lyric spot
<img align="left" width="100" height="100" style="padding-right: 20px;" src="local/static/favicon.ico"> i believe in the radical idea that accessibility features shouldn't be locked behind a paywall, but what do i know? i'm just a silly lil' open source developer guy with a hearing disability, not a multi ~~millionaire~~ billionaire CEO that pays artists pennies for their work that makes his platform possible... anyways for [totally unrelated](https://www.theverge.com/2023/9/5/23860124/spotify-lyrics-premium-only-feature) reasons i'm proud to introduce lyric spot!

<br>

# about
lyric spot uses the spotify and genius APIs to find the lyrics of the song you're currently playing on spotify then displays those lyrics on a webpage. this hosting method means you can view them anywhere* and regardless of device type, as long as it has a web browser.

*assuming you add lyric spot to a server and use a tunnel with port-forwarding, otherwise only when on the same network as the device running it.

# bugs and suggestions
lyric spot is primarily a tool meant to help me understand music with my hearing loss so development will center on that premise. that being said, please put any ideas or suggestions in the issues tab and i'll try to get to them.

### known issues
- the genius API wrapper used won't fail a search, meaning it may return the wrong/gibberish lyrics

<br>

# ready to install?
view the [documentation](docs/tutorial.md) if you need help installing lyric spot.