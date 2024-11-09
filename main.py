from src.utils import copy_tree, generate_page_recursive

def main():
    print("** Static Site Generator **\n")
    copy_tree(src="./static", dst="./public")
    generate_page_recursive(src="./content", dst="./public", template_path="./template.html")

if __name__ == "__main__":
    main()
