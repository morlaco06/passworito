import random

def generar_contrasena(hash, use_char, password_length):
    random.seed(hash)
    caracteres = ''
    if 'm' in use_char:
        caracteres += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if 'n' in use_char:
        caracteres += 'abcdefghijklmnopqrstuvwxyz'
    if '0' in use_char:
        caracteres += '0123456789'
    if 's' in use_char:
        caracteres += '!@#$%^&*()'
    if 'c' in use_char:  # Para 'cualquiera'
        caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()'
    
    return ''.join(random.choice(caracteres) for _ in range(password_length))
