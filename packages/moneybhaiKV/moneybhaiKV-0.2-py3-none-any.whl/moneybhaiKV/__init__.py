import math

def calculate(expression):
    """
    Evaluate and return the result of a mathematical expression.

    Args:
        expression (str): The mathematical expression to be evaluated.

    Returns:
        float: The result of the evaluated expression.

    Raises:
        ValueError: If the expression is invalid or if the evaluation fails.
    """

    try:
        result = eval(expression)
        return result
    except Exception as e:
        raise ValueError("Invalid expression or evaluation failed.") from e


#################################################################################################
def add(*args):
    """
    Add the given numbers

    Args:
        *args (list): List of the number as a input to be added

    Returns:
        int: the sum of all numbers given as input      
    """
    result = 0
    for n in args:
        try:
            result = result + n
        except Exception as e:
            print(e)
            return (False, e)
    return result
####################################################################################################
def substract(a, b):
    """
    Substract two numbers i.e. first number - second number

    Args:
        a (int): first number.
        b (int): second number
    Returns:
        int: a-b
    """
    try:
        result = a-b
    except Exception as e:
        print(e)
        return (False, e)
####################################################################################################
def multiply(*args): 
    """
    Multiply the given numbers

    Args:
        *args (list): List of the number as a input to be multiply

    Returns:
        int: the product of all numbers given as input      
    """
    result = 1
    for n in args:
        try:
            result= n * args
        except Exception as e:
            print(e)
            return (False, e)
    return result
###########################################################################
def divide(a,b):
    try:
        result = a/b
    except Exception as e:
        print(e)
        return (False, e)
    return result
###########################################################################
def isPrimeNumber(number):
    """
    Check if a number is prime or not.

    Args:
        number (int): The number to be checked.

    Returns:
        bool: True if the number is prime, False otherwise.
    """

    if not isinstance(number, int) or number < 2:
        raise ValueError("Please provide a positive integer greater than or equal to 2.")

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True
###########################################################################
def fibonacciSeries(n, toPrint):
    """
    Generate the Fibonacci series up to the given number and print it.

    Args:
        n (int): The number up to which the Fibonacci series should be generated.
        toPrint (bool): To check whether the user wants to print it or not

    Returns:
        list: The Fibonacci series as a list.
    """

    if not isinstance(n, int) or n < 1:
        raise ValueError("Please provide a positive integer.")

    fib_series = [0, 1]

    while fib_series[-1] < n:
        fib_series.append(fib_series[-1] + fib_series[-2])

    fib_series = fib_series[:-1]

    if (type(toPrint) == type(True)):
        if toPrint:
            for i in range(len(fib_series)):
                print(f"Fibonacci #{i + 1}: {fib_series[i]}")
    else:
        raise ValueError("Kindly give boolean value True or False to clarify whether you want to print the Fibonacci series or not.")
    
    return fib_series
###########################################################################
def factorial(n):
    """
    Calculate the factorial of a number.

    Args:
        n (int): The number for which the factorial should be calculated.

    Returns:
        int: The factorial of the given number.

    Raises:
        ValueError: If the input is not a positive integer.
    """

    if not isinstance(n, int) or n < 0:
        raise ValueError("Please provide a positive integer.")

    result = 1

    for i in range(1, n + 1):
        result *= i

    return result

###########################################################################
def digitSum(number):
    """
    Calculate the sum of digits in a number.

    Args:
        number (int): The number for which the sum of digits should be calculated.

    Returns:
        int: The sum of digits in the given number.

    Raises:
        ValueError: If the input is not a positive integer.
    """

    if not isinstance(number, int) or number < 0:
        raise ValueError("Please provide a positive integer.")

    result = 0

    while number > 0:
        result += number % 10
        number //= 10

    return result

###########################################################################
def area(shape, *dimensions):
    """
    Calculate the area of various geometric shapes.

    Args:
        shape (str): The shape for which the area should be calculated. Supported shapes: 'circle', 'rectangle', 'triangle'.
        dimensions (float): The dimensions required for the corresponding shape:
            - For 'circle': Pass a single value for the radius.
            - For 'rectangle': Pass two values for the length and width.
            - For 'triangle': Pass two values for the base and height.

    Returns:
        float: The calculated area of the specified shape.

    Raises:
        ValueError: If the shape is not supported or if the dimensions are invalid.
    """

    if shape not in ['circle', 'rectangle', 'triangle']:
        raise ValueError("Invalid shape. Supported shapes are 'circle', 'rectangle', and 'triangle'.")

    if shape == 'circle':
        if len(dimensions) != 1 or dimensions[0] <= 0:
            raise ValueError("For a circle, please provide a single positive value for the radius.")
        radius = dimensions[0]
        result = math.pi * radius ** 2

    elif shape == 'rectangle':
        if len(dimensions) != 2 or dimensions[0] <= 0 or dimensions[1] <= 0:
            raise ValueError("For a rectangle, please provide two positive values for the length and width.")
        length, width = dimensions
        result = length * width

    elif shape == 'triangle':
        if len(dimensions) != 2 or dimensions[0] <= 0 or dimensions[1] <= 0:
            raise ValueError("For a triangle, please provide two positive values for the base and height.")
        base, height = dimensions
        result = 0.5 * base * height

    return f"The area of the {shape} with its dimension = {result}"

