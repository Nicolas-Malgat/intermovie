def prediction(self, id):
    """Predict the popularity of a movie, using its tconst.

    Args:
        id ([str]): tconst (like tt000001)
    """
    # *********** DEBUT DE LA PREPARATION DES DONNEES DE REFERENCE *********
    # Récupération des données de la BDD.
    dataset = #DATAFRAME_GLOBAL
    # Vérification des valeurs nulles :
    print('NOMBRE DE VALEURS NULLES :\n', dataset.isnull().sum())
    print('*******************')
    # *********** FIN DE LA PREPARATION DES DONNEES DE REFERENCE *********


    # *********** DEBUT REGRESSION LOGISTIQUE **********
    # création de tableaux de features et cibles
    x = #df caractéristiques sans popularité
    y = #df popularités (à partir d'un nb de votes)

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
    x_movie = #df des caractéristiques d'un film sans pop
    x_movie = sc.transform(x_movie)
    y_movie = classifier.predict(x_movie)

    # Seulement pour vérifier la valeur.
    # pop_movie = #valeur réelle de la pop du film qu'on test

    print('popularité estimée de la musique : ', y_movie)
    print('popularité réelle de la musique : ', pop_movie)
    precision = accuracy_score(pop_movie, y_movie)
    print('Précision du test : ', precision)
    # *********** FIN REGRESSION LOGISTIQUE **********

return y_movie