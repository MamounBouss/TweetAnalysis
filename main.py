"""
Fichier principal. À lancer depuis de la répertoire datavisualization13/ en utilisant "python main.py nomDeLaMiss".
Pour des raisons de chemins (des modules entre eux lors des imports, d'accès aux données), il faut bien se placer dans datavisualization13/ pour le lancer.
Ce fichier est un MVP accessible en ligne de commande : les arguments à spécifier sont indiqués à l'aide de la commande "python main.py -h".
"""
import sys

sys.path.append("/Applications/anaconda3/lib/python3.8/site-packages")

import matplotlib.pyplot as plt
import argparse
# Le module argparse permet d'implémenter une interface utilisateur en ligne de commande
import utils.load_dataframe as load
# Le module load_dataframe permet de charger les données et de les nettoyer au besoin
import utils.plot_data as plot
# Le module plot_data permet de gérer l'affichage visuel.
import utils.data_statistics as stat
# Le module data_statistics contient toutes les fonctions d'analyse utilent pour le traitement des données en vue de l'affichage visuel.

parser = argparse.ArgumentParser()
parser.add_argument("nameOfMiss", help = "Display a pie diagram giving the opinion about the Miss", type = str)
args = parser.parse_args()

dataframe = load.cleanMiss(load.load_corpus_in_dataframe())

"""
On travaillera avec le tableau de donneés contenant tous les tweets, duquel ont été supprimés tous les tweets ne parlant pas explicitement
d'une Miss en particulier. Voir la fonction cleanMiss du module load_data pour plus de détails.
"""

def main (nameOfMiss) :
    plt.figure(1)
    plt.subplot(221)
    plot.printHist(dataframe)
    plt.subplot(222)
    plot.printPie(dataframe)
    plt.subplot(224)
    # On n'utilise pas l'emplacement 223 pour laisser de la place à l'histogramme sur la gauche de la figure.
    plot.printPieMiss(dataframe, nameOfMiss)
    # C'est cette commande qui permet d'avoir un affichage utilisateur personnalisé, en spécifiant le nom entré en argument.
    plt.show()
    
if __name__ == '__main__':
    main(str(args.nameOfMiss))
    # On accède à l'attribut nameOfMiss contenant la chaîne de caractère entrée dans le terminal par l'utilisateur pour personnaliser l'affichage