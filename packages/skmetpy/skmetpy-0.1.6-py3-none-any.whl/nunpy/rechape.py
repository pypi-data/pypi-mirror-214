def list():
    list1()
    list2()
    list3()


def list1():
    print(f"REDES NEURONALES"
          f"1 - pasos1()\n"
          f"2 - carga1()\n"
          f"3 - hold1()\n"
          f"4 - norm1()\n"
          f"5 - ini1()\n"
          f"6 - fordw1()\n"
          f"7 - cost1()\n"
          f"8 - grad1()\n"
          f"9 - fmin1()\n"
          f"10 - unroll1()\n"
          f"11 - pred1()\n"
          f"12 - nnsk1()\n"
          )


def list2():
    print(f"RECOMENDACION"
          f"1 - pasos2()\n"
          f"2 - carga2()\n"
          f"3 - rank2()\n"
          f"4 - cost2()\n"
          f"5 - grad2()\n"
          f"6 - fmin2()\n"
          f"7 - recom2()\n"
          f"8 - simi2()\n"
          f"9 - km2()\n"
          f"10 - checkG2()\n")

def list3():
    print(f"CLUSTERING"
          f"1 - pasos3()\n"
          f"2 - carga3()\n"
          f"3 - fcc3()\n"
          f"4 - compc3()\n"
          f"5 - kmean3()\n"
          f"6 - randini3()\n"
          f"7 - elbow3()\n"
          f"8 - clustsk3()\n")

def pasos1():
    print("1 - Carga de datos\n"
          "2 - Holdout\n"
          "3 - Normaliza\n"
          "4 - Inicializa las thetas (pesos)\n"
          "5 - Forward\n"
          "6 - Coste\n"
          "7 - Gradiente\n"
          "8 - Fmin\n"
          "9 - Desenrolla el fmin\n"
          "10 - Normaliza X-test\n"
          "11 - Predice\n")

def pasos2():
    print("1 - Carga de datos\n"
          "2 - Ranking de peliculas\n"
          "3 - Coste\n"
          "4 - Gradiente\n"
          "5 - Fmin\n"
          "6 - Recomendacion usuario\n"
          "7 - Peliculas similares\n"
          "8 - Kmeans\n"
          "9 - checknngradients\n")




def carga1():
    string = '''
        # Cargar los datos 
        data = pd.read_csv("drivers_behavior.csv")
        y = pd.DataFrame(data['Target'])
        X = data.drop(['Target'], axis=1)
        
        # Definición parámetros RED NEURONAL
        input_layer_size = 60
        hidden_layer_size1 = 50
        hidden_layer_size2 = 25
        num_labels = 4
    '''

    print(string)


def hold1():
    string = '''
        def holdout(X, y, percentage=0.75):
            X_training = X.sample(round(percentage * len(X)))

            y_training = y.iloc[X_training.index]

            X_test = X.iloc[~X.index.isin(X_training.index)]
            y_test = y.iloc[~y.index.isin(y_training.index)]

            X_training = X_training.reset_index(drop=True)
            y_training = y_training.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)
            y_test = y_test.reset_index(drop=True)

            X_training = X_training.to_numpy()
            y_training = y_training.to_numpy()
            X_test = X_test.to_numpy()
            y_test = y_test.to_numpy()

            return X_training, y_training, X_test, y_test
      '''

    print(string)


def norm1():
    string = '''
        def normalize(X, X_training):
            # Obtenemos la media por columnas
            mean = np.mean(X, axis=0)
            std = np.std(X, axis=0)
        
            normal = []
        
            # Calculamos por filas los nuevos valores de las X
            for i in range(X_training.shape[0]):
                x = X_training[i] - mean
                x = x / std
                normal.append(x)
        
            return normal, mean, std
      '''

    print(string)


