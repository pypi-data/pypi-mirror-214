def list():
    print(f"1 - list() \n"
          f"2 - list_1()\n"
          f"3 - list_2()\n"
          f"4 - pasos_1()\n"
          f"5 - pasos_2()\n"
          f"6 - carga1()\n"
          f"7 - hold1()\n"
          f"8 - norm1()\n"
          f"9 - ini1()\n"
          f"10 - fordw1()\n"
          f"11 - cost1()\n"
          f"12 - grad1()\n"
          f"13 - fmin1()\n"
          f"14 - unroll1()\n"
          f"15 - pred1()\n"
          f"16 - carga2()\n"
          f"17 - rank2()\n"
          f"18 - cost2()\n"
          f"19 - grad2()\n"
          f"20 - fmin2()\n"
          f"21 - recom2()\n"
          f"22 - simi2()\n"
          f"23 - km2()\n"
          f"24 - checkG2()\n")


def list_1():
    print(f"1 - pasos_1()\n"
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
          )


def list_2():
    print(f"1 - pasos_2()\n"
          f"2 - carga2()\n"
          f"3 - rank2()\n"
          f"4 - cost2()\n"
          f"5 - grad2()\n"
          f"6 - fmin2()\n"
          f"7 - recom2()\n"
          f"8 - simi2()\n"
          f"9 - km2()\n"
          f"10 - checkG2()\n")


def pasos_1():
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


