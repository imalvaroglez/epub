import sys
import os
import tempfile
import shutil
import pypandoc
from ebooklib import epub


def convert_to_epub(input_file, output_file):
    try:
        # Convert PDF to HTML using pypandoc
        temp_dir = tempfile.mkdtemp()
        output_html_file = os.path.join(temp_dir, 'output.html')

        # Use pypandoc to convert input_file to HTML (automatically detects format)
        pypandoc.convert_file(input_file, 'html', outputfile=output_html_file)

        # Create EPUB file
        book = epub.EpubBook()
        book.set_identifier('sample123456')
        book.set_title('Sample Book')
        book.set_language('en')

        # Add chapters
        c1 = epub.EpubHtml(title='Introduction',
                           file_name='chap_01.xhtml', lang='en')
        c1.content = open(output_html_file, 'r', encoding='utf-8').read()
        book.add_item(c1)

        # Define Table Of Contents
        book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),)

        # Add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(
            uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

        # Add CSS file
        book.add_item(nav_css)

        # Save EPUB file
        epub.write_epub(output_file, book, {})

        print(f"EPUB conversion successful. Output file: {output_file}")

    except Exception as e:
        print(f"Error converting file: {e}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# Example usage:
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_to_epub.py input_file.pdf output_file.epub")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_to_epub(input_file, output_file)
