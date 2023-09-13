#!/usr/bin/env python

# for references look at feed gen reference / atom reference / rss reference
# https://feedgen.kiesow.be/api.html
# https://validator.w3.org/feed/docs/atom.html
# https://cyber.harvard.edu/rss/rss.html
# Tinytag detail here: https://github.com/devsnd/tinytag

import sys
import os
from pathlib import Path
from feedgen.feed import FeedGenerator
from tinytag import TinyTag

# Set up basic stuff. Get a folder and build a sorted list of audio files
base_url = "https://ab.janusworx.com/"
book_folder = input("Paste path to audiobook folder here: ")
book_out_path = base_url + (book_folder.split("/")[-1])
file_list = os.walk(book_folder)

## Do a basic check on the validity of the path we get, before we build the audio file list.
try:
    all_files = (list(file_list)[0][2])
except IndexError as e:
    print(f"\n\n"
          f"---\n"
          f"ERROR!: {e}\n"
          f"Have you typed in the right path?\n"
          f"---\n")
    sys.exit("Quitting script!")
audio_files = []
for each_file in all_files:
    each_file = Path(each_file)
    if each_file.suffix in ['.mp3', '.m4a', '.m4b']:
        audio_files.append(str(each_file))
audio_files = sorted(audio_files)

# Setup a feed
## Grab feed metadata from the first audio file
feed_metadata_file = TinyTag.get(Path(book_folder, audio_files[0]))

## Grab title from metadata file.
## At the same time, break out if there isn’t any.
if not feed_metadata_file.album:
    sys.exit("\n---\nStopping feed creation.\nSetup audio file metadata with a tag editor")
feed_title = feed_metadata_file.album

## Creating feed instance
audio_book_feed = FeedGenerator()
audio_book_feed.load_extension("podcast")

## Setting up more stuff on the feed proper
audio_book_feed.id(
    "https://ab.janusworx.com")  # atom thing. should normally be the base website itself if you have one. and i do :)
audio_book_feed.title(feed_title)  # title of the audiobook/podcast
audio_book_feed.author({"name": "Jason Braganza", "email": "feedback@janusworx.com"})  # feed author

### link to the feed relative to the id you set or just put in the full link and say rel='self'.
### i’d prefer being explicit for now. recommended atom thing
### https://validator.w3.org/feed/docs/atom.html#link
audio_book_feed.link(href=f'{book_out_path}', rel='self')

### language. rss thing. feedgen does something to also set xml:lang in atom. good to have
audio_book_feed.language('en')

audio_book_feed.podcast.itunes_category('Private')  # just tellin’ folks this is only for me
audio_book_feed.description(feed_title)

# Loop the file list and create entries in the feed

for each_file in audio_files:
    # Mime types m4a/b - 'audio/x-m4a'
    # mp3 - 'audio/mpeg'
    each_file_metadata = TinyTag.get(Path(book_folder, each_file))
    episode_file_path = Path(each_file)
    episode_suffix = episode_file_path.suffix
    episode_mime_type = 'audio/mpeg' if episode_suffix == '.mp3' else 'audio/x-m4a'
    episode_title = each_file_metadata.title
    episode_size = str(each_file_metadata.filesize)
    episode_link = f"{book_out_path}/{each_file}"
    audio_episode = audio_book_feed.add_entry()
    audio_episode.title(episode_title)
    audio_episode.id(episode_link)
    audio_episode.enclosure(episode_link, episode_size, episode_mime_type)

# Write the rss feed to the same folder as the source audio files
audio_book_feed.rss_file(f"{book_folder}/feed.xml")
