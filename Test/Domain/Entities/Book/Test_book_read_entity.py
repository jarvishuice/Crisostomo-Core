import pytest
from datetime import datetime
from Domain.Entities.Book.BookReadEntity import BookReadEntity

def test_create_book_read_entity():
    now = datetime.now()
    book_read = BookReadEntity(
        code="BR123",
        name="Libro Read",
        description="Desc",
        knowledge_area="Área",
        sub_area="SubÁrea",
        category="Cat",
        editorial_code="E126",
        uploaded_by="User4",
        author="Autor4",
        created_at=now,
        category_name="Categoría Nombre",
        knowledge_area_name="Área Nombre",
        sub_area_name="SubÁrea Nombre",
        editorial_name="Editorial Nombre",
        fullname_user="Usuario Completo",
        author_name="Autor Nombre"
    )

    assert book_read.category_name == "Categoría Nombre"
    assert book_read.knowledge_area_name == "Área Nombre"
    assert book_read.sub_area_name == "SubÁrea Nombre"
    assert book_read.editorial_name == "Editorial Nombre"
    assert book_read.fullname_user == "Usuario Completo"
    assert book_read.author_name == "Autor Nombre"

def test_serialize_book_read_entity():
    now = datetime(2025, 12, 2, 20, 0, 0)
    book_read = BookReadEntity(
        code="BR124",
        name="Libro Serialize Read",
        knowledge_area="Área",
        sub_area="SubÁrea",
        category="Cat",
        editorial_code="E127",
        uploaded_by="User5",
        author="Autor5",
        created_at=now,
        category_name="Cat Nombre",
        knowledge_area_name="Área Nombre",
        sub_area_name="SubÁrea Nombre",
        editorial_name="Editorial Nombre",
        fullname_user="User Completo",
        author_name="Autor Nombre"
    )

    serialized = book_read.serialize()
    assert serialized["created_at"] == now.isoformat()
    assert serialized["code"] == "BR124"
