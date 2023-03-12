# coding=utf-8
"""
Nous allons utiliser dans cette fonctionnalité TextBlob qui est un outil très puissant pour permettre d'analyser des sentiments dans une phrase très rapidement.
Entrée: fichier en .txt
Sortie: dictionnaires
"""

from textblob import TextBlob
from textblob import Blobber
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import load_dataframe as load
import matplotlib.pyplot as plt 

"""
Cette fonction permet d'abord permet d'extraire le vocabulaire d'un ensemble de tweets en récupérant les mots, uniques et lemmatisés.
Ensuit, elle retire de la liste les doublons.
"""

def tweetToWords (tweets) : #tweets est une chaine de caracteres
    stopwordsList = open("stopwords.txt", "r")
    stopwordsListContent = stopwordsList.readlines()

    for word in stopwordsListContent :
        stopwordsListContent[stopwordsListContent.index(word)] = word.strip('\n')

    texte = ""
    
    texte = TextBlob(tweets)
    mots = texte.words
    doublons = []
    for mot in mots :
        mot.lemmatize()
        if mot in doublons or (mot.lower() in stopwordsListContent) :
            mots.remove(mot)
        else :
            doublons += [mot]
    return mots

"""
Cett fonction supprime de la liste obtenue les mots fréquents à partir d'un fichier stop-words. 
"""

def cleanStopwords (tweets) :
    stopwordsList = open("stopwords.txt", "r")
    stopwordsListContent = stopwordsList.readlines()

    for word in stopwordsListContent :
        stopwordsListContent[stopwordsListContent.index(word)] = word.strip('\n')

    texte = ""
    for tweet in tweets :
        texte += tweet
    texte = TextBlob(texte)
    mots = texte.words
    for mot in mots :
        mot.lemmatize()
        if mot.lower() in stopwordsListContent :
            mots.remove(mot)
    return mots

"""
Cette fonction compte le nombre de fois ou le mot est mentionné. 
"""

def corpus_frequent_words (dataframe) :
    texte = ""
    frequencies = {}
    for ligne in dataframe.itertuples() :
        texte += ligne[2] + " "
    texte = texte.lower()
    for word in tweetToWords(texte) :
        frequencies[word] = cleanStopwords(texte).count(word)
    return frequencies

"""
Cette fonction affiche l'histogramme des 40 mots les plus fréquents dans notre corpus.
"""

def printMostUsedWords(dataframe) :
    frequencies = corpus_frequent_words(dataframe)
    mostUsedWords = sorted(frequencies.items(), key=lambda t: t[1])
    wordsToPlot = []
    theirFrequencies = []
    for i in range(1, 41) :
        wordsToPlot.append(mostUsedWords[-i][0])
        theirFrequencies.append(mostUsedWords[-i][1])
    plt.xticks(rotation = "vertical")
    plt.bar(wordsToPlot, theirFrequencies, color = "red", width = 0.5)
    plt.show()
printMostUsedWords(load.load_corpus_in_dataframe())

"""
Cette fonction crée un histogramme représentant l'analyse de l'opinion pour l'évènement à partir d'une polarité arbitraire. 
"""

def analyseOpinion (dataframe) :
    allTweets = []
    positiveTweets = []
    negativeTweets = []
    neutralTweets = []
    for ligne in dataframe.itertuples() :
        allTweets.append(ligne[2])
    for tweet in allTweets :
        blobedTweet = TextBlob(tweet)
        polarity = blobedTweet.sentiment.polarity
        if polarity > 0.3 :
            positiveTweets.append(tweet)
        elif polarity < -0.3 :
            negativeTweets.append(tweet)
        else :
            neutralTweets.append(tweet)
    print("Le pourcentage d'opinions positives est : " + str(len(positiveTweets)*100/len(allTweets)))
    print("\n")
    print("Le pourcentage d'opinions négatives est : " + str(len(negativeTweets)*100/len(allTweets)))
    print("\n")
    print("Le pourcentage d'opinions neutres est : " + str(len(neutralTweets)*100/len(allTweets)))

analyseOpinion(load.load_corpus_in_dataframe())