from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Entities.Book.BookEntity import BookEntity
from Domain.Entities.Book.BookReadEntity import BookReadEntity


class IBookDAO(ABC):
    """
    Interfaz que define el contrato para el acceso a datos de libros (Books).
    Forma parte de la capa Infrastructure dentro de una arquitectura limpia.

    Esta interfaz expone métodos para:
    - Consultar libros por categorías, subáreas y código.
    - Realizar búsquedas generales.
    - Guardar libros y sus archivos PDF asociados.
    """

    @abstractmethod
    async def get_by_category(self, category: str) -> List[BookReadEntity]:
        """
        Obtiene todos los libros pertenecientes a una categoría específica.

        Parámetros:
            category (str): Nombre de la categoría que se desea consultar.

        Retorna:
            List[BookReadEntity]: Lista de libros coincidentes.
        """
        pass

    @abstractmethod
    async def get_by_subarea(self, subArea: str) -> List[BookReadEntity]:
        """
        Obtiene todos los libros filtrados por una subárea de conocimiento.

        Parámetros:
            subArea (str): Subárea que se desea consultar.

        Retorna:
            List[BookReadEntity]: Lista de libros que pertenecen a la subárea.
        """
        pass

    @abstractmethod
    async def get_by_area(self, area: str) -> List[BookReadEntity]:
        """
        Obtiene todos los libros filtrados por una area de conocimiento.

        Parámetros:
            area (str): Subárea que se desea consultar.

        Retorna:
            List[BookReadEntity]: Lista de libros que pertenecen a la subárea.
        """
        pass

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[BookReadEntity]:
        """
        Busca un libro por su código único (clave primaria).

        Parámetros:
            code (str): Código único del libro.

        Retorna:
            Optional[BookReadEntity]: El libro si existe, de lo contrario None.
        """
        pass

    @abstractmethod
    async def search(self, param: str) -> List[BookReadEntity]:
        """
        Realiza una búsqueda general utilizando un parámetro flexible.
        Puede buscar por nombre, descripción, categoría, etc.

        Parámetros:
            param (str): Cadena de texto para realizar la búsqueda.

        Retorna:
            List[BookReadEntity]: Lista de coincidencias encontradas.
        """
        pass

    @abstractmethod
    async def all(self, page_size: int = 100, page: int = 0) -> List[BookReadEntity]:
        """
        Realiza una búsqueda general utilizando un parámetro flexible.
        Puede buscar por nombre, descripción, categoría, etc.

        Parámetros:
            page_size (int): limite de regisrtros.
            page (int): pagina .

        Retorna:
            List[BookReadEntity]: Lista libros encontradas.
        """
        pass

    @abstractmethod
    async def save(self, book: BookEntity) -> bool:
        """
        Guarda un nuevo libro en la base de datos.

        Parámetros:
            book (BookEntity): Entidad de libro que contiene los datos a guardar.

        Retorna:
            bool: True si se guardó correctamente, False si ocurrió un error.
        """
        pass

    @abstractmethod
    async def save_pdf(self, pdf_file, code: str) -> bool:
        """
        Guarda el archivo PDF asociado a un libro.

        Este método no es asíncrono porque generalmente se usa para guardar
        el archivo directamente en el filesystem o en un bucket, no en la BD.

        Parámetros:
            pdf_file: Archivo PDF (bytes, File-like o UploadFile.file).

        Retorna:
            bool: True si el archivo fue guardado exitosamente.
        """
        pass

    @abstractmethod
    async def getBooksNoneImgPreview(self) -> List[str]:
        """
        extrae  todos los librois que no tengan imagenes de previsualizacion.

        Retorna:
            List[BookEntity]: todas los libros que no tenga inmagenes de previsaulza
        """
        pass

    @abstractmethod
    async def checkImg(self, cod) -> bool:
        pass
