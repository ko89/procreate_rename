# procreate_rename

A python script for renaming all procreate files in a directory based on their creation date.

Since I'm often too lazy to name them, most of my procreate files end up as "Untitled Artwork",
which isn't great when trying to find something in a backup.

To have at least some kind of organisation I wrote this script,
to check each file for the date it was created and rename it to something like:

2025-11-06_originalname_number.procreate

Currently the script tries to get the creation date from the timelapse recordings inside the procreate file.
(So if there is no timelapse it won't be able to rename the file..!)

# How to use

I may try to create some kind of executable at some point, but right now you will need to install python to run this.

Using uv as a project manager (be sure to create the output directory first):
uv run main.py -i "/path/to/input" -o "/path/to/output"
