from flask import Flask, render_template, request, jsonify
from controlador import DistribucionesC

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(__name__)

@app.route("/")
def home():
	return render_template("home.html")

#A route to return a particular book given an id value
@app.route('/api/proabilidad/ditribuciones', methods=['GET', 'POST'])
def getDistribucion():

    if 'tipo' in request.args:
    #tipo = request.form.get('tipo', type=str)
        tipo = request.args['tipo']
    else:
        return jsonify("Error: No eligio un tipo de distribucion de Probabilidad")
    
    dist=DistribucionesC()
    results = dist.getDistribucion(tipo, request.form) #request.args

    return jsonify(results)

if __name__ == "__main__":
	app.run()	#app.run(deug=True)