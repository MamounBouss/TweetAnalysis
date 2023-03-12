import os.path
from os import listdir
import pandas as pd

"""
Utilitaire d'accès aux données
Entrée : un fichier d'annotations au format .ann
Sortie : un dictionnaire contenant l'information sur le tweet annoté (ses sujets, l'opinion partagée sur chacun d'eux, les mots positifs
contenus dans le tweet et les mots négatifs contenus dans le tweet)
dataframe 
[ID (int)
Texte (str)
Annotation (dict
    {topics: list
        [dict
            {name: str
            opinion: str}],
    positive_keywords: list[str],
    negative_keywords: list[str]})]
"""

def read_and_load_annotations(annotationPath) :
    annotation = open(annotationPath, "r", encoding="utf-8")
    annotationContent = annotation.read()
    # Dans la suite, on formate le fichier pour le mettre sous forme d'une liste de mots (en enlevant les tabulations mais en gardant les sauts de lignes)
    annotationContent = annotationContent.replace('\t', ' ')
    annotationContent = annotationContent.replace('\n', ' \n ')
    wordsInAnnotation = annotationContent.split(' ') 
    for word in wordsInAnnotation :
        if word == '' :
            wordsInAnnotation.remove(word)

    tweetAnalysis = {"topics" : [], "positive_keywords" : [], "negative_keywords" : []}

    """
    Dans la suite, on segmente le fichier d'annotations (pour l'instant sous forme d'une liste de mots) en segments logique (identiques aux
    lignes qu'on voit quand on affiche le fichier .ann dans un éditeur de texte).
    """

    partsOfAnnotation = []
    annotation = []
    for word in wordsInAnnotation :
        if word == '\n' :
            partsOfAnnotation.append(annotation)
            annotation = []
        else :
            annotation.append(word)

    #Maintenant que la mise en forme est faite, on veut trouver les sujets du tweet correspondant à l'annotation et l'opinion partagée pour chacun d'eux

    for annotation in partsOfAnnotation :
        if "Topic" in annotation :
            nameOfTopic = ""
            for index in range(annotation.index("Topic") + 3, len(annotation)) :
                nameOfTopic += annotation[index] + " "
            nameOfTopic = nameOfTopic.lower()
            opinionAboutTopic = 'negative'
            for index in range (partsOfAnnotation.index(annotation) + 1, len(partsOfAnnotation)):
                if "Topic" in partsOfAnnotation[index] :
                    break
                if "isPositiveOpinionOn" in partsOfAnnotation[index] :
                    opinionAboutTopic = 'positive'
            tweetAnalysis["topics"] += [{'name' : nameOfTopic, 'opinion' : opinionAboutTopic}]

        """
        Dans la suite, on veut lister les mots positifs et négatifs présents dans les parties de l'annotation (contenus dans
        "Subjectiveme_positive" et parfois liés à un "Negator" quand ces mots sont à comprendre au sens de la négation)
        """

        if "Subjectiveme_positive" in annotation :
            positiveWord = annotation[-1] #Le dernier mot de "Subjectiveme_positive" est toujours le qualificatif positif non-négationné
            tweetAnalysis["positive_keywords"] += [positiveWord.lower()]

        """
        On va ensuite à la recherche d'un possible "Negator" dans les environs de l'annotation qui nous intéresse car ce dernier est toujours
        lié à son qualificatif. Remarquez la structure des blocs d'exception pour prévenir les erreurs d'index (qui peuvent arriver si
        l'annotation est dans en bout de partsOfAnnotation).
        """

        try : 
            if "Subjectiveme_positive" in annotation and "Negator" in partsOfAnnotation[partsOfAnnotation.index(annotation) - 1] :
                negativeWord = partsOfAnnotation[partsOfAnnotation.index(annotation) - 1][4] + " " + annotation[4]
                tweetAnalysis["negative_keywords"] += [negativeWord.lower()]
        except IndexError :
            continue
        try :    
            if "Subjectiveme_positive" in annotation and "Negator" in partsOfAnnotation[partsOfAnnotation.index(annotation) + 1] :
                negativWord = partsOfAnnotation[partsOfAnnotation.index(annotation) + 1][4] + " " + annotation[4]
                tweetAnalysis["negative_keywords"] += [negativWord.lower()]
        except IndexError :
            continue

    return tweetAnalysis

