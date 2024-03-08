from modules.get_config import cargar_configuracion,guardar_configuracion
from modules.get_password import generar_contrasena
from modules.get_hash import generar_hash
import getpass
import os

# Asegurarse de que la carpeta config existe
config_folder = 'config'
if not os.path.exists(config_folder):
    os.makedirs(config_folder)

def main():
    tag = input("Introduce el tag del sitio: ")
    private_key=getpass.getpass("Introduce tu private key para este tag: ")
    configuracion = cargar_configuracion(tag, private_key)

    if configuracion:
        print("Configuración cargada.")
        modificar = input("¿Deseas modificar la configuración existente? (Y/n): ")
        if modificar.lower() != 'y':
            master_key = getpass.getpass("Introduce tu master key: ")
            hash = generar_hash(configuracion['tag'], configuracion['private_key'], master_key)
            password = generar_contrasena(hash, configuracion['use_char'], configuracion['password_length'])
            print(f"Tu contraseña generada es: {password}")
            return
    else:
        print("No se encontró configuración previa o hubo un error al cargarla.")
    
    # Si no hay configuración previa o el usuario desea modificarla:
    master_key = getpass.getpass("Introduce la master key: ")
    print("Introduce los caracteres a usar: \n")
    use_char = input("Ejemplo: m=[A-Z] n=[a-z] 0=[0-9] s=[$-%)()] c=[Aa0%] ")
    password_length = int(input("Introduce la longitud de la contraseña: "))
    
    
    
    guardar_configuracion(tag, private_key, master_key, use_char, password_length)
    #generar hash de semilla de contraseña
    hash = generar_hash(tag,private_key,master_key)
    # Generar y mostrar la nueva contraseña
    password = generar_contrasena(hash, use_char, password_length)
    print(f"Tu contraseña generada es: {password}")

main()