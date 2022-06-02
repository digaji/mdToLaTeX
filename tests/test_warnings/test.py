import sys, os
sys.path.append(os.getcwd() + f"\\src")

from main import generate_latex

def main():
    generate_latex("tests/test_warnings/warnings.md", "tests/test_warnings/warnings.tex")

if __name__ == "__main__":
    main()