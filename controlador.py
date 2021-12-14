from pmfs import DistribucionDeProbabilidadFactory

class DistribucionesC(object):	
	def __init__(self):
		pass

	def getDistribucion(self, tipo, args):
		#parsear args a un diccionario de acuerdo al tipo
		if(tipo=="Poisson"):
			dict={'l':  args.get('l', type=int) }
		elif tipo == "Binomial" or tipo == "BinomialNegativa":
			dict={'p':  args.get('p', type=float), 'n': args.get('n', type=int) }	
		elif tipo == "Normal":
			dict={'loc': args.get('loc', type=int), 'scale': args.get('scale', type=int) }
		elif tipo == "Exponencial":
			dict={'scale': args.get('scale', type=int)}
		else:
			#si ocurre un error devolver error
			return "ocurrio un error"

		#caso contrario continuar con el factory
		factory=DistribucionDeProbabilidadFactory()
		f=factory.getDistribucion(tipo, dict)		
		#results=f.getProbability(3)
		results=f.getSample( args.get('cardinality', type=int) )
		return results