def ini1():
    string = '''
        # Main
        theta1 = randInitializeWeights(61, 50)
        theta2 = randInitializeWeights(51, 25)
        theta3 = randInitializeWeights(26, 4)

        # Funcion
        def randInitializeWeights(capa_entrada, capa_salida):
              epsilon_init = 0.12
              W = np.random.rand(capa_salida, capa_entrada) * 2 * epsilon_init - epsilon_init
              return W
      '''

    print(string)


def forwd1():
    string = '''
        def forward(theta1, theta2, theta3, X):
            #Variables necesarias
            m = len(X)
            ones = np.ones((m, 1))

            a1 = np.hstack((ones, X))

            a2 = sigmoid(a1 @ theta1.T)
            a2 = np.hstack((ones, a2))

            a3 = sigmoid(a2 @ theta2.T)
            a3 = np.hstack((ones, a3))

            a4 = sigmoid(a3 @ theta3.T)

            return a1, a2, a3, a4
      '''

    print(string)


def cost1():
    string = '''
        # Main
        nn_params = np.hstack((theta1.ravel(order='F'), theta2.ravel(order='F'), theta3.ravel(order='F')))
        J = nnCostFunction(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X_training,
                   y_training)

        # Funcion
        def nnCostFunction(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X, y):

            m = len(X)
            inicio = 0
            fin = hidden_layer_size1 * (input_layer_size+1)
            theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size+1), order='F')
            inicio = fin
            fin = fin + (hidden_layer_size2*(hidden_layer_size1+1))
            theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1+1), order='F')
            inicio = fin
            theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2+1), order='F')

            a1, a2, a3, h = forward(theta1,theta2,theta3,X)

            y_d = pd.get_dummies(y.flatten())

            temp1 = np.multiply(y_d, np.log(h))
            temp2 = np.multiply(1-y_d, np.log(1-h))
            temp3 = np.sum(temp1 + temp2)

            J = - np.sum(temp3) / m

            return J
      '''

    print(string)


def grad1():
    string = '''
        # Main
        lambda_param = 0
        checkNNGradients(lambda_param)

        # Funcion
        def nnGradFunction(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X, y):
            inicio = 0
            fin = hidden_layer_size1 * (input_layer_size+1)
            initial_theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size+1), order='F')
            inicio = fin
            fin = fin + (hidden_layer_size2*(hidden_layer_size1+1))
            initial_theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1+1), order='F')
            inicio = fin
            initial_theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2+1), order='F')

            m = len(y)
            y_d = pd.get_dummies(y.flatten())

            a1, a2, a3, a4 = forward(initial_theta1,initial_theta2, initial_theta3, X)

            d4 = a4 - y_d
            d3 = np.multiply(np.dot(d4, initial_theta3), np.multiply(a3, 1-a3))
            d2 = np.multiply(np.dot(d3[:,1:], initial_theta2), np.multiply(a2, 1 - a2))
            d3 = d3[:,1:]
            d2 = d2[:,1:]

            delta1 = d2.T @ a1
            delta2 = d3.T @ a2
            delta3 = d4.T @ a3

            delta1 /= m
            delta2 /= m
            delta3 /= m

            delta3 = delta3.to_numpy()

            gradiente = np.hstack((delta1.ravel(order='F'), delta2.ravel(order='F'), delta3.ravel(order='F')))
            return gradiente
      '''
    print(string)


def fmin1():
    string = '''
        maxiter = 200
        nn_params = opt.fmin_cg(maxiter=maxiter, f=nnCostFunction, x0=nn_params, fprime=nnGradFunction, args=(
        input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X_training, y_training.flatten()))
      '''
    print(string)


def unroll1():
    string = '''
        inicio = 0
        fin = hidden_layer_size1 * (input_layer_size + 1)
        theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size + 1), order='F')
        inicio = fin
        fin = fin + (hidden_layer_size2 * (hidden_layer_size1 + 1))
        theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1 + 1), order='F')
        inicio = fin
        theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2 + 1), order='F')

        print('Theta1: \n', theta1)
        print('Theta2: \n', theta2)
        print('Theta3: \n', theta3)
      '''

    print(string)


