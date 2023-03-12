import matplotlib.pyplot as plt #Chargement de la bibliothèque afin de tracer et visualiser de la data
import utils.data_statistics as stat

def printPie (dataframe) : #Fonction qui va permettre la visualisation du camembert
    opinions = [stat.countPositiveOpinions(dataframe), stat.countNegativeOpinions(dataframe)] 
    plt.pie(opinions, labels = ['Opinions positives', 'Opinions négatives'], autopct = lambda opinion: str(round(opinion, 2)) + '%', colors = ['green', 'red'])
    plt.title("Opinion générale")

def printHist(dataframe) : #Fonction qui va permettre la visualisation de l'histogramme.
    misses = [miss for miss in stat.listOfTopics(dataframe)]

    #Nous avons éliminer les miss ce dessous de manière pas très efficace mais nous n'avons pas trouvé un autre moyen de le faire. 
    misses.remove("loire ")
    misses.remove("les miss ")
    misses.remove("miss réunion ")
    misses.remove("miss alsace ")
    misses.remove("la rousse ")
    plt.xticks(rotation = "vertical")

    #Les deux lignes ci-dessous permettent la création de l'histoigramme avec les couleurs rouge et vert. 
    plt.bar(misses, [stat.countPositiveOpinionsOn(dataframe, miss) for miss in misses], color = "green", width = 0.5)
    plt.bar(misses, [-stat.countNegativeOpinionsOn(dataframe, miss) for miss in misses], color = "red", width = 0.5)

def printPieMiss (dataframe, nameOfMiss) :
    opinions = [stat.countPositiveOpinionsOn(dataframe, nameOfMiss), stat.countNegativeOpinionsOn(dataframe, nameOfMiss)] 
    plt.pie(opinions, labels = ['Opinions positives', 'Opinions négatives'], autopct = lambda opinion: str(round(opinion, 2)) + '%', colors = ['green', 'red'])
    plt.title("Opinions sur " + nameOfMiss)