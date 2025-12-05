from logging import getLogger
from typing import List, Optional

from psycopg.rows import dict_row
from typing_extensions import override
import os
from Config.Settings import Settings
from Domain.Entities.Book.BookEntity import BookEntity
from Domain.Entities.Book.BookReadEntity import BookReadEntity
from Domain.IDAO.Book.IBookDAO import IBookDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster


class BookDAO(IBookDAO):
    def __init__(self, db: PostgreSQLPoolMaster = None):
        self.db = PostgreSQLPoolMaster.get_instance()
        self.logger = getLogger("AppLogger")
    @override
    async def get_by_author(self, code: str) -> List[BookReadEntity]:
        query = """
                                     SELECT b.code, b."name" as name_book, b.description,
                                     b.knowledge_area, b.sub_area, b.category, b.editorial_code,
                                     b.uploaded_by, b.created_at, b.author, b.proccess_img,
                                     c."name"  as area_name, s."name"  as subarea_name,ca."name" as category_name,
                                     e."name" as editorial_name,au.first_name || ' ' || au.last_name AS fullname_user,
                                     a."name" as name_author
                                     from public.book b
                                     inner join dewey_classification c  on c.cod = b.knowledge_area 
                                     left join dewey_classification s
                                     on s.cod = b.sub_area
                                     left join dewey_classification ca on ca.cod = b.category 
                                     inner join editorial e  on e.code = b.editorial_code 
                                     inner join app_user au on au.cod = b.uploaded_by 
                                     inner join author a on a.cod = b.author
                                     where b.author = %s
                                     order by b."name" DESC


                                     """
        params = (code,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchall()

            books: List[BookReadEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"libros leidos correctamente: {len(books)} en el author {code} ")
            return books

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros por author: {e}")
            return []

    @override
    async def get_by_user(self, code: str) -> List[BookReadEntity]:
        query = """
                                             SELECT b.code, b."name" as name_book, b.description,
                                             b.knowledge_area, b.sub_area, b.category, b.editorial_code,
                                             b.uploaded_by, b.created_at, b.author, b.proccess_img,
                                             c."name"  as area_name, s."name"  as subarea_name,ca."name" as category_name,
                                             e."name" as editorial_name,au.first_name || ' ' || au.last_name AS fullname_user,
                                             a."name" as name_author
                                             from public.book b
                                             inner join dewey_classification c  on c.cod = b.knowledge_area 
                                             left join dewey_classification s
                                             on s.cod = b.sub_area
                                             left join dewey_classification ca on ca.cod = b.category 
                                             inner join editorial e  on e.code = b.editorial_code 
                                             inner join app_user au on au.cod = b.uploaded_by 
                                             inner join author a on a.cod = b.author
                                             where b.uploaded_by = %s
                                             order by b."name" DESC


                                             """
        params = (code,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchall()

            books: List[BookReadEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"libros leidos correctamente: {len(books)} en el usuario {code} ")
            return books

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros: {e}")
            return []



    @override
    async def getBooksNoneImgPreview(self) -> List[str]:
        query = """
                                select code from book b where b.proccess_img =false 


                                       """

        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query)
                    rows = await cur.fetchall()

            books: List[str] = [
                row.get("code") for row in rows
            ]

            self.logger.info(f"libros sin imagenes de previsualizacion leidas  correctamente: {len(books)}  ")
            return books

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros sin imagemnnes: {e}")
            return []

    @override
    async def checkImg(self, cod) -> bool:
        query = """
                   UPDATE book
                   SET proccess_img = true
                   WHERE code = %s
               """
        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (cod,))
                    await conn.commit()  # Muy importante para que el cambio quede guardado

            self.logger.info(f"Libro {cod} marcado como procesado")
            return True

        except Exception as e:
            self.logger.error(f"Error marcando libro {cod} como procesado: {e}")
            return False

    @override
    async def get_by_category(self, category: str) -> List[BookReadEntity]:

        query = """
                               SELECT b.code, b."name" as name_book, b.description,
                               b.knowledge_area, b.sub_area, b.category, b.editorial_code,
                               b.uploaded_by, b.created_at, b.author, b.proccess_img,
                               c."name"  as area_name, s."name"  as subarea_name,ca."name" as category_name,
                               e."name" as editorial_name,au.first_name || ' ' || au.last_name AS fullname_user,
                               a."name" as name_author
                               from public.book b
                               inner join dewey_classification c  on c.cod = b.knowledge_area 
                               left join dewey_classification s
                               on s.cod = b.sub_area
                               left join dewey_classification ca on ca.cod = b.category 
                               inner join editorial e  on e.code = b.editorial_code 
                               inner join app_user au on au.cod = b.uploaded_by 
                               inner join author a on a.cod = b.author
                               where b.category = %s
                               order by b."name" DESC
                               

                               """
        params = (category,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchall()

            books: List[BookReadEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"libros leidos correctamente: {len(books)} en la category {category} ")
            return books

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros: {e}")
            return []

    @override
    async def all(self, page_size: int = 100, page: int = 1) -> List[BookReadEntity]:
        offset = (page - 1) * page_size
        query = """
                        SELECT b.code, b."name" as name_book, b.description,
                        b.knowledge_area, b.sub_area, b.category, b.editorial_code,
                        b.uploaded_by, b.created_at, b.author, b.proccess_img,
                        c."name"  as area_name, s."name"  as subarea_name,ca."name" as category_name,
                        e."name" as editorial_name,au.first_name || ' ' || au.last_name AS fullname_user,
                        a."name" as name_author
                        from public.book b
                        inner join dewey_classification c  on c.cod = b.knowledge_area 
                        left join dewey_classification s
                        on s.cod = b.sub_area
                        left join dewey_classification ca on ca.cod = b.category 
                        inner join editorial e  on e.code = b.editorial_code 
                        inner join app_user au on au.cod = b.uploaded_by 
                        inner join author a on a.cod = b.author
                        order by b."name" DESC
                        LIMIT %s OFFSET %s;
                        
                        """
        params = (page_size, offset,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchall()

            books: List[BookReadEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"libros leidos correctamente: {len(books)} ")
            return books

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros: {e}")
            return []

    @override
    async def get_by_subarea(self, subArea: str) -> List[BookReadEntity]:
        query = """
                                       SELECT b.code, b."name" as name_book, b.description,
                                       b.knowledge_area, b.sub_area, b.category, b.editorial_code,
                                       b.uploaded_by, b.created_at, b.author, b.proccess_img,
                                       c."name"  as area_name, s."name"  as subarea_name,ca."name" as category_name,
                                       e."name" as editorial_name,au.first_name || ' ' || au.last_name AS fullname_user,
                                       a."name" as name_author
                                       from public.book b
                                       inner join dewey_classification c  on c.cod = b.knowledge_area 
                                       left join dewey_classification s
                                       on s.cod = b.sub_area
                                       left join dewey_classification ca on ca.cod = b.category 
                                       inner join editorial e  on e.code = b.editorial_code 
                                       inner join app_user au on au.cod = b.uploaded_by 
                                       inner join author a on a.cod = b.author
                                       where b.sub_area = %s
                                       order by b."name" DESC


                                       """
        params = (subArea,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchall()

            books: List[BookReadEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"libros leidos correctamente: {len(books)} en la subarea {subArea} ")
            return books

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros: {e}")
            return []

    @override
    async def get_by_code(self, code: str) -> Optional[BookReadEntity]:

        query = """
                                                     SELECT b.code, b."name" as name_book, b.description,
                                                     b.knowledge_area, b.sub_area, b.category, b.editorial_code,
                                                     b.uploaded_by, b.created_at, b.author, b.proccess_img,
                                                     c."name"  as area_name, s."name"  as subarea_name,ca."name" as category_name,
                                                     e."name" as editorial_name,au.first_name || ' ' || au.last_name AS fullname_user,
                                                     a."name" as name_author
                                                     from public.book b
                                                     inner join dewey_classification c  on c.cod = b.knowledge_area 
                                                     left join dewey_classification s
                                                     on s.cod = b.sub_area
                                                     left join dewey_classification ca on ca.cod = b.category 
                                                     inner join editorial e  on e.code = b.editorial_code 
                                                     inner join app_user au on au.cod = b.uploaded_by 
                                                     inner join author a on a.cod = b.author
                                                     where b.code = %s 
                                                     


                                                     """
        params = (code,
                  )
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchone()

                book = self._map_row_to_entity(rows)

            self.logger.info(f"libros coneguido  ")
            return book

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros: {e}")
            return None

    @override
    async def search(self, param: str) -> List[BookReadEntity]:
        paramPst = f"%{param}%"
        query = """
                                               SELECT b.code, b."name" as name_book, b.description,
                                               b.knowledge_area, b.sub_area, b.category, b.editorial_code,
                                               b.uploaded_by, b.created_at, b.author, b.proccess_img,
                                               c."name"  as area_name, s."name"  as subarea_name,ca."name" as category_name,
                                               e."name" as editorial_name,au.first_name || ' ' || au.last_name AS fullname_user,
                                               a."name" as name_author
                                               from public.book b
                                               inner join dewey_classification c  on c.cod = b.knowledge_area 
                                               left join dewey_classification s
                                               on s.cod = b.sub_area
                                               left join dewey_classification ca on ca.cod = b.category 
                                               inner join editorial e  on e.code = b.editorial_code 
                                               inner join app_user au on au.cod = b.uploaded_by 
                                               inner join author a on a.cod = b.author
                                               where b."name" ilike %s or description ilike %s 
                                               order by b."name" DESC


                                               """
        params = (paramPst,
                  paramPst,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchall()

            books: List[BookReadEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"libros buscados correctamente: {len(books)} en la category {param} ")
            return books

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros: {e}")
            return []

    @override
    async def save(self, book: BookEntity) -> bool:
        query = """
                      INSERT INTO public.book
                      (code, "name", description, knowledge_area, sub_area, category, 
                      editorial_code, uploaded_by, created_at, author, proccess_img)
                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, now(), %s, false);
                       """
        params = (
            book.code,
            book.name,
            book.description,
            book.knowledge_area,
            book.sub_area,
            book.category,
            book.editorial_code,
            book.uploaded_by,
            book.author,

        )

        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)

            self.logger.info(f"Libro   '{book.code}' creado correctamente")
            return True

        except Exception as e:
            self.logger.error(f"Error creando libro '{book.code}': {e}")
            return False

    @override
    async def save_pdf(self, pdf_file, cod: str) -> bool:
        se = Settings()
        pathBase = se.PDF_PATH
        os.makedirs(pathBase, exist_ok=True)
        try:
            if pdf_file.content_type != "application/pdf":
                raise ValueError("El archivo no es un PDF válido")
            book = await self.get_by_code(cod)
            if not book:
                raise Exception("El libro no existe")
            nameFile = f"{cod}.pdf"
            filePath = os.path.join(pathBase, nameFile)

            content = await pdf_file.read()
            with open(filePath, "wb") as f:
                f.write(content)
            return True

        except Exception as e:
            self.logger.error(e)
            raise e

    @override
    async def get_by_area(self, area: str) -> List[BookReadEntity]:
        query = """
                                               SELECT b.code, b."name" as name_book, b.description,
                                               b.knowledge_area, b.sub_area, b.category, b.editorial_code,
                                               b.uploaded_by, b.created_at, b.author, b.proccess_img,
                                               c."name"  as area_name, s."name"  as subarea_name,ca."name" as category_name,
                                               e."name" as editorial_name,au.first_name || ' ' || au.last_name AS fullname_user,
                                               a."name" as name_author
                                               from public.book b
                                               inner join dewey_classification c  on c.cod = b.knowledge_area 
                                               left join dewey_classification s
                                               on s.cod = b.sub_area
                                               left join dewey_classification ca on ca.cod = b.category 
                                               inner join editorial e  on e.code = b.editorial_code 
                                               inner join app_user au on au.cod = b.uploaded_by 
                                               inner join author a on a.cod = b.author
                                               where b.knowledge_area = %s
                                               order by b."name" DESC


                                               """
        params = (area,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params)
                    rows = await cur.fetchall()

            books: List[BookReadEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"libros leidos correctamente: {len(books)} en la area {area} ")
            return books

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los libros: {e}")
            return []

    def _map_row_to_entity(self, row) -> BookReadEntity:
        return BookReadEntity(
            # Campos heredados de BookEntity
            code=row["code"],
            name=row["name_book"],
            description=row.get("description"),
            knowledge_area=row.get("knowledge_area"),
            sub_area=row.get("sub_area"),
            category=row.get("category"),
            editorial_code=row.get("editorial_code"),
            uploaded_by=row.get("uploaded_by"),
            created_at=row.get("created_at"),
            author=row.get("author"),
            process_img=row.get("proccess_img"),  # tu columna se llama proccess_img en SQL

            # Campos adicionales del BookReadEntity
            knowledge_area_name=row.get("area_name"),
            sub_area_name=row.get("subarea_name"),
            category_name=row.get("category_name"),
            editorial_name=row.get("editorial_name"),
            fullname_user=row.get("fullname_user"),
            author_name=row.get("name_author")
        )
