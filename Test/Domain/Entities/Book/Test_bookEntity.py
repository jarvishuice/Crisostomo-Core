import pytest
from datetime import datetime
from Domain.Entities.Book.BookEntity import BookEntity

def test_create_book_entity_all_fields():
    now = datetime.now()
    book = BookEntity(
        code="B123",
        name="Libro Test",
        description="Descripción Test",
        knowledge_area="Área Test",
        sub_area="SubÁrea Test",
        category="Categoría Test",
        editorial_code="E123",
        uploaded_by="User1",
        created_at=now,
        author="Autor Test",
        process_img=True
    )

    assert book.code == "B123"
    assert book.name == "Libro Test"
    assert book.description == "Descripción Test"
    assert book.knowledge_area == "Área Test"
    assert book.sub_area == "SubÁrea Test"
    assert book.category == "Categoría Test"
    assert book.editorial_code == "E123"
    assert book.uploaded_by == "User1"
    assert book.created_at == now
    assert book.author == "Autor Test"
    assert book.process_img is True

def test_create_book_entity_optional_fields():
    book = BookEntity(
        code="B124",
        name="Libro sin descripción",
        knowledge_area="Área",
        sub_area="SubÁrea",
        category="Cat",
        editorial_code="E124",
        uploaded_by="User2",
        author="Autor2"
    )

    assert book.description == "sin descripción"
    assert book.process_img is False
    assert book.created_at is None

def test_serialize_book_entity():
    now = datetime(2025, 12, 2, 20, 0, 0)
    book = BookEntity(
        code="B125",
        name="Libro Serialize",
        knowledge_area="Área",
        sub_area="SubÁrea",
        category="Cat",
        editorial_code="E125",
        uploaded_by="User3",
        author="Autor3",
        created_at=now
    )

    serialized = book.serialize()
    assert serialized["code"] == "B125"
    assert serialized["created_at"] == now.isoformat()
