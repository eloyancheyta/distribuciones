from abc import ABC, abstractmethod
import numpy as np
import math
import random
#import scipy.stats as ss
from numpy import random
#import matplotlib.pyplot as plt
#import seaborn as sns
import json


def singleton(cls):
    instances = dict()
    def wrap(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrap

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
        
class DistribucionDeProbabilidad(ABC):
    @abstractmethod
    def getProbability(self):
        pass

    @abstractmethod
    def getSample(self):
        pass

class PoissonDistribution(DistribucionDeProbabilidad):
    def __init__(self,l=5):
        self.l=l

    def getProbability(self,k):
        p=(self.l**k)*np.exp(self.l*-1)/math.factorial(k)
        return p

    def getSample(self, cardinality):
        sample=[]
        pc = self.getProbability(0)
        #print("p0 = "+str(pc))
        for i in range(cardinality):
            u=random.random()
            #print("u = "+str(u))
            k=0
            f=pc            
            while True:
                #print("k = "+str(k))
                f+=self.getProbability(k)
                #print("f = "+str(f))
                if(f>u):
                    break
                k=k+1
                #print("k = "+str(k))
                #print("")
            sample.append(k)
        return sample

#Distribución Binomial
class BinomialDistribucion(DistribucionDeProbabilidad):
    def __init__(self, p=0.9, n=10):
        self.p = p
        self.n = n

    def getProbability(self, k):
        pr=(math.factorial(self.n)/(math.factorial(k) * (math.factorial(self.n-k) ))) * (self.p**k) * (1-self.p)**(self.n-k)
        return pr

    def getSample(self, cardinality):
        sample=[]
        pc = self.getProbability(0)
        for i in range(cardinality):
            u=random.random()
            k=0
            f=pc
            while True:
                f+=self.getProbability(k)
                if(f>u):
                    break
                k=k+1
            sample.append(k)
        return sample

    def bernoulli(self):
        ri = random.random()
        if(ri <= self.p):
            return 1
        else:
            return 0

    def getSample2(self):
        exitos = 0
        for i in range(self.cardinality):
            b = self.bernoulli()
            if (b == 1):
                exitos+=1
        return exitos            

#Distribución Binomial
class BinomialDistribucionNegativa(DistribucionDeProbabilidad):
    def __init__(self, p=0.9, n=5):
        self.p = p #probabilidad de exito
        self.n = n #ensayos

    def getProbability(self, k):
        if(k > self.n or k == 0):   
            pr = 0
        else:
            pr=(math.factorial(self.n-1)/(math.factorial(self.n-k) * (math.factorial(k-1) ))) * (self.p**k) * (1-self.p)**(self.n-k)
        return pr

    def getSample(self, cardinality):
        sample=[]
        pc = self.getProbability(1)
        #print(pc)
        for i in range(cardinality):
            u=random.random()
            #print("u  = "+str(u))
            k=1
            f=pc
            while True:
                pp = self.getProbability(k)
                #print(pp)
                f+=pp
                if(f>u or k > self.n or pp == 0):
                    break
                k=k+1
            sample.append(k)
        return sample


class NormalDistribucion(DistribucionDeProbabilidad):
    def __init__(self, loc = 1, scale = 2):
        self.loc=loc
        self.scale=scale

    def getProbability(self, k):
      return k

    def getSample(self, cardinality):      
      results =  random.normal(loc=self.loc, scale=self.scale, size=cardinality)
      #sns.distplot(results, hist=False)      
      #plt.show()
      #operation = json.dumps(data, cls=NumpyEncoder)
      return json.dumps(results, cls=NumpyEncoder)    

class ExponencialDistribucion(DistribucionDeProbabilidad):
    def __init__(self, scale = 3):
        self.scale = scale    
    
    def getProbability(self, k):
        return k
        
    def getSample(self, cardinality):
        results = random.exponential(scale=self.scale, size = cardinality)
        #sns.distplot(results, hist=False)
        return json.dumps(results, cls=NumpyEncoder)    
        #plt.show()
        
@singleton
class DistribucionDeProbabilidadFactory:
    def __init__(self):
        pass

    def getDistribucion(self, type, parameters:dict):
        if type=="Poisson":
            return PoissonDistribution(parameters['l'])
        elif type=="Binomial":
            return BinomialDistribucion(parameters['p'], parameters['n'])
        elif type == "BinomialNegativa":
            return BinomialDistribucionNegativa(parameters['p'], parameters['n'])
        elif type == "Normal":
            return NormalDistribucion(parameters['loc'], parameters['scale'] )
        elif type == "Exponencial":
            return ExponencialDistribucion(parameters['scale'])
        else:
            return "Elige una Distribucion De Probabilidad Valida"