def pasos_2():
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
    string = '''\t\t\t\t# Cargar los datos 
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
                # Obtenemos los datos del X_training con la función sample
                X_training = X.sample(round(percentage * len(X)))

                # Utilizamos los mismos indices de X_training para y_training
                y_training = y.iloc[X_training.index]

                # Utilizamos los índices que no estén en X_training para los tests
                X_test = X.iloc[~X.index.isin(X_training.index)]
                y_test = y.iloc[~y.index.isin(y_training.index)]

                # Reseteamos los índices
                X_training = X_training.reset_index(drop=True)
                y_training = y_training.reset_index(drop=True)
                X_test = X_test.reset_index(drop=True)
                y_test = y_test.reset_index(drop=True)

                # Transformamos todos a numpy para poder trabajas con ellos más adelante
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
                  mean = np.mean(X_training, axis=0)
                  std = np.mean(X_training, axis=0)

                  X_normalizado = list()

                  for i in range(len(X_training)):
                  X_normalizado.append((X_training[i] - mean) / std)

                  return X_normalizado, mean, std
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


def forwd():
    string = '''
            def forward(theta1, theta2, theta3, X):
                #Variables necesarias
                m = len(X)
                ones = np.ones((m, 1))

                #Calculamos las activaciones añadiendole la bias después
                a1 = np.hstack((ones, X))

                a2 = sigmoid(a1 @ theta1.T)
                a2 = np.hstack((ones, a2))

                a3 = sigmoid(a2 @ theta2.T)
                a3 = np.hstack((ones, a3))

                #a4 es la hipótesis y no necesitará la bias
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

                #Variable útil más adelante
                m = len(X)

                #Obtenemos las thetas:
                inicio = 0
                fin = hidden_layer_size1 * (input_layer_size+1)
                theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size+1), order='F')
                inicio = fin
                fin = fin + (hidden_layer_size2*(hidden_layer_size1+1))
                theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1+1), order='F')
                inicio = fin
                theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2+1), order='F')

                #Obtenemos la hipótesis con la última activación que nos da el forward
                a1, a2, a3, h = forward(theta1,theta2,theta3,X)

                #Transformamos y en el DataFrame por columnas que necesitamos
                #y = y.to_numpy()
                y_d = pd.get_dummies(y.flatten())

                #Calculamos el coste
                #Para cuando y=1
                temp1 = np.multiply(y_d, np.log(h))
                #Para cuando y=0
                temp2 = np.multiply(1-y_d, np.log(1-h))
                #Suma de ambas
                temp3 = np.sum(temp1 + temp2)

                #Coste final
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
                #Obtenemos las thetas:
                inicio = 0
                fin = hidden_layer_size1 * (input_layer_size+1)
                initial_theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size+1), order='F')
                inicio = fin
                fin = fin + (hidden_layer_size2*(hidden_layer_size1+1))
                initial_theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1+1), order='F')
                inicio = fin
                initial_theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2+1), order='F')

                #Variables útiles:
                m = len(y)

                #y = y.to_numpy()
                y_d = pd.get_dummies(y.flatten())

                a1, a2, a3, a4 = forward(initial_theta1,initial_theta2, initial_theta3, X)

                #Obtenemos las delta minúscula
                d4 = a4 - y_d

                d3 = np.multiply(np.dot(d4, initial_theta3), np.multiply(a3, 1-a3))
                d2 = np.multiply(np.dot(d3[:,1:], initial_theta2), np.multiply(a2, 1 - a2))

                #Le quitamos la bias a las delta minúscula para poder calcular las Delta mayúscula
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
            maxiter = 15
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
                # Obtenemos las thetas
                inicio = 0
                fin = hidden_layer_size1 * (input_layer_size + 1)
                theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size + 1), order='F')
                inicio = fin
                fin = fin + (hidden_layer_size2 * (hidden_layer_size1 + 1))
                theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1 + 1), order='F')
                inicio = fin
                theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2 + 1), order='F')

                # Obtenemos la hipótesis con a4
                a1, a2, a3, a4 = forward(theta1, theta2, theta3, X)

                # Devolvemos el que más valor tenga en la hipótesis
                return np.argmax(a4, axis=1)
      '''
    print(string)


def carga2():
    string = '''
            ### Carga de datos
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
            ranking_peliculas(Y, R, n,movie_idx)

            # Funcion
            def ranking_peliculas(Y, R, movie_idx):
                n_movies = Y.shape[0]
                Yval = np.zeros((n_movies, 1))
                Ymean = np.zeros((n_movies, 1))

                for i in range(n_movies):
                    idx = np.where(R[i, :] == 1)[0] # Esta linea devuelve los indices de las columnas donde la fila i de R tiene el valor 1
                    Yval[i] = len(idx)              # R[i, :] lo que hace es recorrer las filas de la matriz con i, mientras que los dos puntos (:) devuelve las columnas
                    Ymean[i] = Y[i, idx].mean()     # osea devuelve el vector que contiene las columnas

                idxYval = np.argsort(Yval, axis=0)[::-1]
                idxYmean = np.argsort(Ymean, axis=0)[::-1]

                print(f"Primeras {n} peliculas mejor valoradas (con nº de vistas)")
                for i in range(n):
                    print(f"{i} Nº {idxYmean[i]} con {Ymean[int(idxYmean[i])]} puntos, valorada {int(Yval[int(idxYmean[i])])} veces "
                          f"({movie_idx[int(idxYmean[i])]})")
      '''
    print(string)


def cost2():
    string = '''
            # Main
            Theta = np.zeros((features, n_users))
            usuarios = 4
            peliculas = 5
            num_features = 3

            X_sub = X[:peliculas, :num_features]
            Theta_sub = Theta[:num_features, :usuarios]
            Y_sub = Y[:peliculas, :usuarios]
            R_sub = R[:peliculas, :usuarios]

            params = np.hstack((np.ravel(X_sub, order='F'), np.ravel(Theta_sub, order='F')))
            lambda_param = 0

            J_cost = cobaCostFuncReg(params, Y_sub, R_sub, num_features, lambda_param)
            print(f"Coste inicial: {J_cost}")

            # Funcion
            def cobaCostFuncReg(params, Y, R, num_features, lambda_param):
                n_movies = Y.shape[0]
                n_users = Y.shape[1]

                X = np.reshape(params[:n_movies * num_features], (n_movies, num_features), 'F')
                Theta = np.reshape(params[n_movies * num_features:], (num_features, n_users), 'F')

                error = np.multiply(np.dot(X, Theta) - Y, R)
                error_cuadratico = np.power(error, 2)
                J_sin_reg = (1/2) * np.sum(error_cuadratico)

                J_con_reg = J_sin_reg + ((lambda_param/2) * np.sum(np.power(X, 2))) + ((lambda_param/2) * np.sum(np.power(Theta, 2)))

                return J_con_reg

      '''
    print(string)


def grad2():
    string = '''
            # Main
            grad = cobaGradientFuncReg(params, Y_sub, R_sub, num_features, lambda_param)
            print(f"Gradiente {grad}")

            # Funcion
            def cobaGradientFuncReg(params, Y, R, num_features, lambda_param):
                n_movies = Y.shape[0]
                n_users = Y.shape[1]

                X = np.reshape(params[:n_movies * num_features], (n_movies, num_features), 'F')
                Theta = np.reshape(params[n_movies * num_features:], (num_features, n_users), 'F')

                error = np.multiply(np.dot(X, Theta) - Y, R)
                Theta_grad = np.dot(X.T, error) + (lambda_param * Theta)
                X_grad = np.dot(error, Theta.T) + (lambda_param * X)

                grad = np.hstack((np.ravel(X_grad, order='F'), np.ravel(Theta_grad, order='F')))

                return grad
      '''
    print(string)


def fmin2():
    string = '''
            features = 10
            lambda_param = 1.5

            Theta_rand = np.random.rand(features, n_users) * (2*0.12)
            params = np.hstack((np.ravel(X, order='F'), np.ravel(Theta_rand, order='F')))

            fmin_cg = opt.fmin_cg(maxiter=200, f=cobaCostFuncReg, x0=params, fprime=cobaGradientFuncReg, args=(Y, R, features, lambda_param))

            X_fmin = np.reshape(fmin_cg[:n_movies * features], (n_movies, features), 'F')
            Theta_fmin = np.reshape(fmin_cg[n_movies * features:], (features, n_users), 'F')
      '''
    print(string)


def recom2():
    string = '''
            # Main
            user = 2
            num_recomendacion = 5
            recomendacionUsuario(X, Theta, Y, R, user, num_recomendacion, movie_idx)

            # Funcion
            def recomendacionUsuario(X, Theta, Y, R, user, num_recomendacion, movie_idx):
                prediccion = np.dot(X, Theta)
                n_movies = Y.shape[0]

                res_user = np.zeros((n_movies, 1))
                for i in range(n_movies):
                    res_user[i, 0] = np.where(R[i, user] == 0, prediccion[i, user], 0)

                idx = np.argsort(res_user, axis=0)[::-1]

                print(f'Las mejores {num_recomendacion} recomendaciones para el usuario {user}:')
                for i in range(num_recomendacion):
                    j = int(idx[i])
                    print(f"Tasa de predicción {str(float(res_user[j]))} para la película {movie_idx[j]}")
      '''
    print(string)


def simi2():
    string = '''
            def similares(i,num,X):
                   buscar = X[i]
                   X = np.delete(X, i, axis=0)
                   norma = np.linalg.norm(X - buscar, axis=1)
                   idx = np.argsort(norma, axis=0)
                   res = idx[:num]
                   return res
      '''
    print(string)


def km2():
    string = '''
            k = 3
            max_iters = 200
            random_initial_centroids = kMeansInitCentroids(X, 3)
            centroids, idx = runKmeans(X, random_initial_centroids, max_iters)
            print("Centroids: ", centroids)
      '''
    print(string)

