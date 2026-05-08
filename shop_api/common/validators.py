from datetime import date
from rest_framework.exceptions import ValidationError


def validate_user_age(user):
    birthdate = user.birthdate

    if not birthdate:
        raise ValidationError("Дата рождения не указана.")

    today = date.today()

    age = (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )

    if age < 18:
        raise ValidationError(
            "Вам должно быть 18 лет, чтобы создать продукт."
        )