###########################################################################


def isArmstrong(number):
    """
    Check if a given number is an Armstrong number.

    Args:
        number (int): The number to be checked.

    Returns:
        bool: True if the number is an Armstrong number, False otherwise.

    Raises:
        ValueError: If the input is not a positive integer.
    """

    if not isinstance(number, int) or number < 0:
        raise ValueError("Please provide a positive integer.")

    # Calculate the number of digits in the given number
    num_digits = len(str(number))

    # Initialize the sum variable
    armstrong_sum = 0

    # Temporarily store the original number
    temp = number

    # Calculate the sum of the digits raised to the power of the number of digits
    while temp > 0:
        digit = temp % 10
        armstrong_sum += digit ** num_digits
        temp //= 10

    # Check if the calculated sum is equal to the original number
    if number == armstrong_sum:
        return True
    else:
        return False


###########################################################################
def decimalAndBinary(number, mode):
    """
    Convert a decimal number to binary or vice versa.

    Args:
        number (int): The number to be converted.
        mode (str): The conversion mode. 'decimal_to_binary' to convert decimal to binary, 'binary_to_decimal' to convert binary to decimal.

    Returns:
        int: The converted value.

    Raises:
        ValueError: If the input is not a positive integer or if the conversion mode is invalid.
    """

    if not isinstance(number, int) or number < 0:
        raise ValueError("Please provide a positive integer.")

    if mode not in ['decimal_to_binary', 'binary_to_decimal']:
        raise ValueError("Invalid conversion mode. Please choose 'decimal_to_binary' or 'binary_to_decimal'.")

    result = 0

    if mode == 'decimal_to_binary':
        result = bin(number)[2:]  # Remove the '0b' prefix from the binary representation
    elif mode == 'binary_to_decimal':
        result = int(str(number), 2)

    return result


###########################################################################
def gcd(a, b):
    """
    Calculate and return the Greatest Common Divisor (GCD) of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The calculated GCD.

    Raises:
        ValueError: If the inputs are not positive integers.
    """

    if not isinstance(a, int) or not isinstance(b, int) or a <= 0 or b <= 0:
        raise ValueError("Please provide positive integers for both numbers.")

    while b != 0:
        a, b = b, a % b

    result = a
    return result

###########################################################################
def matrix(matrix1, matrix2, operation):
    """
    Perform a matrix operation and return the resulting matrix.

    Args:
        matrix1 (list): The first matrix represented as a 2D list.
        matrix2 (list): The second matrix represented as a 2D list.
        operation (str): The matrix operation to perform. 'add' for matrix addition, 'subtract' for matrix subtraction, 'multiply' for matrix multiplication.

    Returns:
        list: The resulting matrix after the operation.

    Raises:
        ValueError: If the input matrices are not valid or if the operation is invalid.
    """

    # Validate input matrices
    if not all(isinstance(row, list) and len(row) == len(matrix1[0]) for row in matrix1):
        raise ValueError("Invalid first matrix.")
    if not all(isinstance(row, list) and len(row) == len(matrix2[0]) for row in matrix2):
        raise ValueError("Invalid second matrix.")
    if len(matrix1) != len(matrix2):
        raise ValueError("Matrix dimensions do not match.")

    # Validate operation
    if operation not in ['add', 'subtract', 'multiply']:
        raise ValueError("Invalid operation. Choose 'add', 'subtract', or 'multiply'.")

    # Perform matrix operation
    if operation == 'add':
        result = [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
    elif operation == 'subtract':
        result = [[matrix1[i][j] - matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
    elif operation == 'multiply':
        result = [[sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix2))) for j in range(len(matrix2[0]))] for i in range(len(matrix1))]

    return result

