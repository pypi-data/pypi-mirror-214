import numpy as np

import matplotlib.pyplot as plt

import math

from math import sin,cos,sqrt,radians

from tkinter import *

from tkinter import messagebox

from datetime import date

from datetime import datetime

from datetime import timedelta





class ParOrdenado:

    def __init__(self):

               

                #---------raiz

                    

        self.raiz=Tk()

        #------------------framas

        self.miframa=Frame()

        self.miframa.pack()



        #-------------------labels



        self.milabel=Label(self.miframa,text=('Diagrama fasorial'),font=('arial',20))

        self.milabel.pack()

        self.milabel.grid(row=0,column=2,columnspan=2)



        hoy=date.today()

        self.ppp=StringVar()

        self.ppp.set(hoy)

        

        self.code1=Entry(self.miframa,text=self.ppp,width=12)

        self.code1.grid(row=1,column=4,padx=15,pady=10,sticky='w')

        self.labels=Label(self.miframa,text=('Date-->'),font=('arial',10))

        self.labels.grid(row=1,column=3,sticky='e')





        

        self.botone=Button(self.miframa,text="Graficar corrientes",width=24,height=2,command=lambda:self.graficai())

        self.botone.grid(row=10,column=1)



        self.boti=Button(self.miframa,text="Graficar voltajes",width=24,height=2,command=lambda:self.graficav())

        self.boti.grid(row=10,column=2,pady=10)



##        self.bot=Button(self.miframa,text="Graficar todo",width=24,height=2,command=lambda:self.graficall())

##        self.bot.grid(row=7,column=3,pady=10)



        self.nb=Button(self.miframa,text="Mostrar",width=12,height=2,command=lambda:self.nada())

        self.nb.grid(row=10,column=4,padx=3)

#--------------------------------------------------------------------------------------------------------------



        self.yi=StringVar()

        self.yii=StringVar()



        

        self.coda=Entry(self.miframa,text=self.yi,width=24)

        self.coda.grid(row=4,column=2,padx=20,pady=10)

        self.labelit=Label(self.miframa,text=('Digite aqui el angulo del fasor de corriente -->'))

        self.labelit.grid(row=4,column=1)



        self.coda1=Entry(self.miframa,text=self.yii,width=24)

        self.coda1.grid(row=5,column=2,padx=20,pady=10)

        self.labelit1=Label(self.miframa,text=('Digite aqui la magnitud del fasor de corriente -->'))

        self.labelit1.grid(row=5,column=1)

#-------------------------------------------------------------------------------------------------------------



        self.yp=StringVar()

        self.ypp=StringVar()



    

        self.codq=Entry(self.miframa,text=self.yp,width=24)

        self.codq.grid(row=4,column=4,padx=15,pady=10)

        self.labeliq=Label(self.miframa,text=('Digite aqui el angulo del fasor de voltaje -->'))

        self.labeliq.grid(row=4,column=3)



        self.codq=Entry(self.miframa,text=self.ypp,width=24)

        self.codq.grid(row=5,column=4,padx=15,pady=10)

        self.labeliq=Label(self.miframa,text=('Digite aqui la magnitud del fasor de voltaje -->'))

        self.labeliq.grid(row=5,column=3)

