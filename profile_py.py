# -*- coding: utf-8 -*-
"""profile.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lSSjR04e_yqVAC4rT9VoO7CjMA34oqR3
"""

import instaloader
ig=instaloader. Instaloader()
usrname=input("Enter Username: ")
profile=instaloader.Profile.from_username(ig.context, usrname)
print("Username: ", profile.username)
print("Number of Posts Uploads:", profile.mediacount)
print(profile.username+" is having" + str(profile.followers)+ 'followers')
print(profile.username+" is following" + str(profile.followees)+' people')
print("Bio: ", profile.biography)
instaloader. Instaloader().download_profile(usrname,profile_pic_only=True)

pip install instaloader