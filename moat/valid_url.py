def valid_url(soup):
    ''' Check if the first link meets certain criteria. If no links in the first 
    'paragraph' meet the criteria ('paragraph' is probably a tbody of images), 
    try the next paragraph.'''
    links = []
    while len(links) == 0:
        for link in soup:
            #print(link)
            href = link.get("href")
            dont = ["/wiki/Help", "/wiki/File", "/wiki/User"]
            if not link.find(class_='image') and href.startswith("/wiki/") and not href.startswith(tuple(dont)):
                links.append(link.get("href"))
                #print(link.get("href"))
        if len(links) == 0:
            raise ValueError
    return links