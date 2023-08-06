# Calculator

This is a simple calculator program written in Python. 
It performs basic arithmetic operations such as:
- addition, subtraction, multiplication, and division.

### To use the calculator, follow these steps:
Make sure you have Python3 installed on your system.
Run below command: 
```bash
pip install m1nx4s-calculator - to install package
```
In *.py file paste:
```bash
from calculator import calculator - to import package
```
## Usage
```bash
obj = Calculator()
choice = 1  # number should be higher than 1

while choice != 0:  # if not = 0 will proceed with calculation
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
print("0. Exit")
try:
choice = int(input("Enter choice: "))
if choice >= 5 or choice < 0:
print("Invalid choice, choose the number from 0 to 4!!")
continue
if choice != 0:
num = int(input("Enter number: "))
except ValueError:
print("It is a letter, Please Enter an integer")
continue
if choice == 1:
print("Result: ", obj.add(num))
elif choice == 2:
print("Result: ", obj.sub(num))
elif choice == 3:
print("Result: ", obj.mul(num))
elif choice == 4:
print("Result: ", obj.div(num))
elif choice == 0:
print("Exiting!", obj.reset())
```

## Features
### The calculator supports the following features:
- Addition: Adds two numbers together.
- Subtraction: Subtracts the second number from the first number.
- Multiplication: Multiplies two numbers together. 
- Division: Divides the first number by the second number.
- Memory: calculator has its own memory
- Reset: 0 selection exits from calculator and reset memory

## Test case
- Execution of test case with below command in correct path: 
```bash
"python -m unittest .\tests\test_calculator.py -v"
```

## License
This project is licensed under the MIT License. 
Feel free to use and modify it according to your needs.

## Contact
If you have any questions or need assistance, you can reach me at m.kancevicius@gmail.com.