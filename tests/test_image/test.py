import sys, os
sys.path.append(os.getcwd() + f"\\src")

from main import generate_latex

def main():
    generate_latex("tests/test_image/image.md", "tests/test_image/image.tex")

if __name__ == "__main__":
    main()