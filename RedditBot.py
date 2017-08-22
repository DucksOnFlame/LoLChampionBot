# A Reddit bot that posts champion information for characters in a game League Of Legends
# The data is extracted from .......................
# Created by Bartlomiej Styczynski (/u/5th_Deathsquad)
# License: MIT License


from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4

path = "/responded/responded_comments.txt"

header = "**Champion data**\n"
footer = "\n--This data was extracted from .......... | Bot created by /u/5th_Deathsquad"

def authenticate:
    print("Authenticating...")
    reddit = praw.Reddit()