"""
Cette fonction prend en paramètre l'identifiant d'un tweet (entier) et renvoie en sortie le dictionnaire contenant les informations qui
nous intéressent sur ce tweet (id, texte et annotations) si elles existent, et contenant (id, False, False) sinon.
"""

def load_tweet_with_annotation(id) :
    tweetPath = './data/tweets/' + str(id)+'.txt'
    annotationPath = './data/tweets/annotations/' + str(id) + '.ann'
    tweetExists = os.path.exists(tweetPath)
    annotationExists = os.path.exists(annotationPath) 
    if (tweetExists and annotationExists) : #Le tweet existe à la fois sous forme de fichier .txt et d'annotation .ann
        tweet = open(tweetPath,'r', encoding = "utf-8")
        tweetContent = tweet.read()
        tweetInfo = {
            'id': id,
            'text': tweetContent,
            'annotation': read_and_load_annotations(annotationPath)}
    else :
        tweetInfo = {
            'id': id,
            'text': False,
            'annotation': False}
    return(tweetInfo)

"""
Cette fonction renvoie le dataframe contenant tous le corpus de tweets (au format {id, text, annotations}). Notez l'opération de nettoyage
dataframe en seconde partie de code.
"""

def load_corpus_in_dataframe():
    #D'abord, on récupère tous les IDs des fichiers d'annotations (il n'y pas bijection entre les tweets et les annotations, il faudra nettoyer les données)
    annotationsDirectory = listdir('./data/tweets/annotations')
    ids = [int(annotation.split('.')[0]) for annotation in annotationsDirectory]
    tweets = [load_tweet_with_annotation(id) for id in ids]
    textes = [tweet["text"] for tweet in tweets]
    annotations = [tweet["annotation"] for tweet in tweets]
    corpusContent = pd.DataFrame({"ID" : ids, "Texte" : textes, "Annotation" : annotations})
    
    for index in corpusContent.index : #Supprimons toutes les lignes vides du DataFrame
        if (corpusContent["Texte"][index] == False or corpusContent["Annotation"][index] == False) :
            corpusContent.drop(index, 0, inplace = True)
    return corpusContent

def cleanMiss (dataframe) :
    
    regionsDictionnary = {
        "champagne" : "Miss Champagne-Ardenne",
        "picardie" : "Miss Picardie",
        "lorraine" : "Miss Lorraine",
        "calais" : "Miss Nord Pas-de-Calais",
        "poitou" : "Miss Poitou-Charente",
        "provence" : "Miss Provence",
        "corse" : "Miss Corse",
        "guadeloupe" : "Miss Guadeloupe",
        "languedoc" : "Miss Languedoc-Roussillon",
        "roussillon" : "Miss Languedoc-Roussillon",
        "centre" : "Miss Centre-Val-de-Loire",
        "tahiti" : "Miss Tahiti",
        "normandie" : "Miss Normandie",
        "bretagne" : "Miss Bretagne",
        "alsace" : "Miss Alsace",
        "midi" : "Miss Midi-Pyrénées",
        "réunion" : "Miss Réunion",
        "aquitaine" : "Miss Aquitaine",
        "auvergne" : "Miss Auvergne",
        "bourgogne" : "Miss Bourgogne",
        "martinique" : "Miss Martinique",
        "mayotte" : "Miss Mayotte",
        "calédonie" : "Miss Nouvelle-Calédonie",
        "pays-de-la-loire" : "Miss Pays-de-la-Loire",
        "bretagne" : "Miss Bretagne",
        "île" : "Miss Île-de-France",
    }

    print(list(regionsDictionnary.values()))

    for tweet in dataframe.itertuples() :
        for topicOfTheTweet in tweet[3]["topics"] :
            for nameOfRegions in regionsDictionnary.keys() :
                if nameOfRegions in topicOfTheTweet["name"] :
                    topicOfTheTweet["name"] = regionsDictionnary[nameOfRegions]
                
            if topicOfTheTweet["name"] not in list(regionsDictionnary.values()):
                tweet[3]["topics"].remove(topicOfTheTweet)                    
    return dataframe

print(load_corpus_in_dataframe)