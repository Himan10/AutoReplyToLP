""" Randomly select a quote from quotes.txt 
and Add a line at the end of the file 
lots of love @sender_tags
"""

from random import choice

def GenerateMessage():

    full_Message = ''

    # Starting line
    startLine = ""
    with open('txtFiles/greetings.txt', 'r') as file:
        startLine = choice(file.readlines())

    #Select a quote
    finalQuote = ""
    with open('txtFiles/quotes.txt', 'r') as file:
        FinalQuote = choice(file.readlines())   # return a list

    #Create a line
    lastLine = "\nLots of Love and virtual hugs "
    names = []
    with open('txtFiles/message2.txt', 'r') as file:
        names = list(map(lambda x: '@'+x.strip(), set(file.readlines())))
    
    full_Message = startLine + finalQuote + lastLine + ' '.join(names)
    return full_Message
