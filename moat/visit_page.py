from . import app
from . import remove_parens, valid_url
from bs4 import BeautifulSoup
import requests
import re

def visit(url="https://en.wikipedia.org/wiki/", topic="",
visited=None, hashed = None):
    if visited is None:
        visited = []
    if hashed is None:
        hashed = {}
    print(topic)
    #topic = topic[6:]
    #make dictionary where each word has either a number or a "next word".
    common = ['Science', 'Knowledge', 'Awareness', 'Quality_(philosophy)', 'Property_(philosophy)']
    for i, word in enumerate(common):
        if word == topic:
            common = common[i:]
            visited += common
            return visited
    if topic in hashed:
        visited.append(topic)
        return visited
    else:
        visited.append(topic)
        hashed[topic] = 1
    r = requests.get(url + topic)
    text = remove_parens.remove_parens(r.text)
    # BeautifulSoup(text, "html.parser").select('#mw-content-text li > a') + 
    soup = BeautifulSoup(text,  "html.parser").select('#mw-content-text p > a')
    try:
        topic = valid_url.valid_url(soup)[0][6:]
        print("topic,", topic)
    except ValueError:
        return visited
    if topic != "/wiki/Philosophy":
        return visit(url, topic, visited, hashed)
    visited.append('Philosophy')
    return visited