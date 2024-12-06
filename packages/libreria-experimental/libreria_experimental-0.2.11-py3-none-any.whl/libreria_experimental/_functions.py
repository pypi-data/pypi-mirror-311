from typing import Callable
from sympy import *
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from statistics import mean, pstdev
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit


def ajuste_linear(x:NDArray[np.float64],y:NDArray[np.float64],errorx:NDArray[np.float64] | float=0,errory:NDArray[np.float64] | float=0,xlabel:str='',ylabel:str='',titulo:str='',color:str='orange',colorerr:str='black',colordot:str='red'):
    """
    Realiza un ajuste lineal de los datos x e y introducidos en la función, y devuelve la pendiente, la ordenada en origen y el coeficiente de correlación al cuadrado.
    """
    n=len(x)
    xm=np.mean(x)
    ym=np.mean(y)
    sx=np.sum(x)
    sy=np.sum(y)
    sxy=np.sum(x*y)
    sx2=np.sum(x**2)
    sy2=np.sum(y**2)
    m=(n*sxy-sx*sy)/(n*sx2-sx**2)
    b=(sx2*sy-sx*sxy)/(n*sx2-sx**2)
    xi=symbols('xi')
    f=b+m*xi
    fx=lambdify(xi,f)
    fi=fx(x)
    numerador=n*sxy-sx*sy
    raiz1=np.sqrt(n*sx2-sx**2)
    raiz2=np.sqrt(n*sy2-sy**2)
    r=numerador/(raiz1*raiz2)
    r2=r**2
    r2_porcentaje=np.around(r2*100,2)
    sigma=(sum((y-m*x-b)**2)/(len(x)-2))**(1/2)
    errorm=(((len(x)*sigma**2)/(len(x)*sum(x**2)-(sum(x))**2)))**(1/2)
    errorn=((sigma**2*sum(x**2))/(len(x)*sum(x**2)-(sum(x))**2))**(1/2)
    m1='m='+str(m)+'+/-'+str(errorm)
    b1='n='+str(b)+'+/-'+str(errorn)
    plt.plot(x,y,'o',label='Datos')
    plt.plot(x,fi,color=color,label='Ajuste')
    plt.errorbar(x,y,color=colorerr,yerr=errory,fmt='.')
    plt.errorbar(x,y,color=colorerr,xerr=errorx,fmt='.')
    for i in range(0,n,1):
        y0=np.min([y[i],fi[i]])
        y1=np.max([y[i],fi[i]])
        plt.vlines(x[i],y0,y1, color=colordot,
            linestyle ='dotted')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.show
    f1='f='+str(f)
    r21='r^2='+str(r2)
    return f1,m1,b1,r21

def ajuste_magico(x:NDArray[np.float64],y:NDArray[np.float64],funcion:Callable[...,float] ,parametros:list[str],p0:NDArray[np.float64],xerror:NDArray[np.float64]|float=0,yerror:NDArray[np.float64]|float=0,xlabel:str='',ylabel:str='',titulo:str='',color:str='r-',colorerr:str='black'):
    """
    Toma una función como argumento, por lo tanto es necesario definirla antes de realizar el ajuste. 
    Realiza un ajuste de cualquier función y devuelve los parámetros de la misma con su error correspondiente.
    """
    popt,pcov=curve_fit(funcion,x,y,p0)
    min_x=x[0]
    for i in x[1:]:
        min_x=min(min_x,i)
    max_x=x[-1]
    for i in x[1:]:
        max_x=max(max_x,i)        
    x_ajuste=np.linspace(min_x,max_x)
    plt.figure()
    plt.plot(x,y,'o',label='Datos')
    plt.plot(x_ajuste,funcion(x_ajuste,*popt),color,label='Ajuste')
    plt.errorbar(x,y,color=colorerr,yerr=yerror,fmt='.')
    plt.errorbar(x,y,color=colorerr,xerr=xerror,fmt='.')
    plt.legend(loc='best')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.tight_layout()
    pstd=np.sqrt(np.diag(pcov))
    nombres_de_param=parametros
    print('Parámetros:')
    for i, param in enumerate(popt):
        print('{:s}={:f}+-{:f}'.format(nombres_de_param[i],param,pstd[i]/2))
def properrores(variables:list[Symbol],f:Symbol,errores:list[float],valores1:NDArray[np.float64]):
    """
    Es necesario definir de manera simbólica antes de realizar la propagación de errores.
    En los valores se ha de utilizar un array bidimensional (una matriz).
    Realiza la propagación de errores de una función dadas unas variables y unos valores con sus respectivos errores, para devolver la funcion de error y los valores de estos.
    """
    ecuacion=0
    errorindirecto1=[]
    valores=valores1.T
    for i in range(len(variables)):
        ecuacion+=abs(diff(f,variables[i]))*errores[i]
    print(ecuacion)
    eqlatex=latex(ecuacion)
    print(eqlatex)
    for j in range(len(valores)):
        errorindirecto2=ecuacion.subs(dict(zip(variables,valores[j])))
        errorindirecto1.append(errorindirecto2)
    return np.array(errorindirecto1)

