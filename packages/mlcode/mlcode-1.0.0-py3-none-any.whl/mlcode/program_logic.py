import os

# Path to the programs folder
PROGRAMS_FOLDER = os.path.join(os.path.dirname(__file__), "programs")

def program(number):
    """Load and return the contents of a program file based on the number."""
    file_name = f"program{number}.txt"
    file_path = os.path.join(PROGRAMS_FOLDER, file_name)
    
    if not os.path.exists(file_path):
        return f"Program {number} not found."
    
    with open(file_path, "r") as file:
        return file.read()
