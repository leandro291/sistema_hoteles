from bcrypt import gensalt, hashpw, checkpw

def hashear_contrasena(contrasena: str) -> str:
    bytes_contrasena = contrasena.encode('utf-8')
    salt = gensalt()
    hashed_contrasena = hashpw(bytes_contrasena, salt)

    return hashed_contrasena.decode('utf-8')

def validar_contrasena(contrasena_ingresada: str, hash_guardado) -> str:
    bytes_contrasena = contrasena_ingresada.encode('utf-8')
    bytes_hash = hash_guardado.encode('utf-8')

    return checkpw(bytes_contrasena, bytes_hash)
