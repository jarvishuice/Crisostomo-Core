import pytest
from datetime import date, datetime, timedelta
from Domain.Entities.Users.UserEntity import UserEntity
from pydantic import ValidationError

def test_create_user_all_fields():
    dob = date(1990, 5, 20)
    now = datetime.now()
    user = UserEntity(
        cod="U123",
        first_name="Gabriel",
        middle_name="J.",
        last_name="Huice",
        second_last_name="Padron",
        email="gabriel@test.com",
        date_of_birth=dob,
        phone_number="123456789",
        username="gabrielhuice",
        password_hash="hashed_password",
        created_at=now,
        updated_at=now
    )

    assert user.cod == "U123"
    assert user.first_name == "Gabriel"
    assert user.middle_name == "J."
    assert user.last_name == "Huice"
    assert user.second_last_name == "Padron"
    assert user.email == "gabriel@test.com"
    assert user.date_of_birth == dob
    assert user.phone_number == "123456789"
    assert user.username == "gabrielhuice"
    assert user.password_hash == "hashed_password"
    assert user.created_at == now
    assert user.updated_at == now

def test_create_user_required_fields_only():
    user = UserEntity(
        cod="U124",
        first_name="Solo",
        last_name="Nombre",
        email="solo@test.com",
        username="solonombre",
        password_hash="hash"
    )

    assert user.middle_name is None
    assert user.second_last_name is None
    assert user.date_of_birth is None
    assert user.phone_number is None
    assert user.created_at is None
    assert user.updated_at is None

def test_age_calculation():
    dob = date.today() - timedelta(days=366*25)  # 25 años
    user = UserEntity(
        cod="U125",
        first_name="Test",
        last_name="User",
        email="testuser@test.com",
        username="testuser",
        password_hash="hash",
        date_of_birth=dob
    )
    assert user.age == 25

def test_age_none_if_no_dob():
    user = UserEntity(
        cod="U126",
        first_name="NoDOB",
        last_name="User",
        email="nodob@test.com",
        username="nodobuser",
        password_hash="hash"
    )
    assert user.age is None

def test_serialize_user_all_fields():
    dob = date(2000, 1, 1)
    now = datetime(2025, 12, 2, 20, 0, 0)
    user = UserEntity(
        cod="U127",
        first_name="Serialize",
        last_name="Test",
        email="serialize@test.com",
        username="serializeuser",
        password_hash="hash",
        date_of_birth=dob,
        created_at=now,
        updated_at=now
    )

    serialized = user.serialize()
    assert serialized["date_of_birth"] == dob.isoformat()
    assert serialized["created_at"] == now.isoformat()
    assert serialized["updated_at"] == now.isoformat()

def test_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError):
        UserEntity(
            cod="U128",
            first_name="Invalid",
            last_name="Email",
            email="not-an-email",
            username="invalidemail",
            password_hash="hash"
        )
