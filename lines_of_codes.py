import os

# Define a function to count the lines of code in a file with a given extension
def count_lines(filename, extension):
    with open(filename, encoding='ISO-8859-1') as f:
        return sum(1 for line in f if line.strip() and line.strip()[0] != "#" and line.strip()[0] != "/" and filename.endswith(extension))


# Define a function to count the lines of code in a directory
def count_directory(dirname):
    # Initialize counters for each programming language
    html_count = 0
    css_count = 0
    js_count = 0
    py_count = 0

    # Traverse the directory tree and count the lines of code in each file
    for dirpath, _, filenames in os.walk(dirname):
        if "venv" in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(".html"):
                html_count += count_lines(os.path.join(dirpath, filename), ".html")
            elif filename.endswith(".css"):
                css_count += count_lines(os.path.join(dirpath, filename), ".css")
            elif filename.endswith(".js"):
                js_count += count_lines(os.path.join(dirpath, filename), ".js")
            elif filename.endswith(".py"):
                py_count += count_lines(os.path.join(dirpath, filename), ".py")

    # Print the results
    print("HTML: {} lines".format(html_count))
    print("CSS: {} lines".format(css_count))
    print("JS: {} lines".format(js_count))
    print("Python: {} lines".format(py_count))


# Call the count_directory function with the path to your Django project directory
count_directory(".")
