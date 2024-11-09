#!/usr/bin/env python

# File reads top to bottom, imperatively

# for references look at feed gen reference / atom reference / rss reference
# https://feedgen.kiesow.be/api.html
# https://validator.w3.org/feed/docs/atom.html
# https://cyber.harvard.edu/rss/rss.html
# Tinytag detail here: https://github.com/devsnd/tinytag

import sys
import os
import datetime
from pathlib import Path
from feedgen.feed import FeedGenerator
from tinytag import TinyTag

# User supplied info
# Set BASE_URL to the website that will serve your podcast/audiobook files
# BASE_URL = "https://your-web-site"
BASE_URL = ""
AUTHOR_NAME = ""
AUTHOR_EMAIL = ""

# Get time to work with.
current_time = datetime.datetime.now()

# Set up basic stuff. Get a folder and build a sorted list of audio files
book_folder = input("Paste path to audiobook folder here: ")
book_out_url = BASE_URL + "/" + (book_folder.split("/")[-1])
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
    if each_file.suffix in ['.mp3', '.m4a', '.m4b']:  # add other audio file extensions if you use them
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
    BASE_URL)  # atom thing. should normally be the base website itself if you have one. and i do :)
audio_book_feed.title(feed_title)  # title of the audiobook/podcast
audio_book_feed.author({"name": AUTHOR_NAME, "email": AUTHOR_EMAIL})  # feed author

### link to the feed relative to the id you set or just put in the full link and say rel='self'.
### i’d prefer being explicit for now. recommended atom thing
### https://validator.w3.org/feed/docs/atom.html#link
audio_book_feed.link(href=f'{book_out_url}', rel='self')
### language. rss thing. feedgen does something to also set xml:lang in atom. good to have
audio_book_feed.language('en')
audio_book_feed.podcast.itunes_category('Private')  # just tellin’ folks this is only for me
audio_book_feed.description(feed_title)

# Loop the file list and create entries in the feed

## Setup an empty dict to hold all the raw episode entries; keys ought to be the episode number
rough_episode_dict = {}
for each_file in audio_files:
    each_file_metadata = TinyTag.get(Path(book_folder, each_file))
    episode_file_path = Path(each_file)
    episode_suffix = episode_file_path.suffix
    episode_mime_type = 'audio/mpeg' if episode_suffix == '.mp3' else 'audio/x-m4a'
    episode_title = each_file_metadata.title
    episode_size = str(each_file_metadata.filesize)
    episode_link = f"{book_out_url}/{each_file}"
    dict_key_episode_num = int(each_file_metadata.track)
    rough_episode_dict[dict_key_episode_num] = [each_file_metadata, episode_title, episode_link, episode_size,
                                                episode_mime_type, episode_file_path, episode_suffix]
## Create a new sorted dict
episode_dict = dict(sorted(rough_episode_dict.items()))

## Now actually create entries in the dict, using values from the sorted dict
for each_episode in episode_dict.values():
    # The generator only has precision upto seconds. So we manually increment by a second for each episode
    current_time = current_time + datetime.timedelta(seconds=1)
    # Unpack stuff
    episode_title = each_episode[1]
    episode_link = each_episode[2]
    episode_size = each_episode[3]
    episode_mime_type = each_episode[4]
    episode_suffix = each_episode[5]
    episode_date = f'{datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")} +05:30'
    # Create a feed entry
    audio_episode = audio_book_feed.add_entry()
    audio_episode.title(episode_title)
    audio_episode.id(episode_link)
    audio_episode.enclosure(episode_link, episode_size, episode_mime_type)
    audio_episode.pubDate(episode_date)

# Write the rss feed to the same folder as the source audio files
audio_book_feed.rss_file(f"{book_folder}/feed.xml", pretty=True)
