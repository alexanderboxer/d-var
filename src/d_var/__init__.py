import argparse

from d_var.common import get_project_root
from d_var.sources import get_external_files
from d_var.templates import create_template_datafiles, create_word_templates
from d_var.parser import torah, verse
from d_var.web import chapter_to_html


def main() -> None:
    parser = argparse.ArgumentParser(prog='d-var', description='Hebrew Bible text analysis')
    subparsers = parser.add_subparsers(dest='command')

    # d-var download
    subparsers.add_parser('download', help='Download external data sources (Sefaria, OpenScriptures)')

    # d-var templates
    subparsers.add_parser('templates', help='Generate template files for hand-parsed data')

    # d-var words
    subparsers.add_parser('words', help='Generate per-chapter word template files for hand-parsing')

    # d-var build
    build_parser = subparsers.add_parser('build', help='Generate HTML chapter pages')
    build_parser.add_argument('book', nargs='?', default='genesis', help='Book name (default: genesis)')
    build_parser.add_argument('chapter', nargs='?', type=int, default=1, help='Chapter number (default: 1)')

    # d-var torah
    subparsers.add_parser('torah', help='Build and print Torah DataFrame info')

    args = parser.parse_args()

    if args.command == 'download':
        get_external_files()
    elif args.command == 'templates':
        create_template_datafiles()
    elif args.command == 'words':
        create_word_templates()
    elif args.command == 'build':
        chapter_to_html(book=args.book, chapter=args.chapter)
    elif args.command == 'torah':
        df = torah()
        print(df)
    else:
        parser.print_help()
