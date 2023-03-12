# coding=utf-8
# On précise l'encodage pour éviter les erreurs d'accents, typiques dans la langue française et nombreux dans les tweets du corpus

"""
Ce fichier contient des fonctions d'analyses statistiques sur un tableau de données (de type pandas ici) donné. Toutes ces fonctions n'ont pas
été effectivement utilisées, mais pourraient l'être dans une prochaine version du code !
À de nombreux endroits, on utilise la fonction itertuples() qui permet d'itérer sur les lignes du tableau de données (chaque ligne est donnée
sous forme de tuple, d'où le nom).
"""

def countTweets (dataframe) : # Renvoie le nombre de tweets du corpus
    numberOfLigns = dataframe.shape[0]
    return numberOfLigns

def countTopics (dataframe) : # Renvoie le nombre de sujets différents du corpus. Attention : cette fonction est sensible à la casse.
    numberOfTopics = 0
    topicSet = set()
    for topicDict in list(dataframe['Annotation']) :
        for topic in topicDict['topics'] :
            topicSet.add(topic['name'])
    numberOfTopics = len(topicSet)
    return numberOfTopics

def listOfTopics (dataframe) : # Renvoie l'ensemble des sujets du corpus. Attention : cette fonction est sensible à la casse.
    setOfTopics = set()
    for tweet in dataframe.itertuples() :
        for topicOfTheTweet in tweet[3]["topics"] :
            setOfTopics.add(topicOfTheTweet["name"])
    return setOfTopics

def countPositiveOpinions (dataframe) : # Tout est dans le titre ! Compte le nombre d'opinions positives général, peu importe les sujets
    count = 0
    for ligne in dataframe.itertuples() :
        for topic in ligne[3]["topics"] :
            if topic["opinion"] == 'positive' :
                count += 1
    return count

def countPositiveOpinionsOn (dataframe, nameOfTopic) : # Compte le nombre d'opinions positives étant donné un sujet passé en argument
    count = 0
    for ligne in dataframe.itertuples() :
        for topic in ligne[3]["topics"] :
            if topic["name"] == nameOfTopic and topic["opinion"] == 'positive' :
                count += 1
    return count

def countNegativeOpinions (dataframe) : 
    count = 0
    for ligne in dataframe.itertuples() :
        for topic in ligne[3]["topics"] :
            if topic["opinion"] == 'negative' :
                count += 1
    return count

def countNegativeOpinionsOn (dataframe, nameOfTopic) :
    count = 0
    for ligne in dataframe.itertuples() :
        for topic in ligne[3]["topics"] :
            if topic["name"] == nameOfTopic and topic["opinion"] == 'negative' :
                count += 1
    return count

def sizeOfPositiveKeywords (dataframe) : # Renvoie la taille du vocabulaire des mots positifs du corpus de tweets.
    positiveKeywords = set()
    for ligne in dataframe.itertuples() :
        positiveKeywords = positiveKeywords.union(set(ligne[3]["positive_keywords"]))
    return len(positiveKeywords)

def printPositiveKeywords (dataframe) : # La même fonction que la précédente mais retourne l'ensemble des mots positifs au lieu de les compter
    positiveKeywords = set()
    for ligne in dataframe.itertuples() :
        positiveKeywords = positiveKeywords.union(set(ligne[3]["positive_keywords"]))
    return positiveKeywords

def linkOpinionsAndTopics (dataframe) : # Lie chaque sujet du corpus à son nombre d'opinions positives et négatives.
    topicsRated = {}
    for topic in listOfTopics(dataframe) :
        topicsRated[topic] = [countPositiveOpinionsOn(dataframe, topic), countNegativeOpinionsOn(dataframe, topic)]
    return topicsRated
