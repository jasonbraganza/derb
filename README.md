# derb is retired
Derb is essentially feature complete; it does all I want it to do.  
Hence the freeze.  
The only thing I really need, is a single executable that I can easily distribute, so I’m reinventing the wheel with [ReDerb](https://github.com/jasonbraganza/rederb).  
ReDerb is still very much an unfinished work in progress as of 2025-03-08. I’ll update it when I consider it done.   

## derb
Utility to create an RSS feed from a bunch of files in a given path.  
I need to serve audio files to my family, and serving them up as a feed, so that they could subscribe to it as a podcast seemed like a good idea. 

## Why is this called derb?  
Because it was the first name that popped up when I used the first random name generator site I looked for, on the web. It’s just a fun, nice sounding, random noun.
  
## What does this do?
Derb generates an podcast feed for all the audio files in a directory. No it does not recurse.  

## Prerequisites
1. The audio files need to be in a single directory
2. They need to have proper metadata (if not, use something like Ex Falso, Puddletag, and Kid3 on Linux or Tag & Rename on Windows (paid software, I’m not aware of opensource options on Windows) to tag them the way you want.)

## How do I use this?
- Clone repo to a folder
- Create a `venv` and activate it
- Install dependencies
- Edit the script and edit the `base_url` variable to point to your site that’ll serve the feed.
- and run the script 
- It’ll ask you for a path to the files
- and then create `feed.xml` in the audio file directory you gave.

## Then what?  
- Examine feed, and see if all is to your liking
- Move said folder to your website, so it can be served

# Gratitude
To [Tom Wallroth](https://github.com/devsnd)’s (@devsnd) [Tinytag](https://github.com/devsnd/tinytag) and  [Lars Kiesow](https://github.com/lkiesow)’s (@lkiesow) [Feedgenerator](https://github.com/lkiesow/python-feedgen).  
They made it easy to whip up a tiny script like this.
