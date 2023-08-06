from PIL import Image, ImageTk
import tkinter as tk
from tkinter import font
import sys

import webbrowser

class Nova:

    def __init__(self):
        pass

    def screen2():
        # Create a Tkinter window
        window = tk.Tk()
        # Remove the title bar from the window
        window.overrideredirect(True)

        # Set the window size and position
        window_width, window_height = 500, 500
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Define a beautiful background color for the window
        background_color = "#FFC3A0"  # Attractive color

        # Set the window background color
        window.configure(bg=background_color)

        # Define button colors
        button_colors = ["#ff9f43", "#ee5253", "#54a0ff"]  # Attractive colors

        # Define window colors
        window_colors = ["#feca57", "#ff6b6b", "#5f27cd"]  # Attractive colors

        # Define button click functions
        def open_window1():
            window.destroy()
            def on_select(event):
                def open_youtube():
                    webbrowser.open(url1)
                selected_text = listbox.get(listbox.curselection())
                back_button_frame1 = tk.Frame(new_window)
                back_button_frame1.grid(row=2, column=0, padx=10, pady=10, sticky=tk.SE)

        # Create the back button
                back_button1 = tk.Button(back_button_frame1, text="Video", font=("Arial", 12), command=open_youtube,bg="Red",fg="white")
                back_button1.pack()

            

                if selected_text == "Introduction to Python":
                    def_label.config(text="Python is a high-level programming language\nknown for its simplicity and readability. It was created by Guido van Rossum\n and first released in 1991. Python emphasizes code readability with \nits clear and expressive syntax, making it easier to write and understand compared to \nother programming languages. It supports multiple programming paradigms,\n including procedural, object-oriented, and functional programming.\nPython is widely used in various domains such as web development,\n scientific computing,data analysis, artificial intelligence, and automation. It has a \nvast ecosystem of libraries and frameworks that\n enhance its capabilities and enable developers to accomplish complex tasks\n with ease.\n")
                    code1_label.config(text="Python Syntex will be:\n\n print(Hello, World!)\n\nmessage = Welcome to Python!\nnumber = 42")
                    code2_label.config(text="Applications:\n\n1.Web Development\n2.Machine Learning and AI\n3.Automation and Scripting\n4.Game Development\n5.Desktop GUI Applications")
                    url1 = "https://youtu.be/BP9FTCl4sGM?list=PL1VbPa6UXxUMgMFZOTtIi4kpXScKspZ8x"
              
                
                
                elif selected_text == "Data Types":
                    def_label.config(text="In programming, a data type is an attribute or classification given to\n a variable or value, determining the type of data it can hold and the operations \nthat can be performed on it. Data types define the representation \nof data in memory, the range of values it can store, and the operations\n that can be performed on that data")
                    code1_label.config(text="Numeric Type:\n\n1. Integer(x = 42,y = -10)\n\n2. Floating(pi = 3.14159,temperature = -2.5)\n\n3. Complex Type(z = 2 + 3j,w = -1.5 + 2j)\n\nOther Types:\n\nNone:presents the absence of a value or a null value.\n\nbytes: Represents a sequence of bytes.\n\nbytearray: Represents a mutable sequence of bytes")
                    code2_label.config(text=" Boolean Types\n\n is_raining = True\n\nis_sunny = False\n\nprint(is_raining) # Output: True\n\nprint(is_sunny)  # Output: False")
                    url1 = "https://youtu.be/vmCfc8n5XVA?list=PL1VbPa6UXxUMgMFZOTtIi4kpXScKspZ8x"
                elif selected_text == "Operations":
                    def_label.config(text="In Python, an operation refers to an action or manipulation performed on data\n or variables \nPython supports a wide range of operations, including arithmetic, assignment,\n comparison, logical, bitwise, and more. These operations allow you to perform \ncalculations, manipulate data, and control the flow of your program.")
                    code1_label.config(text="Arithmetic Operations:\n\n a = 5, b = 3\naddition = a + b\nsubtraction = a - b\nmultiplication = a * b\ndivision = a / b\nmodulus = a % b\nexponentiation = a ** b\n\nAssignment Operators:\n\nx=10 ,x+=5(: x=x+5)\nx-=3(: x=x-3) ,x*=2(: x=x*2) ,x/=4(: x=x/4)")
                    code2_label.config(text="Comparision Operations\n\na = 5\nb = 3\nprint(a == b)   # Output: False\nprint(a != b)   # Output: True\nprint(a > b)    # Output: True\nprint(a < b)    # Output: False\nprint(a >= b)   # Output: True\nprint(a <= b)   # Output: False ")
                    url1 = "https://youtu.be/vmCfc8n5XVA?list=PL1VbPa6UXxUMgMFZOTtIi4kpXScKspZ8x"
                elif selected_text == "If-Else Statements":
                    def_label.config(text="If-else statements allow your program to make decisions based on certain conditions.\nYou can specify different code blocks to be executed based on whether the condition \nis True or False.")
                    code1_label.config(text="Example:\n\nx = 10\n\nif x > 5:\n    print('x is greater than 5')\nelse:\n    print('x is not greater than 5')")
                    code2_label.config(text="Output:\n\nx is greater than 5")
                    url1="https://youtu.be/WtwsekLNXME?list=PL1VbPa6UXxUMgMFZOTtIi4kpXScKspZ8x"
                elif selected_text == "For Loop": 
                    def_label.config(text="A for loop is used to iterate over a sequence (such as a list, tuple, string, or range)\n or other iterable objects.\nIt allows you to execute a set of statements repeatedly for each item in the sequence.")
                    code1_label.config(text="Example 1:\n\nfruits = ['apple', 'banana', 'cherry']\nfor fruit in fruits:\n    print(fruit)\n\nOutput:\napple\nbanana\ncherry")
                    code2_label.config(text="Example 2:\n\nfor i in range(5):\n    print(i)\n\nOutput:\n0\n1\n2\n3\n4")
                    url1="https://youtu.be/WtwsekLNXME?list=PL1VbPa6UXxUMgMFZOTtIi4kpXScKspZ8x"
                elif selected_text == "While Loop":
                    def_label.config(text="A while loop is used to repeatedly execute a set of statements as long as \na certain condition is True.It is useful when you don't know beforehand how many\n times the loop will be executed.")
                    code1_label.config(text="Example:\n\ncount = 0\nwhile count < 5:\n    print('Count:', count)\n    count += 1")
                    code2_label.config(text="Output:\n\nCount: 0\nCount: 1\nCount: 2\nCount: 3\nCount: 4")
                    url1="https://youtu.be/WtwsekLNXME?list=PL1VbPa6UXxUMgMFZOTtIi4kpXScKspZ8x"
                elif selected_text == "Logical Operators":
                    def_label.config(text="Logical operators in Python are used to combine multiple conditions and perform \nlogical operations on them.\nThere are three logical operators: 'and', 'or', and 'not'.")
                    code1_label.config(text="Example:\n\nx = 5\ny = 10\n\nif x > 0 and y < 20:\n    print('Both conditions are True')\n\nif x > 0 or y > 20:\n    print('At least one condition is True')\n\nif not(x < 0):\n    print('Negation of a condition')")
                    code2_label.config(text="Output:\n\nBoth conditions are True\nAt least one condition is True\nNegation of a condition")
                    url1="https://youtu.be/cmeJZVv_1_E?list=PL1VbPa6UXxUN1p2J1Q22js5IAEpOx1jac"
                elif selected_text == "Simple Calculator":
                    def_label.config(text="A simple calculator performs basic arithmetic operations such\n as addition, subtraction, multiplication, and division.")
                    code1_label.config(text="Example:\n\nnum1 = 5\nnum2 = 3\n\n# Addition\nresult = num1 + num2\nprint('Addition:', result)\n\n# Subtraction\nresult = num1 - num2\nprint('Subtraction:', result)\n\n# Multiplication\nresult = num1 * num2\nprint('Multiplication:', result)\n\n")
                    code2_label.config(text="Division\nresult = num1 / num2\nprint('Division:', result)\n=====================\nOutput:\n\nAddition: 8\nSubtraction: 2\nMultiplication: 15\nDivision: 1.6666666666666667")   
                    url1="https://youtu.be/9KOuBvFr-RE?list=PL1VbPa6UXxUMgMFZOTtIi4kpXScKspZ8x"
                elif selected_text == "User-defined Functions":
                    def_label.config(text="A user-defined function is a block of reusable code that performs a specific task.\nIt allows you to encapsulate a sequence of statements into a single entity, which \ncan be called multiple times throughout your program.")
                    code1_label.config(text="Example:\n\ndef greet(name):\n    print('Hello, ' + name + '!')\n\n\ndef add_numbers(a, b):\n    return a + b\n\n\ndef multiply_numbers(a, b):\n    return a * b\n\n\n# Calling the greet() function\nname ='Alice'\ngreet(name)")
                    code2_label.config(text="num1 = 5\nnum2 = 3\nresult = add_numbers(num1, num2)\nprint('Addition:', result)\n\n\n# Calling the multiply_numbers() function\n\nnum3 = 4\nnum4 = 2\nresult = multiply_numbers(num3, num4)\nprint('Multiplication:', result)\n=====================\nOutput:\n\nHello, Alice!\nAddition: 8\nMultiplication: 8") 
                    url1="https://youtu.be/JnxmJimNEzs?list=PL1VbPa6UXxUMgMFZOTtIi4kpXScKspZ8x"
                elif selected_text == "Factorization Example":
                    def_label.config(text="Factorization is the process of finding the prime factors of a given number.\nPrime factors are the prime numbers that divide the given number\n without leaving any remainder.")
                    code1_label.config(text="Example:\n\ndef factorize(number):\n    factors = []\n    divisor = 2\n\n    while divisor <= number:\n        if number % divisor == 0:\n            factors.append(divisor)\n            number = number // divisor\n        else:\n            divisor += 1\n\n    return factors\n\ndef num_factorization(number):\n    factors = factorize(number)\n    result = str(number) + ' = '")
                    code2_label.config(text="for i, factor in enumerate(factors):\n        result += str(factor)\n\n        if i != len(factors) - 1:\n            result += ' * '\n\n    return result\n=====================\nUsage:\n\nnum = 24\nfactorization = num_factorization(num)\nprint(factorization)\n\nOutput:\n\n24 = 2 * 2 * 2 * 3")
                    url1=""
                elif selected_text == "Lists":
                    def_label.config(text="In Python, a list is a mutable ordered collection of elements.\n Lists are versatile and can store elements of different data types,\n including numbers, strings, or even other lists. You can add, remove, \nor modify elements in a list, making it a powerful data structure for storing\n and manipulating data.")
                    code1_label.config(text="Creating a List:\n\n# Empty list\nmy_list = []\n\n# List with elements\nmy_list = [1, 2, 'Hello', 3.14]\n\nAccessing Elements:\n\n# Accessing single element\nprint(my_list[0])  # Output: 1\n\n# Accessing a range of elements\nprint(my_list[1:3])  # Output: [2, 'Hello']\n\nModifying Elements:\n===============\n# Modifying an element\nmy_list[2] = 'Hi'\n\n# Modifying a range of elements\nmy_list[1:3] = [5, 6]\n\n")
                    code2_label.config(text="Common List Operations:\n\n# Length of a list\nlength = len(my_list)\n\n# Checking if an element exists in a list\nprint('Hello' in my_list)  # Output: True\n\n# Concatenating two lists\nnew_list = my_list + [4, 5]\n\n# Repeating a list\nrepeated_list = my_list * 3\n\n# Sorting a list\nmy_list.sort()\n\n")
                    url1=""
                elif selected_text == "Tuples":
                    def_label.config(text="In Python, a tuple is an immutable ordered collection of elements.Tuples are similar\n to lists, but they cannot be modified once created. Tuples are commonly \nused to group related data together and provide data integrity. Unlike lists,\n tuples are enclosed in parentheses instead of square brackets.")
                    code1_label.config(text="Creating a Tuple:\n================\n# Empty tuple\nmy_tuple = ()\n\n# Tuple with elements\nmy_tuple = (1, 2, 'Hello', 3.14)\n=====================\nAccessing Elements:\n\n# Accessing single element\nprint(my_tuple[0])  # Output: 1\n\n# Accessing a range of elements\nprint(my_tuple[1:3])  # Output: (2, 'Hello')")
                    code2_label.config(text="Common Tuple Operations:\n==============\n# Length of a tuple\nlength = len(my_tuple)\n\n# Checking if an element exists in a tuple\nprint('Hello' in my_tuple)  # Output: True\n\n# Concatenating two tuples\nnew_tuple = my_tuple + (4, 5)\n\n# Repeating a tuple\nrepeated_tuple = my_tuple * 3")
                    url1=""
                elif selected_text == "Dictionaries":
                    def_label.config(text="In Python, a dictionary is an unordered collection of key-value pairs. It is also\n known as an associative array or hash table. Dictionaries are mutable\n, meaning their elements can be modified after creation. Each element\n in a dictionary consists of a key and its corresponding value.\n")
                    code1_label.config(text="Creating a Dictionary:\n===========\n# Empty dictionary\nmy_dict = {}\n\n# Dictionary with elements\nmy_dict = {'name': 'John', 'age': 25'}\n\nAccessing Elements:\n===============\n# Accessing value using key\nprint(my_dict['name'])  # Output: 'John'")
                    code2_label.config(text="Common Dictionary Operations:\n================\n# Adding or updating an element\nmy_dict['gender'] = 'Male'\n\n# Removing an element\ndel my_dict['age']\n\n# Checking if a key exists\nprint('name' in my_dict)  # Output: True\n\n# Getting all keys\nkeys = my_dict.keys()\n\n# Getting all values\nvalues = my_dict.values()")
                    url1=""
                elif selected_text == "Sets":
                    def_label.config(text="In Python, a set is an unordered collection of unique elements. Sets are used \nto store multiple items in a single variable, without any particular order.\n Sets are mutable, meaning you can add or remove elements from them. Sets \ncommonly used to perform mathematical set operations such as union, intersection,\n and difference.")
                    code1_label.config(text="Creating a Set:\n===============\n# Empty set\nmy_set = set()\n\n# Set with elements\nmy_set = {1, 2, 3}\n\nAdding and Removing Elements:\n================\n# Adding an element\nmy_set.add(4)\n\n# Removing an element\nmy_set.remove(2)")
                    code2_label.config(text="Common Set Operations:\n===============\n# Union of two sets\nset1 = {1, 2, 3}\nset2 = {3, 4, 5}\nunion_set = set1 | set2\n\n# Intersection of two sets\nintersection_set = set1 & set2\n\n# Difference of two sets\ndifference_set = set1 - set2\n\n# Checking if a value exists in a set\nprint(3 in set1)  # Output: True")
                    url1=""
                elif selected_text == "Example1":
                    def_label.config(text="This is an example that demonstrates the usage of lists,\n tuples, dictionaries, and sets together.")
                    code1_label.config(text="Create a list\nmy_list = [1, 2, 3, 4, 5]\nprint(my_list[0])  # Output: 1\n\n# Update an element\nmy_list[0] = 10\n# Create a tuple\nmy_tuple = (1, 2, 3, 4, 5)\n\n# Access an element\nprint(my_tuple[0])  # Output: 1\n# Create a dictionary\nmy_dict = {'name': 'John', 'age': 25}\n\n# Access a value\nprint(my_dict['name'])  # Output: John\n# Create a set\nmy_set = {1, 2, 3, 4, 5}")
                    code2_label.config(text="#Usage of lists, tuples, dictionaries,and sets\n\n# List\nmy_list = [1, 2, 3, 4, 5]\n\n# Tuple\nmy_tuple = (6, 7, 8, 9, 10)\n\n# Dictionary\nmy_dict = {'name': 'Alice', 'age': 30}\n\n# Set\nmy_set = {11, 12, 13, 14, 15}\n\n# Print the elements\nprint('List:', my_list)\nprint('Tuple:', my_tuple)\nprint('Dictionary:', my_dict)\nprint('Set:', my_set)")
                    url1=""
                elif selected_text == "Reading Files":
                    def_label.config(text="This section demonstrates how to read data from a file in Python.")
                    code1_label.config(text="# Open the file in read mode\nfile = open('data.txt', 'r')\n\n# Read the entire file\ncontent = file.read()\n\n# Print the content\nprint(content)\n\n# Close the file\nfile.close()")
                    code2_label.config(text="# Open the file in read mode\nwith open('data.txt', 'r') as file:\n    # Read the entire file\n    content = file.read()\n\n# Print the content\nprint(content)")
                    url1=""
                elif selected_text == "Writing Files":
                    def_label.config(text="This section demonstrates how to write data to a file in Python.")
                    code1_label.config(text="# Open the file in write mode\nfile = open('data.txt', 'w')\n\n# Write content to the file\nfile.write('Hello, World!')\n\n# Close the file\nfile.close()")
                    code2_label.config(text="# Open the file in write mode\nwith open('data.txt', 'w') as file:\n    # Write content to the file\n    file.write('Hello, World!')")
                    url1=""
                elif selected_text == "Error Handling":
                    def_label.config(text="Error handling in Python allows you to catch and handle\n exceptions that occur during the execution of your program.")
                    code1_label.config(text="try:\n    # Code that may raise an exception\n    x = 10 / 0\nexcept ZeroDivisionError:\n    # Code to handle the specific exception\n    print('Error: Division by zero')")
                    code2_label.config(text="try:\n    # Code that may raise an exception\n    x = int('abc')\nexcept ValueError:\n    # Code to handle the specific exception\n    print('Error: Invalid conversion')")
                    url1=""
                elif selected_text == "Continue Statement":
                    def_label.config(text="The continue statement is used in Python to skip the rest \nof the current iteration in a loop and move to the next iteration.")
                    code1_label.config(text="for num in range(1, 6):\n    if num == 3:\n        continue\n    print(num)")
                    code2_label.config(text="Output:\n1\n2\n4\n5")
                    url1=""
                elif selected_text == "Break Statement":
                    def_label.config(text="The break statement is used in Python to terminate the\n execution of a loop prematurely.")
                    code1_label.config(text="for num in range(1, 6):\n    if num == 4:\n        break\n    print(num)")
                    code2_label.config(text="Output:\n1\n2\n3")
                    url1=""
                elif selected_text == "Errors Types":
                    def_label.config(text="In Python, errors are classified into different types based \non their nature and cause.")
                    code1_label.config(text="1. SyntaxError:\n\nprint('Hello')\n    print('World')\n\n2. NameError:\n\nx = 5\nprint(y)\n\n3. RuntimeError:\n\n# Example of a runtime error\nx = 10\ny = 0\nresult = x / y")
                    code2_label.config(text="4. ValueError:\n\n# Example of a logical error\nx = 5\ny = 2\nif x < y:\n    print('x is smaller than y')\nelse:\n    print('x is greater than y')\n\n5. IndexError:\n\n# Example of an index error\nnumbers = [1, 2, 3]\nprint(numbers[3])\n")
                    url1=""
                elif selected_text == "Modules":
                    def_label.config(text="In Python, a module is a file containing Python definitions and statements.\nModules are used to organize code into reusable components.")
                    code1_label.config(text="To use a module in your Python program,\n you first need to \nimport it using the import statement.\n\nExample:\n\nimport math\n\ndef main():\n    radius = 5\n    area = math.pi * math.pow(radius, 2)\n    print('The area of the circle is:', area)\n\nmain()")
                    code2_label.config(text="In this example, the 'math' module\n is imported to perform mathematical\n calculations.\nThe 'pi' constant and the 'pow'\n function from the 'math' module are used \nto calculate the area of a circle.")
                    url1=""
                elif selected_text == "Third-Party Modules":
                    def_label.config(text="Third-party modules are external libraries or packages that are not\nbuilt-in to Python but are created and maintained by the Python community.")
                    code1_label.config(text="To use a third-party module,\n you need to install it first using a\n package managersuch as pip. \nOnce installed, you can import and \nuse the module in your Python code.")
                    code2_label.config(text="Example:\n\n# Installation\n\n$ pip install requests\n\n# Usage\n\nimport requests\n\nresponse = requests.get('https://www.\nexample.com')\nprint(response.status_code)")
                    url1=""
                elif selected_text == "Practice_Questions":
                    def_label.config(text="Practice Questions")
                    code1_label.config(text="1. Write a Python program to \ncalculate the factorial of \na number.\n\n2. Create a function that takes a \nstring as input and returns the \nreverse of the string.\n\n3. Write a Python program to \nfind the largest element in a list.\n\n4. Create a dictionary that stores\n the names and ages \nof five people.\n\n5. Write a Python program \nto remove duplicates from \na list.")
                    code2_label.config(text="1. Write a Python program to\n check if a number \nis prime.\n\n2. Create a loop that \niterates through a list and \nprints each element.\n\n3. Write a Python program to \ncount the number of occurrences \nof a specific element in a list.\n\n4. Create a tuple containing\n the names of three \ncountries.\n\n5. Write a Python program to \nperform set operations \n(union, intersection, difference) \non two sets.")
                    url1=""
            
               



            def go_back():
                new_window.destroy()
                sys.exit()

        # Create the main window

            new_window = tk.Tk()
        #    Remove the title bar from the window
            new_window.overrideredirect(True)

        # Set the fixed screen size
            new_window.geometry("800x400")  # Adjust the dimensions as desired

        # Calculate the window position to center it on the screen
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            window_x = (screen_width - 800) // 2
            window_y = (screen_height - 400) // 2
            new_window.geometry(f"+{window_x}+{window_y}")

        # Create a search entry field with styling
            search_entry = tk.Entry(new_window, font=("Arial", 14), bd=2, relief=tk.SOLID)
            search_entry.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Create a listbox for the scroll-down menu
            listbox = tk.Listbox(new_window, width=20)
            listbox.grid(row=1, column=0, padx=10, pady=0, sticky=tk.NSEW)

        # Create a scrollbar and link it to the listbox
            scrollbar = tk.Scrollbar(new_window)
            scrollbar.grid(row=1, column=1, padx=0, pady=0, sticky=tk.NS)
            listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)

        # Sample texts for the listbox
            sample_texts = [
                "Introduction to Python",
                "Data Types",
                "Operations",
                "If-Else Statements",
                "For Loop",
                "While Loop",
                "Logical Operators",
                "Simple Calculator",
                "User-defined Functions",
                "Factorization Example",
                "Lists",
                "Tuples",
                "Dictionaries",
                "Sets",
                "Example1",
                "Reading Files",
                "Writing Files",
                "Error Handling",
                "Continue Statement",
                "Break Statement",
                "Errors Types",
                "Modules",
                "Third-Party Modules",
                "Practice_Questions"
            ]

        # Add sample items to the listbox
            for item in sample_texts:
                listbox.insert(tk.END, item)

        # Bind the selection event to the listbox
            listbox.bind('<<ListboxSelect>>', on_select)



        # Create a label to display the selected text
            display_label = tk.Label(new_window, text="", font=("Arial", 14))
            display_label.grid(row=1, column=2, padx=10, pady=10, sticky=tk.NSEW)

        # Create the upper frame for definitions with black background
            upper_frame = tk.Frame(new_window, bg="black")
            upper_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky=tk.NSEW)

        # Create labels for the frames
            def_label = tk.Label(upper_frame, text="", font=("Arial", 10), fg="white", bg="black")
            def_label.pack(side=tk.TOP, padx=10, pady=10)

        # Create the two vertical frames within the lower frame
            left_lower_frame = tk.Frame(upper_frame, bg="powder blue")
            left_lower_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            right_lower_frame = tk.Frame(upper_frame, bg="light yellow")
            right_lower_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create labels for the vertical frames
            code1_label = tk.Label(left_lower_frame, text="", font=("console", 10), bg="powder blue")
            code1_label.pack(side=tk.TOP, padx=10, pady=10)

            code2_label = tk.Label(right_lower_frame, text="", font=("console", 10), bg="light yellow")
            code2_label.pack(side=tk.TOP, padx=10, pady=10)

        # Function to update the listbox as the user types in the search field
            def update_listbox(event):
                search_query = search_entry.get().lower()
                listbox.delete(0, tk.END)
                for item in sample_texts:
                    if search_query in item.lower():
                        listbox.insert(tk.END, item)

        # Bind the key press event to update the listbox dynamically
            search_entry.bind('<KeyRelease>', update_listbox)

        # Create the frame for the back button
            back_button_frame = tk.Frame(new_window)
            back_button_frame.grid(row=2, column=2, padx=10, pady=10, sticky=tk.SE)

        # Create the back button
            back_button = tk.Button(back_button_frame, text="Exit", font=("Arial", 12), command=go_back)
            back_button.pack()




        # Configure grid layout weights for proper resizing
            new_window.grid_columnconfigure(2, weight=1)
            new_window.grid_rowconfigure(1, weight=1)
            upper_frame.grid_columnconfigure(0, weight=1)
            upper_frame.grid_rowconfigure(1, weight=1)

        # Start the main loop
            new_window.mainloop()

            

        def open_window2():
            new_window = tk.Toplevel(window)
            new_window.title("Intermediate Level")
            new_window.configure(bg=window_colors[1])
            new_window.geometry("300x200")
            label_font1 = font.Font(family="Algerian", size=10, weight="bold")
            label1 = tk.Label(new_window, text="Available Soon in Version 1.1", bg=background_color, fg="black", font=label_font1)

           # Position the label in the center
            label1.place(relx=0.5, rely=0.2, anchor="center")

        def open_window3():
            new_window = tk.Toplevel(window)
            new_window.title("Intermediate Level")
            new_window.configure(bg=window_colors[1])
            new_window.geometry("300x200")
            label_font1 = font.Font(family="Algerian", size=10, weight="bold")
            label1 = tk.Label(new_window, text="Available Soon in Version 1.1", bg=background_color, fg="black", font=label_font1)
            # Position the label in the center
            label1.place(relx=0.5, rely=0.2, anchor="center")

        def exit_program():
            window.destroy()
            sys.exit()

        # Create buttons with enhanced styling
        button_font = font.Font(family="Arial", size=16, weight="bold")

        button1 = tk.Button(window, text="Beginners Level", command=open_window1, bg=button_colors[0], fg="white",
                            font=button_font, relief="solid", bd=0, activebackground="#FFA067")
        button2 = tk.Button(window, text="Intermediate Level", command=open_window2, bg=button_colors[1], fg="white",
                            font=button_font, relief="solid", bd=0, activebackground="#FF8181")
        button3 = tk.Button(window, text="Expert Level", command=open_window3, bg=button_colors[2], fg="white",
                            font=button_font, relief="solid", bd=0, activebackground="#8A4DFF")

        # Position buttons in the center
        button1.place(relx=0.5, rely=0.4, anchor="center")
        button2.place(relx=0.5, rely=0.5, anchor="center")
        button3.place(relx=0.5, rely=0.6, anchor="center")

        # Create a label name for the window screen
        label_font = font.Font(family="Algerian", size=20, weight="bold")
        label = tk.Label(window, text="NovaPy: Python Tutorial", bg=background_color, fg="black", font=label_font)

        # Position the label in the center
        label.place(relx=0.5, rely=0.2, anchor="center")

        # Add a black border around the window
        window.attributes("-alpha", 0.9)  # Set window transparency
        window.wm_attributes("-topmost", True)  # Keep the window on top
        window.configure(borderwidth=10, relief="solid", bd=0)  # Set the border properties

        # Add an exit button
        exit_button = tk.Button(window, text="Exit", command=exit_program, bg="black", fg="white",
                                font=button_font, relief="solid", bd=0, activebackground="#808080")
        exit_button.place(relx=1, rely=1, anchor="se")  # Position at bottom-right corner

        # Start the Tkinter event loop
        window.mainloop()




        
     
  

    screen2()
