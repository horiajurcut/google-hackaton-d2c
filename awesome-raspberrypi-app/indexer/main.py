import os
import time
import json
from urllib import quote

import mutagen
import requests

from webapp.core import db
from webapp.models import Song
from indexer.location import LocationDetecter

from pyechonest import config
config.ECHO_NEST_API_KEY = "5MIPWN4SAMW1TKX0Z"

from pyechonest import song

SUPPORTED_EXTENSIONS = [ "mp3", "m4a" ]
EXTRACTED_PARAMS = [ "album", "artist", "title", "genre" ] 
TIMEOUT = 1

class EmptyTags(Exception):
  pass

class Tag(object):

  def __init__(self, mutagen_obj, length=None, source=None):
    self._params = {}

    for param in EXTRACTED_PARAMS:
      if param in mutagen_obj:
        setattr(self, param, mutagen_obj[param][0])
        # for to_filter
        self._params[param] = mutagen_obj[param][0]
      else:
        setattr(self, param, None)

    #if len(self._params.keys()) == 0:
    #  raise EmptyTags()

    self._params["duration"] = int(length)
    self._params["source"] = source

    if self.artist != None and self.title != None:
      # bucket=id:7digital-US&bucket=audio_summary&bucket=tracks

      try:

        response = json.loads(requests.get("http://ws.audioscrobbler.com/2.0/?method=track.search&artist=%s&track=%s&api_key=cfbaac1876f3141cab02e1235b958e20&format=json" % (quote(self.artist), quote(self.title))).text)

        self._params["cover"] = response["results"]["trackmatches"]["track"][0]["image"][2]["#text"]

      except:
        pass

  def to_filter(self):
    return self._params

class Indexer(object):

  def __init__(self):
    pass

  def run(self):
    self.location = LocationDetecter().get_location()

    #while True:
    self.update()
    #  time.sleep(TIMEOUT)

  def update(self):
    # http://ws.audioscrobbler.com/2.0/?method=track.search&track=Believe&api_key=cfbaac1876f3141cab02e1235b958e20&format=json
    path = self.location.path
    updated = []

    for root, dirs, files in os.walk(path):
      for filename in files:
        if any([ filename.endswith(ext) and not filename.startswith(".") for ext in SUPPORTED_EXTENSIONS ]):
          path = root + "/" + filename
          length = mutagen.File(path).info.length

          audiofile = Tag(mutagen.File(path, easy=True), length=length, source=path)

          filters = audiofile.to_filter()
          song = Song.query.filter_by(**filters).first()

          if song == None:
            song = Song(**filters)
            db.session.add(song)
            db.session.commit()

            updated.append(song.id)
          else:
            db.session.execute(db.update(Song).where((Song.id.in_([ song.id ]))).values(**filters))
            db.session.commit()
            updated.append(song.id)

    db.session.execute(db.update(Song).where(db.not_(Song.id.in_(updated))).values(status=0))
    db.session.commit()
