#!/usr/bin/env python
 
import os
import sys
import eyed3
from goldfinch import validFileName as vfn
from gmusicapi import Mobileclient
import getpass
try:
  from urllib.request import urlretrieve
except ImportError:
  from urllib import urlretrieve


if len(sys.argv) == 1:
  print("usage: python gmusic-dl.py <email> <album id>")
  sys.exit()


def normalizePath(input):
  return vfn(input, space="keep", initCap=False).decode('utf-8').rstrip(".")  


login = sys.argv[1]
targetDir = os.getcwd()
albumId = sys.argv[2]
password = getpass.getpass()

eyed3.log.setLevel("ERROR")

api = Mobileclient(debug_logging=False)
api.login(login, password, Mobileclient.FROM_MAC_ADDRESS)

album = api.get_album_info(albumId)
dirName = normalizePath("%s - %s" % (album["artist"], album["name"]))
dirPath = targetDir + "/" + dirName

print("downloading to directory: " + dirPath)
if not os.path.exists(dirPath):
    os.makedirs(dirPath)
	
for song in album["tracks"]:
  url = api.get_stream_url(song_id=song["storeId"], quality="hi")
  fileName = normalizePath("%s. %s - %s.mp3" % (song["trackNumber"], song["artist"], song["title"]))
  filePath = dirPath + "/" + fileName
  print("downloading: " + fileName)
  urlretrieve(url, filePath)
  
  audio = eyed3.load(filePath)
  if audio.tag is None:
    audio.tag = eyed3.id3.Tag()
    audio.tag.file_info = eyed3.id3.FileInfo(filePath)
  audio.tag.artist = song["artist"]
  audio.tag.album = album["name"]
  audio.tag.album_artist = album["artist"]
  audio.tag.title = song["title"]
  audio.tag.track_num = song["trackNumber"]
  audio.tag.save()

print("done.")
