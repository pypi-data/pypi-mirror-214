import random
import sqlite3
import time
print ("Bienvenido")
print("Indicaciones del juego")
print("""1)Preguntas aleatrorias de Cálculo álgebra Física circuitos proramación \n
      2) Cada respuesta de las preguntas tendran la inicial de la materia a preguntar, ejmp (matemáticas: 2x2, Respuesta: m4)\n
      3)Tenga encuenta que las respuestas saldran aleatoriamente esto quiere decir, que te podria salir en desorden las asignaturas\n
      ############################################
      Preguntas:
      CÁLCULO
      1)Derivada de 2x
      2) Derivada de 259x^2
      3) A que es igual las variables independientes en Funciones de varias variables "dependientes"

      ÁLGEBRA
      1) El dato es el valor que cada ********** asumirá en un individuo determinado
      2) Efectuar: (4x-2xy+5)-(x+xy-1)
      3) Resolver: (80-30)^2

      FÍSICA
      1)Capacidad que tiene la materia de producir trabajo en forma de movimiento, luz, calor, etc.
      2)unidad del Sistema Internacional para energía y trabajo.
      3)Forma de energía que produce efectos luminosos, mecánicos, caloríficos, químicos, etc., y que se debe a la separación o movimiento de los electrones que forman los átomos

      PROGRAMACIÓN
      1) (falso lenguaje), es una serie de normas léxicas y gramaticales parecidas a la mayoría de los lenguajes de programación, pero sin llegar a la rigidez de sintaxis de estos ni a la fluidez del lenguaje coloquial.
      2) Es el proceso por el cual la información de una fuente es convertida en símbolos para ser comunicada. 

      CIRCUITOS
      1) Suministran corriente eléctrica al circuito.
      2) Transforman la energía del circuito electrico en un trabajo útil.
      3) Permiten que circulen la corriente eléctrica.
    """)





AHORCADO = ['''
      +---+
      |   |
          |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========''']
class palabra():
    global pt
    palabras = "c2", "c518", "crango", "avariable", "a3x-3xy+6", "a2500", "fenergia", "felectricidad", "fjoule", "ceneradores", "creceptores", "cconductores", "ppseudocodio", "pcodificacion ".split()

    def base():
        print('su puntaje es: ')
        print(pt)
###############################crear base de datos##########################################33
        bass = sqlite3.connect("bass.db")
        cursor =bass.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS DATOS (nombre TEXT, puntos VARCHAR,fecha TEXT)''') 
        bass = sqlite3.connect("bass.db")
        cursor =bass.cursor()
##################################agregar datos###################################################33
        nombre=input('ingrese su nombre para guardarlo en el sistema\n')
        puntos= pt
        fecha= time.strftime("%d/%m/%y")
        lista=[(nombre,puntos,fecha)]
        #INSERT para guardar datos en la tabla dentro de la base de datos
        cursor.executemany("INSERT INTO DATOS  values (?,?,?)",lista)
        bass.commit()
        print ("Los datos fueron agregados con éxito")
        cursor.close()
        time.sleep(2)
        print()
###########################ver los datos ##################################################33
        bass=sqlite3.connect("bass.db")
        cursor=bass.cursor()
   #     consulta=("SELECT columna FROM tabla ORDER BY columna DESC")
        #fetchall este método devuelve los datos guardados en cursor.
        cursor.execute("SELECT * FROM DATOS ORDER BY puntos DESC")#seleccionar todo de datos ordenar por puntos descendientmente 
        datos=cursor.fetchmany(3)#muestra solo 3 datos de la base de datos 
        bass.commit()
        
        time.sleep(5)
        print('USUARIO  PTS  FECHA')
            
        for i in datos:#imprimir los datos de la base de datos.
            print(*i)
            
       # print(datos)
        cursor.close()
        bass.close()
        print("##############################################################")
        print ('Quieres jugar de nuevo? (Si o No)')
        return input().lower().startswith('s')
        exit
        StopIteration
####################################################################################################################333
    def buscarPalabraAleat(listaPalabras):
        palabraAleatoria = random.randint(0, len(listaPalabras) - 1)
        return listaPalabras[palabraAleatoria]
     
    def displayBoard(AHORCADO, letraIncorrecta, letraCorrecta, palabraSecreta):
        print(AHORCADO[len(letraIncorrecta)])
        print ("")
        fin = " "
        print ('Letras incorrectas:', fin)
        for letra in letraIncorrecta:
            print (letra, fin)
        print ("")
        espacio = '_' * len(palabraSecreta)
        for i in range(len(palabraSecreta)): 
            if palabraSecreta[i] in letraCorrecta:
                espacio = espacio[:i] + palabraSecreta[i] + espacio[i+1:]
        for letra in espacio: 
            print (letra, fin)
        print ("")
     
    def elijeLetra(algunaLetra):
        while True:
            print ('Adivina una letra:')
            letra = input()
            letra = letra.lower()
            if len(letra) != 1:
                print ('Introduce una sola letra.') 
            elif letra in algunaLetra:
                print ('Ya has elegido esa letra ¿Qué tal si pruebas con otra?')
       #     elif letra not in 'abcdefghijklmnopqrstkuvwxyz':
        #       print ('Elije una letra.')
            else:
                return letra
     
 #   def empezar(self):
  #      print ('Quieres jugar de nuevo? (Si o No)')
   #     return input().lower().startswith('s')
     
    pt=200
    print ('A H O R C A D O')
    letraIncorrecta = ""
    letraCorrecta = ""
    palabraSecreta = buscarPalabraAleat(palabras)
    finJuego = False
    while True:
        displayBoard(AHORCADO, letraIncorrecta, letraCorrecta, palabraSecreta)
       
        letra = elijeLetra(letraIncorrecta + letraCorrecta)
        if letra in palabraSecreta:
            letraCorrecta = letraCorrecta + letra
           
            letrasEncontradas = True
            for i in range(len(palabraSecreta)):
                if palabraSecreta[i] not in letraCorrecta:
                    letrasEncontradas = False
                    
                    exit
            if letrasEncontradas:
                print ('¡Muy bien! La palabra secreta es "' + palabraSecreta + '"! ¡Has ganado!')
                a=(len(letraIncorrecta))
                r=a*20
                pt=pt-r
                base()
         #       finJuego = True
            
        else:
            letraIncorrecta = letraIncorrecta + letra
           
            if len(letraIncorrecta) == len(AHORCADO) - 1:
                displayBoard(AHORCADO, letraIncorrecta, letraCorrecta, palabraSecreta)
                print ('¡Se ha quedado sin letras!\nDespues de ' + str(len(letraIncorrecta)) + ' letras erroneas y ' + str(len(letraCorrecta)) + ' letras correctas, la palabra era "' + palabraSecreta + '"')
     #           finJuego = True
                a=(len(letraIncorrecta))
               # b=(len(letraCorrecta))
                c=(len(palabraSecreta))
                r=a*30
                pt=pt-r
                base()
       
     #   if finJuego:
      #      if empezar():
       #         letraIncorrecta = ""
        #        letraCorrecta = ""
         #       finJuego = False
          #      palabraSecreta = buscarPalabraAleat(palabras)
           # else:
            #    exit

