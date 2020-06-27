""" Randomly select a quote from quotes.txt 
and Add a line at the end of the file 
lots of love @sender_tags
"""

from random import choice, sample

def GenerateMessage():

    fullMessage = ''

    # Starting line
    startLine = ""
    with open('txtFiles/greetings.txt', 'r') as file:
        startLine = choice(file.readlines())

    #Select a quote
    FinalQuote = "Quote of the Day -> "
    with open('txtFiles/quotes.txt', 'r') as file:
        FinalQuote += choice(file.readlines())   # return a list

    #Create a line
    LastLine = "\nLots of Love and virtual hugs to "
    names = []
    with open('txtFiles/message2.txt', 'r') as file:
        names = list(set(map(lambda x: '@'+x.split('-')[0].strip(), file.readlines())))
    
    fullMessage = startLine + FinalQuote + LastLine + ' '.join(names)
    fullMessage = '\n'.join(sample(fullMessage.split('\n'), len(fullMessage.split('\n'))))
    return fullMessage