############################################################################
def simpleInterest(principal, rate, time):
    """
    Calculate and return the Simple Interest.

    Args:
        principal (float): The principal amount.
        rate (float): The interest rate per period.
        time (float): The time period in years.

    Returns:
        float: The calculated Simple Interest.

    Raises:
        ValueError: If any of the inputs are not valid or if the interest rate or time is negative.
    """

    if not isinstance(principal, (int, float)) or principal < 0:
        raise ValueError("Invalid principal amount. Please provide a non-negative number.")
    if not isinstance(rate, (int, float)) or rate < 0:
        raise ValueError("Invalid interest rate. Please provide a non-negative number.")
    if not isinstance(time, (int, float)) or time < 0:
        raise ValueError("Invalid time period. Please provide a non-negative number.")

    result = (principal * rate * time) / 100
    return result

##########################################################################
def fileIOmenu():
    """
    Perform file I/O operations based on user input.

    Returns:
        str: The message indicating the completion of the file operation.

    Raises:
        ValueError: If the user input is not a valid option.
    """

    while True:
        print("\nFile Operations Menu:")
        print("1. Create a new file")
        print("2. Read an existing file")
        print("3. Write to an existing file")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice (1-4): "))
        except ValueError:
            print("Invalid input. Please enter a valid option.")
            continue

        if choice == 1:
            file_path = input("Enter the path of the new file: ")
            try:
                with open(file_path, 'w'):
                    pass
                print("File created successfully.")
            except FileNotFoundError:
                print("Invalid file path. Please provide a valid path.")
            except PermissionError:
                print("Permission denied. Unable to create file.")

        elif choice == 2:
            file_path = input("Enter the path of the file to read: ")
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                print("\nFile Contents:")
                print(content)
            except FileNotFoundError:
                print("File not found. Please provide a valid file path.")
            except PermissionError:
                print("Permission denied. Unable to read file.")

        elif choice == 3:
            file_path = input("Enter the path of the file to write: ")
            content = input("Enter the content to write: ")
            try:
                with open(file_path, 'w') as file:
                    file.write(content)
                print("File written successfully.")
            except FileNotFoundError:
                print("File not found. Please provide a valid file path.")
            except PermissionError:
                print("Permission denied. Unable to write to file.")

        elif choice == 4:
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please enter a valid option (1-4).")

    return "File operation completed."

###############################################################################
def quadratic(a, b, c):
    """
    Find the roots of a quadratic equation of the form ax^2 + bx + c = 0.

    Args:
        a (float): Coefficient of x^2.
        b (float): Coefficient of x.
        c (float): Constant term.

    Returns:
        tuple: A tuple containing the roots of the quadratic equation.
               If the equation has real roots, it returns a tuple of two values (root1, root2).
               If the equation has complex roots, it returns a tuple of two complex values (root1, root2).

    Raises:
        ValueError: If the equation does not have real or complex roots.
    """

    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        root1 = (-b + (discriminant)**0.5) / (2*a)
        root2 = (-b - (discriminant)**0.5) / (2*a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2*a)
        return root, root
    else:
        real_part = -b / (2*a)
        complex_part = ((-discriminant)**0.5) / (2*a)
        root1 = complex(real_part, complex_part)
        root2 = complex(real_part, -complex_part)
        return root1, root2

###############################################################################
def palindrome(number):
    """
    Check whether a number is a palindrome or not.

    Args:
        number (int): The number to be checked.

    Returns:
        bool: True if the number is a palindrome, False otherwise.

    Raises:
        ValueError: If the input is not a positive integer.
    """

    if not isinstance(number, int) or number <= 0:
        raise ValueError("Input must be a positive integer.")

    # Convert the number to a string for easy comparison
    number_str = str(number)

    # Check if the number is equal to its reverse
    return number_str == number_str[::-1]
################################################################################
def multiplicationTable(number):
    """
    Print the multiplication table for a given number from 1 to 10.

    Args:
        number (int): The number for which the multiplication table is generated.

    Returns:
        str: The formatted multiplication table.

    Raises:
        ValueError: If the input is not a positive integer.
    """

    if not isinstance(number, int) or number <= 0:
        raise ValueError("Input must be a positive integer.")

    table = ""

    for i in range(1, 11):
        row = f"{number} x {i} = {number * i}"
        table += row + "\n"

    return table

###############################################################################
def inf0():
    return ("calculate", "add", "substract", "multiply", "divide", "isPrimeNumber", "fibonacciSeries", "factorial", "digitSum", "area", "isArmstrong", "decimalAndBinary", "gcd", "matrix", "simpleIntrest", "fileIOmenu", "quadratic", "palindrome", "multiplicationTable", "inf0")



