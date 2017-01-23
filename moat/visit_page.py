from . import app
from . import remove_parens, valid_url
from bs4 import BeautifulSoup
import requests

def visit(url="https://en.wikipedia.org/wiki/", topic="",
visited=None, hashed=None, i=0):
    if visited is None:
        visited = []
    if hashed is None:
        hashed = {}
    r = requests.get(url + topic)
    text = remove_parens.remove_parens(r.text)
    soup = BeautifulSoup(text,  "html.parser").select('#mw-content-text p > a')
    # to improve: make cache hold either "next word", or list all the way to 
    # Philosophy
    common = ['Science', 'Knowledge', 'Awareness', 'Quality_(philosophy)', 'Property_(philosophy)', 'Philosophy']
    common2 = ['Unincorporated_community', 'Law', 'System', 'Interaction', 'Action_(physics)', 'Physics', 'Natural_science']
    common3 = ['United_Kingdom', 'Europe', 'Continent', 'Landmass', 'Earth', 'Sun', 'Star', 'Plasma_(physics)', 'State_of_matter#The_four_fundamental_states']
    common4 = ['Time', 'Sequence Mathematics', 'Quantity']
    common5 = ['Military', 'Use_of_force', 'Law_enforcement', 'Society', 'Social_group', 'Social_science', 'Discipline_(academia)']
    try:
        if i == 0:
            i += 1
            visited.append(topic)
            return visit(url, topic, visited, hashed, i)
        topic = valid_url.valid_url(soup)[0][6:] # [6:] because 'wiki/'
    except ValueError:
        return visited
    #print(topic)
    for i, word in enumerate(common):
        if word == topic:
            visited += common[i:]
            return visited
    for i, word in enumerate(common2):
        if word == topic:
            visited += common2[i:-1]
            topic = common2[-1]
            return visit(url, topic, visited, hashed, i)
    for i, word in enumerate(common3):
        if word == topic:
            visited += common3[i:-1]
            topic = common3[-1]
            return visit(url, topic, visited, hashed, i)
    for i, word in enumerate(common4):
        if word == topic:
            visited += common4[i:-1]
            topic = common4[-1]
            return visit(url, topic, visited, hashed, i)
    for i, word in enumerate(common5):
        if word == topic:
            visited += common5[i:-1]
            topic = common5[-1]
            return visit(url, topic, visited, hashed, i)
    if topic in hashed:
        visited.append(topic)
        return visited
    else:
        visited.append(topic)
        hashed[topic] = 1
    if topic != "/wiki/Philosophy":
        return visit(url, topic, visited, hashed, i)
    visited.append('Philosophy')
    return visited