def pred1():
    string = '''
        # Main
        X_test_normal = []
        for i in range(X_test.shape[0]):
          x = X_test[i] - mean
          x = x / std
          X_test_normal.append(x)

        pred = predict(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X_test_normal)
        print("Accuracy del conjunto de test: ", np.mean(pred.flatten() == y_test.flatten()) * 100)

        # Funcion
        def predict(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X):
            inicio = 0
            fin = hidden_layer_size1 * (input_layer_size + 1)
            theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size + 1), order='F')
            inicio = fin
            fin = fin + (hidden_layer_size2 * (hidden_layer_size1 + 1))
            theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1 + 1), order='F')
            inicio = fin
            theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2 + 1), order='F')

            a1, a2, a3, a4 = forward(theta1, theta2, theta3, X)

            return np.argmax(a4, axis=1)
      '''
    print(string)

def nnsk1():
    string = '''
        # Cargar los datos
        data = pd.read_csv("drivers_behavior.csv")
        y = pd.DataFrame(data['Target'])
        X = data.drop(['Target'], axis=1)
    
        # Definición parámetros RED NEURONAL
        capa_entrada = 60
        capa_oculta1 = 50
        capa_oculta2 = 25
        n_salidas = 4
    
        # Ejercicio 1: Holdout
        X_train, X_test, y_train, y_test = nn.train_test_split(X, y, train_size=0.75, random_state=42)
        print(f"X_train: {X_train}, \nX_test: {X_test}, \ny_train: {y_train}, \ny_test: {y_test}")
    
        # Ejercicio 2: Normalización
        X_train_estandarizada = sk.preprocessing.normalize(X)
        print(f"X_train_estandarizada: {X_train_estandarizada}")
    
        # Ejercicio 3: Inicialización de los pesos
        # Llamada a la función randInitializeWeights del script funcionesUtiles
        Theta1 = randInitializeWeights(capa_entrada + 1, capa_oculta1)
        Theta2 = randInitializeWeights(capa_oculta1 + 1, capa_oculta2)
        Theta3 = randInitializeWeights(capa_oculta2 + 1, n_salidas)
        nn_params = np.hstack((np.ravel(Theta1, order='F'), np.ravel(Theta2, order='F'), np.ravel(Theta3, order='F')))
    
        # Ejercicio 4: Función Forward
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        # Crea el modelo de red neuronal
        mlp = MLPClassifier(hidden_layer_sizes=(capa_oculta1, capa_oculta2), activation='logistic', max_iter=200)
        # Entrena el modelo
        mlp.fit(X_train_scaled, y_train)
    
        # Ejercicio 5: Predicción
        X_test_scaled = scaler.transform(X_test)
        predictions = mlp.predict(X_test_scaled)
        print(f"Prediccion: {predictions}")
        precision = sk.metrics.accuracy_score(y_test, y_pred=predictions)
        print(f"Precision: {precision}")
    '''
    print(string)

def carga2():
    string = '''
        ### Carga de datos
        print('Realizando carga de datos.')
        movies = sio.loadmat("ex8_movies.mat")
        Y = movies['Y']  # [n_items, n_users]
        R = movies['R']  # [n_items, n_users]
        n_movies = Y.shape[0]
        n_users = Y.shape[1]
    
        params_data = sio.loadmat('ex8_movieParams.mat')
        X = params_data['X']
        Theta = params_data['Theta']
        Theta = Theta.T
        features = X.shape[1]
    
        # Títulos de las películas en el mismo orden que las matrices Y y R
        movie_idx = {}
        f = open('movie_ids.txt', encoding='ISO-8859-1')
        for line in f:
            tokens = line.split(' ')
            tokens[-1] = tokens[-1][:-1]
            movie_idx[int(tokens[0]) - 1] = ' '.join(tokens[1:])
    
        print("Títulos de las películas en el mismo orden que las matrices Y y R. Se muestran 10 del principio.")
        for i in range(10):
            print('{0} - Nombre: {1}.'.format(str(i), movie_idx[i]))
      '''
    print(string)


