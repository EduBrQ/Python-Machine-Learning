import numpy as np
from flask import Flask, abort, jsonify, request
import pickle as pickle

import numpy as np
import base64

from flask import Flask, request, render_template, make_response
from sklearn.externals import joblib
from io import BytesIO
from skimage import io as skio
from skimage.transform import resize

##############################################
###CARREGO MEU MODELO DE APRENDIZAGEM AQUI####
my_knn = pickle.load(open('analytics_folder/knn.pkl', 'rb'))
app = Flask(__name__)

##############################################
################ -API HOME - #################
@app.route('/')

def display_gui():
    return render_template('template.html')

###############################################
############# -ROTA DE TESTE - ################
@app.route("/users/<string:username>")

def hello_world(username=None):
    return("Hello {}!".format(username))

###############################################
############# -ROTA DE TESTE - ################
# ROTA PARA ACESSAR OS GRAFICOS
@app.route('/graficos')

def graficos():
    return ("PLOTA AQUI OS GRAFICOS A PARTIR DOS DADOS ENVIADOS")
    
###############################################

# ROTA (POST) QUE RECEBE OS ATRIBUTOS ESPERADOS DO MODELO DE APRENDIZAGEM DEFINIDO E RETORNA A PREDIÇÃO FEITA POR ELE
@app.route('/api', methods=['POST'])

def make_predict(): #10.0.0.102
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            predict_request = [data['Batimentos'], data['Calorias']]
            
        except ValueError:
            return jsonify("Por favor, coloque um valor para batimentos e calorias: ")
        
    predict_request = np.array(predict_request)
    predict_request = predict_request.reshape(1,-1)

    y_hat = my_knn.predict(predict_request) #retorna o resulta em JSON

    output = [y_hat[0]]
    
    #return jsonify(my_knn.predict(predict_request).tolist()) #Transforma o resultado JSON em uma lista
                   
    def result(m):
        if m[0] == 0:
            return "Sua Pressão está normal"
        
        elif m[0] == 1:
            return "Sua Pressão está muito Baixa"
        
        elif m[0] == 2:
            return "Sua Pressão está muito Alta"
   
    output = result(output)
    return jsonify(results=output)
###############################################

if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=33)

