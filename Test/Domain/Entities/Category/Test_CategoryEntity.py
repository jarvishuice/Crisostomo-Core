import pytest
from Domain.Entities.Category.CategoryEntity import CategoryEntity  # ajusta el import según tu estructura


def test_category_serialize_full_data():
    """Debe serializar correctamente cuando todos los campos están presentes"""
    c = CategoryEntity(cod="CAT001", name="Novela", parentCod="CAT000")
    data = c.serialize()

    assert isinstance(data, dict)
    assert data["cod"] == "CAT001"
    assert data["name"] == "Novela"
    assert data["parentCod"] == "CAT000"


def test_category_serialize_empty_strings():
    """Debe manejar correctamente valores vacíos"""
    c = CategoryEntity(cod="", name="", parentCod="")
    data = c.serialize()

    assert data["cod"] == ""
    assert data["name"] == ""
    assert data["parentCod"] == ""


def test_category_serialize_type_validation():
    """Pydantic debe lanzar error si los tipos no son str"""
    with pytest.raises(ValueError):
        CategoryEntity(cod=123, name="Novela", parentCod="CAT000")