def rank2():
    string = '''
        # Main
        ranking(Y, R, movie_idx, 5)
        # Funcion
        def ranking(Y, R, movies_idx, num_peliculas):
            n_movies = Y.shape[0]
            peliculas = list()
            num_valoraciones = list()
            peliculas_recomendadas = list()
        
            for i in range(n_movies):
                peliculas.append(np.where(R[i, :] == 1)[0])
                num_valoraciones.append(len(peliculas[i]))
                peliculas_recomendadas.append(np.mean(Y[i, peliculas[i]]))
        
            indices_ordenados_valoracion = np.argsort(num_valoraciones, axis=0)[::-1]
            indices_ordenados_media = np.argsort(peliculas_recomendadas, axis=0)[::-1]
        
            print(f"Primeras {num_peliculas} películas mejor valoradas (Ordenadas por valoración):")
            for i in range(num_peliculas):
                print(f"{i} Nº {indices_ordenados_valoracion[i]} con {peliculas_recomendadas[indices_ordenados_valoracion[i]]} puntos valorada {num_valoraciones[indices_ordenados_valoracion[i]]} ({movies_idx[indices_ordenados_valoracion[i]]})")
        
            print(f"\nPrimeras {num_peliculas} peliculas mejor valoradas (Ordenadas por media):")
            for i in range(num_peliculas):
                print(
                    f"{i} Nº {indices_ordenados_media[i]} con {peliculas_recomendadas[indices_ordenados_media[i]]} puntos valorada {num_valoraciones[indices_ordenados_media[i]]} ({movies_idx[indices_ordenados_media[i]]})")
      '''
    print(string)


def cost2():
    string = '''
        # Main
        lambda_param = 0
        sub_users = 4
        sub_movies = 5
        sub_features = 3
    
        Theta = np.zeros((features, n_users))
    
        X_sub = X[:sub_movies, :sub_features]
        Theta_sub = Theta[:sub_features, :sub_users]
        Y_sub = Y[:sub_movies, :sub_users]
        R_sub = R[:sub_movies, :sub_users]
    
        params = np.hstack((np.ravel(X_sub, order='F'), np.ravel(Theta_sub, order='F')))
    
        coste_sub = cobaCostFuncReg(params, Y_sub, R_sub, sub_features, lambda_param)
        print("Coste:", coste_sub)
    
        # Funcion
        def cobaCostFuncReg(params, Y, R, num_features, lambda_param):
            n_movies = Y.shape[0]
            n_users = Y.shape[1]
        
            X = np.reshape(params[:n_movies * num_features], (n_movies, num_features), 'F')
            Theta = np.reshape(params[n_movies * num_features:], (num_features, n_users), 'F')
        
            error = np.multiply(np.dot(X, Theta) - Y, R)
            error_cuadratico = np.power(error, 2)
            J_sin_Reg = (1/2) * np.sum(error_cuadratico)
        
            J_con_reg = J_sin_Reg + ((lambda_param/2) * np.sum(np.power(X, 2))) + ((lambda_param/2) * np.sum(np.power(Theta, 2)))
        
            return J_con_reg

      '''
    print(string)


