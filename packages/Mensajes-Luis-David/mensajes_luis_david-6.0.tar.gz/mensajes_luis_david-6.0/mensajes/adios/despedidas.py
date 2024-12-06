def despedir():
	print("Adiós, me despido desde despedidas.despedir()")
	
#Aquí, ojo... si llamo al módulo desde otro	módulo o script, se ejecutará.
#Para evitar que suceda, haremos antes:
#La variable especial __name__ almacena el nombre del script
#Esto nos servirá para hacer pruebas en el propio módulo, sin que se ejecuten fuera del mismo
#Que __name__ valga '__main__' quiere decir que el script que se está ejecutando es este mismo... si __name__ vale 'saludos', es que ha sido llamado desde otro script.
if __name__ == '__main__':
	saludar()
	
class Despedida:
	def __init__(self):
		print("Adiós, me despido desde Despedida.__init__()")