#----------------------------------------------------------

        self.raiz.mainloop()

        

    def graficai(self):

         

        self.be='Grafica de fasores de corriente'



        self.grade=float(self.yi.get())#float(input('ingrese el grado del vector'))

        x=math.radians(self.grade)

        self.mag=float(self.yii.get())#float(input('Ingrese la magnitud del vector'))

        if (self.mag<=0):

            ejemplo = ParOrdenado()

        else:

            

            if self.grade>=0 and self.grade<=300:

                co=(self.mag*sin(x))

                ca=(self.mag*cos(x))

                self.a=float(ca)# coordenada x

                self.b=float(co)#coordenada y

                self.real = float(self.a)

                self.imaginario = float(self.b)

                

                self.c=float(self.mag*cos(math.radians(self.grade+120)))# coordenada x

                self.d=float(self.mag*sin(math.radians(self.grade+120)))#coordenada y

                self.rea = float(self.c)

                self.imaginar = float(self.d)



                self.e=float(self.mag*cos(math.radians(self.grade-120)))

                self.f=float(self.mag*sin(math.radians(self.grade-120)))

                self.reas = float(self.e)

                self.imaginars = float(self.f)

                ccc=self.grade+120

                cccc=self.grade-120

                self.data=['magnitud:',self.mag,'angulo:',self.grade]

                self.date=['magnitud:',self.mag,'angulo:',ccc]

                self.dati=['magnitud:',self.mag,'angulo:',cccc]

                

                qs=np.array(self.data)

                qd=StringVar()

                qd.set(qs)

                self.co=Entry(self.miframa,text=qd,width=30)

                self.co.grid(row=6,column=3,padx=100,pady=10)

                self.laq=Label(self.miframa,text=('Datos del vector Ifa(azul) -->'))

                self.laq.grid(row=6,column=2)



                ql=np.array(self.date)

                qde=StringVar()

                qde.set(ql)

                self.co=Entry(self.miframa,text=qde,width=30)

                self.co.grid(row=7,column=3,padx=100,pady=10)

                self.laq=Label(self.miframa,text=('Datos del vector Ifc(rojo) -->'))

                self.laq.grid(row=7,column=2)



                qr=np.array(self.dati)

                qdr=StringVar()

                qdr.set(qr)

                self.co=Entry(self.miframa,text=qdr,width=30)

                self.co.grid(row=8,column=3,padx=100,pady=10)

                self.laq=Label(self.miframa,text=('Datos del vector Ifb(naranja) -->'))

                self.laq.grid(row=8,column=2)



                

            else:

                print('error')



    def nada(self):

        messagebox.showinfo('.','para visualizar grafica cierra la ventana del programa ')

        

         

    def graficav(self):

         

        self.be='Grafica de fasores de voltaje'



        self.grade=float(self.yp.get())#float(input('ingrese el grado del vector'))

        x=math.radians(self.grade)

        self.mag=float(self.ypp.get())#float(input('Ingrese la magnitud del vector'))

        if (self.mag<=0):

            ejemplo = ParOrdenado()

        else:

            

            if self.grade>=0 and self.grade<=300:

                co=(self.mag*sin(x))

                ca=(self.mag*cos(x))

                self.a=float(ca)# coordenada x

                self.b=float(co)#coordenada y

                self.real = float(self.a)

                self.imaginario = float(self.b)

                

                self.c=float(self.mag*cos(math.radians(self.grade+120)))# coordenada x

                self.d=float(self.mag*sin(math.radians(self.grade+120)))#coordenada y

                self.rea = float(self.c)

                self.imaginar = float(self.d)



                self.e=float(self.mag*cos(math.radians(self.grade-120)))

                self.f=float(self.mag*sin(math.radians(self.grade-120)))

                self.reas = float(self.e)

                self.imaginars = float(self.f)





                ccc=self.grade+120

                cccc=self.grade-120

                self.data=['magnitud:',self.mag,'angulo:',self.grade]

                self.date=['magnitud:',self.mag,'angulo:',ccc]

                self.dati=['magnitud:',self.mag,'angulo:',cccc]

                

                qs=np.array(self.data)

                qd=StringVar()

                qd.set(qs)

                self.co=Entry(self.miframa,text=qd,width=30)

                self.co.grid(row=6,column=3,padx=100,pady=10)

                self.laq=Label(self.miframa,text=('Datos del vector Van(azul) -->'))

                self.laq.grid(row=6,column=2)



                ql=np.array(self.date)

                qde=StringVar()

                qde.set(ql)

                self.co=Entry(self.miframa,text=qde,width=30)

                self.co.grid(row=7,column=3,padx=100,pady=10)

                self.laq=Label(self.miframa,text=('Datos del vector Vcn(rojo) -->'))

                self.laq.grid(row=7,column=2)



                qr=np.array(self.dati)

                qdr=StringVar()

                qdr.set(qr)

                self.co=Entry(self.miframa,text=qdr,width=30)

                self.co.grid(row=8,column=3,padx=100,pady=10)

                self.laq=Label(self.miframa,text=('Datos del vector Vbn(naranja) -->'))

                self.laq.grid(row=8,column=2)



                

               

            else:

                print('error')









               

    

def graficarComp(self):



    

    

    

    # Coordenadas del vector

    x1, y1 = self.real, self.imaginario

    x2, y2 = self.rea,  self.imaginar

    x3, y3 = self.reas, self.imaginars

   

    # Limites de la figura

    izda =(self.mag*-2) 

    dcha =(self.mag*2)

    abajo =(self.mag*-2) 

    arriba = (self.mag*2)



  

    #pinta vectores #ffeceff1



    plt.quiver([0],[0],[x1],[y1], color='blue', angles='xy', scale_units='xy', scale=1)

    plt.quiver([0],[0],[x2],[y2], color='red', angles='xy', scale_units='xy', scale=1)

    plt.quiver([0],[0],[x3],[y3], color='orange', angles='xy', scale_units='xy', scale=1)



    # origen de coordenadas

    plt.axhline(0, color='black')

    plt.axvline(0, color='black')



    #límites, etiquetas y títulos

    plt.xlim([izda, dcha ])

    plt.ylim([abajo, arriba])

    plt.xlabel('x')

    plt.ylabel('y')

    plt.title('{}'.format(self.be))

    plt.show()

   







ejemplo = ParOrdenado()

graficarComp(ejemplo)





    





