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

path = "C:/Users/DucksOnFlame/Desktop/Workspaces/Python/LoLChampionBot/responded/responded_comments.txt"

header = "**Champion data**\n"
footer = "\n--This data was extracted from .......... | Bot created by /u/5th_Deathsquad"

subreddits = "test"
limit = 5000
search_interval = 10

def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit("LoLChampionBot", user_agent="web:lol-champion-bot:v0.1 by (/u/5th_Deathsquad")
    print("Authenticated as {}\n".format(reddit.user.me()))
    return reddit


def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tag = soup.find("p")
    data = ""
    while True:
        if isinstance(tag, bs4.element.Tag):
            if tag.name == "h2":
                break
            if tag.name == "h3":
                tag = tag.nextSibling
            else:
                data = data + "\n" + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling

    return data


def run_lolchampionbot(reddit):

    print("Getting " + str(limit) + " comments...")

    for comment in reddit.subreddit(subreddits).comments(limit=limit):
        match = re.findall("http[s]?://[www.]?xkcd.com/\d+", comment.body)
        if match:
            print("Link found in comment with comment ID: " + comment.id)
            xkcd_url = match[0]
            url_obj = urlparse(xkcd_url)
            xkcd_id = int((url_obj.path.strip("/")))
            myurl = "http://www.explainxkcd.com/wiki/index.php/" + str(xkcd_id)

            file_obj_r = open(path, "r")

            try:
                explanation = fetch_data(myurl)
            except:
                print("Exception! Possibly incorrect xkcd URL... \n")
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print("Comment is unique... posting explanation\n")
                    comment.reply(header + explanation + footer)

                    file_obj_r.close()

                    file_obj_r = open(path, "a+")
                    file_obj_r.write(comment.id + "\n")
                    file_obj_r.close()
                else:
                    print("Already visited link... no reply needed.\n")

    print("Waiting " + str(search_interval) + " seconds... \n")
    time.sleep(search_interval)


def main():
    reddit = authenticate()
    while True:
        run_lolchampionbot(reddit)


if __name__ == "__main__":
    main()