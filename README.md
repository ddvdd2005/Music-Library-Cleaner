# Music-Library-Cleaner
Cleans a music library of any duplicate

# What It Does
It makes sure your library does not have any duplicate by comparing the title and artist field of each track with every other tracks.

# Inputs:
It needs very few inputs from the users:
- A text file with the location of every song that you want to check for duplicates against (Read below how to obtain)
- A text file with the location of every song that you are sure contains no duplicates (Optional, for optimization)
- Choose whether you would like to, when duplicates are encountered:

  -Choose manually which files are kept
  
  -Choose automatically based on:
  
     i)best bitrate
       
     ii)longest
     
     iii)biggest (size-wise)
   
# Outputs:
A .m3u file that most music players should be able to read (MusicBee and MediaMonkey)

# Requirements:
Python 2.7 with Tkinter and Mutagen

A music library software (foobar, MusicBee, MediaMonkey for example)

# How to create the text file with the location of songs:
The following is a tutorial for MusicBee:

1. Select all the songs in the library (ctrl-a)
2. Right-click and choose add to playlist
3. Go to playlist and right-click the playlist you just created and choose export
4. This should create a m3u file
5. Open the m3u file with a notepad and copy the entirety of the m3u file and paste it in another notepad (to create a .txt file instead)
6. Choose, when saving the .txt file, for encoding, UTF-8

# Allowed file format:
This program only works with .FLAC, .mp3 and .m4a for now

# How to run:
Just run the python file
