from decimal import Decimal, InvalidOperation


# Check if the username follows some basic rules
def validate_username(name):
    if len(name) < 3 or len(name) > 20:
        return "Username must have between 3 and 20 characters"

    for character in name:
        if not (character.isalnum() or character == "_"):
            return "Username can only use letters, numbers and underscores"

    return None


# Check if the password follows some basic rules
def validate_password(password):
    if len(password) < 8:
        return "Password must have at least 8 characters"

    has_letter = False
    has_number = False

    for character in password:
        if character.isalpha():
            has_letter = True

        if character.isdigit():
            has_number = True

    if not has_letter or not has_number:
        return "Password must include at least one letter and one number"

    return None


# Convert a text value into a decimal number
def parse_decimal_value(value):
    try:
        return Decimal(str(value)), None
    except (InvalidOperation, TypeError):
        return None, "Value must be a valid number"


# Convert a text value into an integer number
def parse_int_value(value):
    try:
        return int(value), None
    except (ValueError, TypeError):
        return None, "Value must be a valid whole number"


# Check if the profile measurements are inside the allowed range
def validate_measurements(measurements):
    for field, value in measurements.items():
        if value == "":
            continue

        number_value, error_message = parse_decimal_value(value)

        if error_message:
            return "Measurements must be valid numbers"

        if field == "weight":
            if number_value < Decimal("30") or number_value > Decimal("600"):
                return "Weight must be between 30 and 600 kilograms"

        elif field == "height":
            if number_value < Decimal("1") or number_value > Decimal("3"):
                return "Height must be between 1 and 3 metres"

        elif number_value < Decimal("10") or number_value > Decimal("200"):
            return f"{field.capitalize()} must be between 10 and 200 centimetres"

    return None


# Check if the cardio exercise values are valid
def validate_cardio_exercise(exercise):
    time_value, time_error = parse_decimal_value(exercise.get("time"))

    if time_error:
        return "Time must be a valid number"

    if time_value <= 0 or time_value > Decimal("500"):
        return "Time must be between 1 and 500 minutes"

    if exercise.get("name") != "Swimming":
        level_value, level_error = parse_int_value(exercise.get("level"))

        if level_error:
            return "Level must be a valid whole number"

        if level_value < 0 or level_value > 20:
            return "Level must be between 0 and 20"

    if exercise.get("name") == "Treadmill":
        incline_value, incline_error = parse_int_value(exercise.get("incline"))

        if incline_error:
            return "Incline must be a valid whole number"

        if incline_value < 0 or incline_value > 20:
            return "Incline must be between 0 and 20"

    return None


# Check if the weight training exercise values are valid
def validate_weight_exercise(exercise):
    if not exercise.get("name"):
        return "Exercise name is required"

    weight_value, weight_error = parse_decimal_value(exercise.get("weight"))

    if weight_error:
        return "Weight must be a valid number"

    if weight_value <= 0 or weight_value > Decimal("200"):
        return "Weight must be between 1 and 200 kilograms"

    reps_value, reps_error = parse_int_value(exercise.get("reps"))

    if reps_error:
        return "Reps must be a valid whole number"

    if reps_value <= 0 or reps_value > 100:
        return "Reps must be between 1 and 100"

    return None
