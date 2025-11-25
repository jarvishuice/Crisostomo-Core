import hashlib

class HashGeneratorHelper:
    """
    Clase para generar hashes usando distintos algoritmos soportados por hashlib.
    """

    def __init__(self, algorithm: str = "sha256"):
        """
        Inicializa el generador con un algoritmo específico.
        Algoritmos comunes: md5, sha1, sha256, sha512, sha3_256, sha3_512
        """
        self.algorithm = algorithm.lower()
        if self.algorithm not in hashlib.algorithms_available:
            raise ValueError(f"Algoritmo {self.algorithm} no soportado")

    def generate(self, password: str) -> str:
        """
        Genera el hash del texto dado y lo devuelve en formato hexadecimal.
        """
        hash_obj = hashlib.new(self.algorithm)
        hash_obj.update(password.encode("utf-8"))
        return hash_obj.hexdigest()

