import os
import shutil as sh

from pathlib import Path
from src.htmlnode import ParentNode
from src.exceptions import ValueNotFoundError

from src.logger import logger
from src.text_block import markdown_to_html_node, paragraph_to_html_node

def copy_tree(src: str, dst: str) -> None:
    
    if os.path.exists(dst):
        logger.info(f"copy_tree(): Removing existing destination: '{dst}'")
        sh.rmtree(dst)
    os.makedirs(dst)
    logger.info(msg=f"copy_tree(): Created destination directory: '{dst}'")

    for item in os.listdir(src):
        curr_src = os.path.join(src, item)

        if os.path.isfile(curr_src):
            logger.info(msg=f"copy_tree(): Copying from '{curr_src}' to '{dst}'")
            sh.copy(src=curr_src, dst=dst)

        if os.path.isdir(curr_src):
            curr_dst = os.path.join(dst, item)
            logger.info(msg=f"copy_tree(): Creating dir '{item}' at {curr_dst}") 
            os.mkdir(curr_dst)
            copy_tree(src=curr_src, dst=curr_dst)

def read_markdown(markdown: str | Path) -> str:
    with Path(markdown).open() as file:
        return file.read()
    
def extract_title(markdown: str | Path ) -> str:
    file = read_markdown(markdown)
    
    if len(file) == 0 or "#" not in file:
        raise ValueNotFoundError("No header found in file")
    
    for seg in file.split("\n"):
        if seg[0] == "#" in seg and seg[1] == " ":
            return seg.replace("# ", "").strip()
        

def generate_page(
    src: str | Path, 
    dst: str | Path,
    template_path: str | Path 
) -> None:

    logger.info(f"Generating page from '{src}' to '{dst}' using '{template_path}'")

    source_md = read_markdown(src)
    title = extract_title(src)
    source_html = markdown_to_html_node(source_md).to_html()
    template_md = read_markdown(template_path)
    templated_html = template_md.replace("{{ Title }}", title).replace("{{ Content }}", source_html)

    with Path(dst).open("w") as file:
        file.write(templated_html)
    
    logger.info(f"Generated new HTML to '{dst}'")

def generate_page_recursive(
    src: str | Path, 
    dst: str | Path,
    template_path: str | Path
):

    for item in filter(lambda x: not x.startswith('.'), os.listdir(src)):
        curr_src = os.path.join(src, item)
        curr_dst = os.path.join(dst, item)
        
        if os.path.isfile(curr_src):
            logger.info(msg=f"generate_page_recursive(): Generating HTML from file '{curr_src}' into '{dst}'")
            generate_page(curr_src, curr_dst.replace(".md", ".html"), template_path)

        if os.path.isdir(curr_src):
            logger.info(msg=f"generate_page_recursive(): Creating dir '{item}' at {curr_dst}") 
            os.mkdir(curr_dst)
            generate_page_recursive(curr_src, curr_dst, template_path)