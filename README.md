# Toontown Autotask

This is a work-in-progress computer vision bot that aims to play the 3D MMORPG Toontown.

So far, I've built the part of the bot that is activated once the player's objective is determined. The bot detects the location of the player and objective on the minimap, computes a path between the two points, and converts this path into arrow-key inputs so that the player automatically moves to the objective.

Adapted code from [learncodebygaming's OpenCV tutorial](https://github.com/learncodebygaming/opencv_tutorials/tree/master/007_canny_edge). In particular:
- windowcapture.py, edgefilter.py, hsvfilter.py are unaltered
- minor alterations to vision.py
- main.py altered quite heavily
- pathfinder.py is my own code.
