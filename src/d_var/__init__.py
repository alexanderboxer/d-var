from d_var.common import get_project_root
from d_var.sources import get_external_files
from d_var.templates import create_template_datafiles
from d_var.parser import torah, verse
from d_var.web import chapter_to_html


def main() -> None:
    print("Hello from d-var!")
