import pytest
from datetime import datetime
from Domain.Entities.Author.AuthorEntity import AuthorEntity

def test_create_author_all_fields():
    now = datetime.now()
    author = AuthorEntity(
        cod="A123",
        name="Gabriel Huice",
        description="Autor de prueba",
        created_at=now,
        updated_at=now
    )

    assert author.cod == "A123"
    assert author.name == "Gabriel Huice"
    assert author.description == "Autor de prueba"
    assert author.created_at == now
    assert author.updated_at == now

def test_create_author_required_fields_only():
    author = AuthorEntity(name="Solo Nombre")

    assert author.cod is None
    assert author.name == "Solo Nombre"
    assert author.description is None
    assert author.created_at is None
    assert author.updated_at is None

def test_serialize_author_all_fields():
    now = datetime(2025, 12, 2, 20, 0, 0)
    author = AuthorEntity(
        cod="A456",
        name="Autor Test",
        description="Descripción Test",
        created_at=now,
        updated_at=now
    )

    serialized = author.serialize()
    assert serialized["cod"] == "A456"
    assert serialized["name"] == "Autor Test"
    assert serialized["description"] == "Descripción Test"
    assert serialized["created_at"] == now.isoformat()
    assert serialized["updated_at"] == now.isoformat()

