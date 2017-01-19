def remove_parens(text):
    '''Parentheses, and anything inside of them, should be removed if they are
    not inside of '<>'s'''
    hrefs, paren, bracket, tbody = [], 0, 0, 0
    '''To cut down on time, only look at first quarter of text.  This could 
    clearly be optimized further'''
    #print(len(text))
    for i in range(len(text)):
        if bracket == 0 and tbody == 0 and text[i] == '(':
            paren += 1
        elif bracket == 0 and tbody == 0 and text[i] == ')':
            paren -= 1
        elif text[i] == '<':
            if text[i:i+6] == '<tbody':
                tbody += 1
                bracket += 1
                #print("9hiusadhsa")
            elif text[i:i+8] == '</tbody>':
                tbody -= 1
            elif paren == 0:
                bracket += 1
        elif text[i] == '>':
            if text[i-6:i] == '/tbody':
                #print("YUP")
                pass
            elif paren == 0:
                bracket -= 1
        #print(i, text[i], paren, bracket, tr)
        if paren == 0 and tbody == 0:
            # and (bracket == 1 or text[i] == '>')
            hrefs.append(text[i])
            #print(hrefs)
    links = "".join(hrefs)
    #print(links)
    return links
