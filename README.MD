# lyric spot
i believe in the radical idea that accessibility features shouldn't be locked behind a paywall, but what do i know? i'm just a silly lil' open source developer guy with a hearing disability, not a multi ~~millionaire~~ billionaire CEO that pays artists pennies for their work that makes his platform possible... anyways for [totally unrelated](https://www.theverge.com/2023/9/5/23860124/spotify-lyrics-premium-only-feature) reasons i'm proud to introduce lyric spot!

# about
lyric spot uses the spotify and genius APIs to find the lyrics of the song you're currently playing on spotify then displays those lyrics on a webpage. this hosting method means you can view them anywhere* and regardless of device type, as long as it has a web browser.

*assuming you add lyric spot to a server and use a tunnel with port-forwarding, otherwise only when on the same network as the device running it.

# bugs and suggestions
bugs are bound to happen especially with a single developer managing multiple APIs as a side project to his university coursework, so don't be afraid to report any in the issues tab. the only issue that i know of that i can't fix is the genius API showing the wrong thing when the lyrics don't exist on the genius website for the current song, but hey i guess it's a reason to contribute, right? :)

lyric spot is primarily a tool meant to help me understand music with my hearing loss so development will center on that premise. that being said, please put any ideas or suggestions in the issues tab and i'll try to get to them.

here are the features i'm currently planning on implementing:
- using the web UI for initial setup instead of terminal in order to make the installation process as easy as possible for non-techys, as well as adding credintials into the settings menu as a byproduct
- firefox and chrome extensions; gives users the option to choose a lite version of lyric spot if they're not interested in they whole installation process
    - pros: don't need to set up python or constantly run a python script on your machine
    - cons: lyrics can only be accessed from the extension page on that specific browser on that specific machine, may be slower due to running in a browser, may not be able to cache lyrics as well

# ready to install?
view the [tutorial](docs/tutorial.md) if you need help setting up lyric spot.