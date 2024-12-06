# module.py

def greet(name):
    """
    Returns a greeting message for the given name.
    
    Args:
        name (str): The name of the person to greet.
    
    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}! Welcome to my_package."

def add_numbers(a, b):
    """
    Adds two numbers together.
    
    Args:
        a (int or float): The first number.
        b (int or float): The second number.
    
    Returns:
        int or float: The sum of the numbers.
    """
    return a + b

def factorial(n):
    """
    Computes the factorial of a non-negative integer.
    
    Args:
        n (int): The number to compute the factorial for.
    
    Returns:
        int: The factorial of n.
    """
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Example usage:
if __name__ == "__main__":
    print(greet("Alice"))
    print(f"The sum of 5 and 3 is {add_numbers(5, 3)}")
    print(f"The factorial of 5 is {factorial(5)}")
