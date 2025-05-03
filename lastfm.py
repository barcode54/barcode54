import os
import requests
import re
import pathlib

print(os.environ)
LASTFM_KEY = os.environ.get("LASTFM_KEY", "")
LASTFM_USER = os.environ.get("LASTFM_USER", "")
root = pathlib.Path(__file__).parent.resolve()
#plzworkk
def fetch_last(USER, KEY):
  url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={}&api_key={}&format=json&limit=1&page=1".format(USER, KEY)
  response = requests.get(url)
  result = response.json()
  track = result["recenttracks"]["track"][0]
  artist = track["artist"]["#text"]
  image = track["image"][3]["#text"]
  name = track["name"]

  clg = {
    "name" : name,
    "artist" : artist,
    "image" : image if image else "mizu5.png"
  }

  return clg





#code from https://eugeneyan.com/writing/how-to-update-github-profile-readme-automatically/


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(marker, chunk, marker)
    return r.sub(chunk, content)




if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()
    data = fetch_last(LASTFM_USER, LASTFM_KEY)
    res = '''<div>
    		      <hr>
    		      <h3>Lastfm status</h3>
	              <img width="300" height="300" src="{}" >
		              <h3> 🎵 Listening to {} - {}</h3>
    </div> '''.format(data['image'], data['artist'], data['name'])
    rewritten = replace_chunk(readme_contents, "lastfm status", res)
    
    readme.open("w").write(rewritten)
