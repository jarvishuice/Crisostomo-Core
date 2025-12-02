from datetime import datetime

import pytest
from Domain.Entities.Editorial.EditorialEntity import EditorialEntity

def test_editorial_entity_creation():
    # Creamos una instancia con todos los campos
    editorial = EditorialEntity(
        code="E001",
        name="Editorial Uno",
        description="Descripción de prueba"
    )

    assert editorial.code == "E001"
    assert editorial.name == "Editorial Uno"
    assert editorial.description == "Descripción de prueba"

def test_editorial_entity_optional_description():
    # Creamos una instancia sin descripción
    editorial = EditorialEntity(
        code="E002",
        name="Editorial Dos"
    )

    assert editorial.code == "E002"
    assert editorial.name == "Editorial Dos"
    assert editorial.description is None

def test_editorial_entity_type_check():
    editorial = EditorialEntity(
        code="E003",
        name="Editorial Tres",
        description="Otra descripción"
    )

    assert isinstance(editorial.code, str)
    assert isinstance(editorial.name, str)
    assert editorial.description is None or isinstance(editorial.description, str)
def test_serialize_with_description_and_date():
    e = EditorialEntity(code="ED001", name="Planeta", description="editorial", created_at=datetime(2025, 12, 1))
    data = e.serialize()
    assert data["description"] == "EDITORIAL"
    assert "T" in data["created_at"]

def test_serialize_without_description_and_date():
    e = EditorialEntity(code="ED002", name="Santillana")
    data = e.serialize()
    assert "description" not in data or data["description"] is None
    assert "created_at" not in data or data["created_at"] is None