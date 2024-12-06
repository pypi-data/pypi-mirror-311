import numpy as np

def saludar():	
	print("Hola wey, te saludo desde saludos.saludar()")
	
def prueba():
	print("Esto es una nueva prueba de la nueva versión 6.0")
	

#Función nueva: generar unos números en un array
def generar_array(numeros):
	return np.arange(numeros)


#Aquí, ojo... si llamo al módulo desde otro	módulo o script, se ejecutará.
#Para evitar que suceda, haremos antes:
#La variable especial __name__ almacena el nombre del script
#Esto nos servirá para hacer pruebas en el propio módulo, sin que se ejecuten fuera del mismo
#Que __name__ valga '__main__' quiere decir que el script que se está ejecutando es este mismo... si __name__ vale 'saludos', es que ha sido llamado desde otro script.
if __name__ == '__main__':
	print(generar_array(5))
	
class Saludo:
	def __init__(self):
		print("Hola, te saludo desde Saludo.__init__()")