def grad2():
    string = '''
        # Main
        gradiente_sub = cobaGradientFuncReg(params, Y_sub, R_sub, sub_features, lambda_param)
            print("Gradiente:", gradiente_sub)
        # Funcion
        def cobaGradientFuncReg(params, Y, R, num_features, lambda_param):
            n_movies = Y.shape[0]
            n_user = Y.shape[1]
        
            X = np.reshape(params[:n_movies * num_features], (n_movies, num_features), 'F')
            Theta = np.reshape(params[n_movies * num_features:], (num_features, n_user), 'F')
        
            error = np.multiply(np.dot(X, Theta) - Y, R)
            Theta_grad = np.dot(X.T, error) + (lambda_param * Theta)
            X_grad = np.dot(error, Theta.T) + (lambda_param * X)
        
            grad = np.hstack((np.ravel(X_grad, order='F'), np.ravel(Theta_grad, order='F')))
        
            return grad
      '''
    print(string)


def fmin2():
    string = '''
        lambda_param = 1.5
        maxiter = 200
        X_rand = np.random.rand(n_movies, features) * (2 * 0.12)
        Theta_rand = np.random.rand(features, n_users) * (2 * 0.12)
        params = np.hstack((np.ravel(X_rand, order='F'), np.ravel(Theta_rand, order='F')))
    
        fmin = opt.fmin_cg(maxiter=maxiter, f=cobaCostFuncReg, x0=params, fprime=cobaGradientFuncReg, args=(Y, R, features, lambda_param))
    
        X = np.reshape(fmin[:n_movies * features], (n_movies, features), 'F')
        Theta = np.reshape(fmin[n_movies * features:], (features, n_users), 'F')
      '''
    print(string)


def recom2():
    string = '''
        # Main
        usuario = 2
            num_peliculas = 5
            recomendacionUsuario(X, Theta, Y, R, usuario, num_peliculas, movie_idx)
        # Funcion
        def recomendacionUsuario(X, Theta, Y, R, usuario, num_peliculas, movie_idx):
            prediccion = np.dot(X, Theta)
            n_movies = Y.shape[0]
            pelicula_recomendada = list()
        
            for i in range(n_movies):
                pelicula_recomendada.append(np.where(R[i, usuario] == 0, prediccion[i, usuario], 0))
        
            print(pelicula_recomendada)
        
            indices_pelicula_recomendada = np.argsort(pelicula_recomendada, axis=0)[::-1]
        
            print(f"Las mejores {num_peliculas} recomendaciones para el usuario {usuario}:")
            for i in range(num_peliculas):
                print(f"Tasa de predicción {pelicula_recomendada[indices_pelicula_recomendada[i]]} para la pelicula {movie_idx[indices_pelicula_recomendada[i]]}")
      '''
    print(string)


def simi2():
    string = '''
        # Main
        pelicula = 0
            similares(X, pelicula, num_peliculas)
        # Funcion
        def similares(X, pelicula, num_peliculas):
            datos_pelicula = X[pelicula]
            X = np.delete(X, pelicula, axis=0)
            distancia = np.linalg.norm(X - datos_pelicula, axis=0)
            indices_ordenados = np.argsort(distancia, axis=0)[::-1]
        
            print(f"{num_peliculas} películas parecidas a la nº {pelicula}, titulada {movie_idx[pelicula]}")
            for i in range(num_peliculas):
                print(f"Película nº {indices_ordenados[i]}, titulada {movie_idx[indices_ordenados[i]]}")
      '''
    print(string)


def km2():
    string = '''
        K = 3
        max_iters = 200
        centroids = kMeansInitCentroids(X, K)
        centroids, idx = runKmeans(X, centroids, max_iters, True)
      '''
    print(string)

def pasos3():
    print("1 - Carga de datos\n"
          "2 - Find closets centroids\n"
          "3 - Compute centroids\n"
          "4 - Kmeans\n"
          "5 - Ini centroids random\n"
          "6 - Elbow\n")

def carga3():
    string = '''
        X = sio.loadmat("ex7data2.mat")['X']
        print(X.shape)
        for i in range(len(X)):
            plt.scatter(X[i][0], X[i][1], color="blue")
        plt.show()
    '''
    print(string)

