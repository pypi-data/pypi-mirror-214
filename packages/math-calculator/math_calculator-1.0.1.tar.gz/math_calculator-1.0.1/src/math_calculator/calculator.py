import emoji

def add(x, y):
    """Add two numbers with an emoji."""
    result = x + y
    return emoji.emojize(":plus:") + " " + str(result)

def subtract(x, y):
    """Subtract two numbers with an emoji."""
    result = x - y
    return emoji.emojize(":minus:") + " " + str(result)

def multiply(x, y):
    """Multiply two numbers with an emoji."""
    result = x * y
    return emoji.emojize(":multiply:") + " " + str(result)

def divide(x, y):
    """Divide two numbers with an emoji."""
    if y != 0:
        result = x / y
        return emoji.emojize(":divide:") + " " + str(result)
    else:
        raise ZeroDivisionError("Cannot divide by zero.")
