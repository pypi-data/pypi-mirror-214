import emoji

def add(x, y):
    """Add two numbers with an emoji."""
    result = x + y
    return emoji.emojize(":heavy_plus_sign:") + " " + str(result)

def subtract(x, y):
    """Subtract two numbers with an emoji."""
    result = x - y
    return emoji.emojize(":heavy_minus_sign:") + " " + str(result)

def multiply(x, y):
    """Multiply two numbers with an emoji."""
    result = x * y
    return emoji.emojize(":heavy_multiplication_x:") + " " + str(result)

def divide(x, y):
    """Divide two numbers with an emoji."""
    if y != 0:
        result = x / y
        return emoji.emojize(":heavy_division_sign:") + " " + str(result)
    else:
        raise ZeroDivisionError("Cannot divide by zero.")