def fcc3():
    string = '''
        # Main
        print("Finding closest centroids\n")
        idx = findClosestCentroids(X, initial_centroids)
        print("Closest centroids for the first 3 examples: ", idx[0:3])
        
        # Funcion
        def findClosestCentroids(x, initial_centroids):
            closest_centroids = list()
        
            for i in range(len(x)):
                distancia_minima = float('inf')
                for j in range(len(initial_centroids)):
                    distancia = np.sqrt(np.sum(np.power((x[i] - initial_centroids[j]), 2)))
        
                    if distancia <= distancia_minima:
                        indice_cercano = j
                        distancia_minima = distancia
                closest_centroids.append(indice_cercano)
        
            return closest_centroids
    '''
    print(string)

def compc3():
    string = '''
            # Main
            centroids = computeCentroids(X, idx, K)
            
            # Funcion
            def computeCentroids(X, idx, k):
                centroides = list()
            
                for i in range(k):
                    puntos_en_cluster = list()
                    for j in range(len(X)):
                        if i == idx[j]:
                            puntos_en_cluster.append(X[j])
                    media = np.mean(puntos_en_cluster, axis=0)
                    centroides.append(media)
            
                return centroides
    '''
    print(string)


def kmean3():
    string = '''
            # Main
            max_iters = 10
            centroids, idx = runKmeans(X, initial_centroids, max_iters, plot=True)
            
            # Funcion
            def runKmeans(X, initial_centroids, max_iters, plot=True):
                centroids_finales = initial_centroids
                indices_centroides_finales = list()
                K = len(initial_centroids)
            
                for i in range(max_iters):
                    indices_centroides_finales = findClosestCentroids(X, centroids_finales)
                    centroids_finales = computeCentroids(X, indices_centroides_finales, K)
            
                if plot:
                    plotClusters(X, indices_centroides_finales, centroids_finales, initial_centroids)
            
                return centroids_finales, indices_centroides_finales
                '''
    print(string)


def randini3():
    string = '''
            # Main
            random_initial_centroids = kMeansInitCentroids(X, K)
            centroids, idx = runKmeans(X, random_initial_centroids, max_iters, plot=True)
            
            # Funcion
            def kMeansInitCentroids(X, K):
                centroids = []
            
                for i in range(K):
                    indice_aleatorio = np.random.randint(0, len(X)-1, size=K)
                    centroids.append(X[indice_aleatorio[i]])
            
                return centroids
    '''
    print(string)

def elbow3():
    string = '''
            # Main
            elbowMethod(X)
            
            # Funcion
            def elbowMethod(X):
                costes = []
            
                for K in range(1,11):
                    coste = 0
                    initial_centroids = kMeansInitCentroids(X, K)
                    centroids, indice_centroid = runKmeans(X, initial_centroids, max_iters=10, plot=False)
            
                    # h es cada elemento de X
                    for j in range(len(X)):
                        coste += np.sum(np.power((X[j] - centroids[indice_centroid[j]]), 2))
                    costes.append(coste)
            
                num_clusters = [i for i in range(1,11)]
                plt.plot(num_clusters, costes)
                plt.show()
    '''
    print(string)

def clustsk3():
    string = '''
            # Main
            X, _ = make_blobs(n_samples=200, centers=4, random_state=0)
            inertias = []
        
            # Determinar el número óptimo de clusters
            for k in range(1, 11):
                kmeans = KMeans(n_clusters=k, init='k-means++')
                kmeans.fit(X)
        
            inertias.append(kmeans.inertia_)
        
            plt.plot(range(1, 11), inertias, marker='o')
            plt.xlabel('Número de Clusters (K)')
            plt.ylabel('Inercia')
            plt.title('Método del Codo')
            plt.show()
        
            kneedle = KneeLocator(range(1, 11), inertias, curve='convex', direction='decreasing')
            optimal_k = kneedle.knee
        
            print("Número óptimo de clusters (k):", optimal_k)
    '''
    print(string)
