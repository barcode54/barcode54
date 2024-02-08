import os
import requests
import re
import pathlib

KEY = os.environ.get("LASTFM_KEY", "")
USER = os.environ.get("LASTFM_USER", "")
root = pathlib.Path(__file__).parent.resolve()
#plzwork
def fetch_last(KEY, USER):
  url = "http://ws.audioscrobbler.com/2.0/"
  params = {
    "limit" : 1,
    "user" : USER,
    "page" : 1,
    "api_key" : KEY
  }

  response = requests.get(url=url, params=params)
  result = response.json()
  track = result["recenttracks"]["track"][0]
  artist = track["artist"]["#text"]
  image = track["image"][3]["#text"]
  name = ["name"]

  clg = {
    "name" : name,
    "artist" : artist,
    "image" : image
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
    data = fetch_last(KEY, USER)
    res = '''<div style="position:relative;width:400px; margin:auto">
	              <img src="image['image']" style="height:400px; width:inherit;">
	              <div style="position:absolute;bottom:0px;left:0px;width:100%;background-image:linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.7));">
		              <h1 style="color:white; font-family:consolas; margin-left:10px;overflow: hidden; text-overflow: ellipsis;">{data['artist']}</h1>
 		              <h2 style="color:white; font-family:consolas; margin-left:10px;overflow: hidden; text-overflow: ellipsis;">{data['name']}</h2>
  	            </div>
    </div> '''
    rewritten = replace_chunk(readme_contents, "lastfm status", res)
    
    readme.open("w").write(rewritten)
