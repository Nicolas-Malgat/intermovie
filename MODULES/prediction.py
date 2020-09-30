import pandas as pd

from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import sklearn
from sklearn import metrics
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt


class IntermoviePrediction:

    def predict(self, global_dataset, id):
        """Predict the popularity of a movie, using its tconst.

        Args:
            global_dataset ([dataframe]): dataframe with all the movies features
            id ([str]): tconst (like tt000001)
        """
        # *********** DEBUT DE LA PREPARATION DES DONNEES DE REFERENCE *********
        # global_dataset =  pd.util.hash_pandas_object(global_dataset[['actors', 'genres', 'producer', 'writer', 'composer', 'region']], encoding='utf8')
        global_dataset = global_dataset[['actors', 'genres', 'producer', 'writer', 'composer', 'region']].astype(float)
        # Vérification des valeurs nulles :
        # print('NOMBRE DE VALEURS NULLES :\n', dataset.isnull().sum())
        # print('*******************')
        # *********** FIN DE LA PREPARATION DES DONNEES DE REFERENCE *********


        # *********** DEBUT REGRESSION LOGISTIQUE **********
        # création de tableaux de features et cibles
        x = global_dataset[['actors', 'isAdult', 'startYear', 'runtimeMinutes', 'genres', 'producer', 'writer', 'composer', 'region']]
        y = global_dataset[['averageRating']]

        # Split du dataset en test et set.
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.20, random_state=0)

        # Mise à l'échelle
        sc=StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)

        # Entrainement de la Régression Logistique (modèle).
        classifier=LogisticRegression()
        classifier.fit(x_train, y_train)

        # Prédiction sur le test
        y_pred = classifier.predict(x_test)

        # Sélection des valeurs d'une musique à tester.
        x_movie = global_dataset[global_dataset.index==id]
        x_movie = sc.transform(x_movie)
        y_movie = classifier.predict(x_movie)

        # Seulement pour vérifier la valeur.
        pop_movie = x_movie.averageRating

        print('popularité estimée de la musique : ', y_movie)
        print('popularité réelle de la musique : ', pop_movie)
        precision = accuracy_score(pop_movie, y_movie)
        print('Précision du test : ', precision)
        # *********** FIN REGRESSION LOGISTIQUE **********

        return y_movie