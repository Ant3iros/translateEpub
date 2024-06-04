import os
from crewai import Agent, Task, Crew, Process
from decouple import config
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from gtts import gTTS
from agents import CustomAgents
from tasks import CustomTasks

# Assurez-vous que les bibliothèques nécessaires sont installées:
# pip install ebooklib beautifulsoup4 requests python-decouple gtts

epub_path = "Bossgrot.epub"
result_epub_path = "result.epub"
output_text_file = "traduction.txt"
output_audio_file = "traduction.mp3"
skip = 0
CHAR_LIMIT = 4000  # Le nombre maximum de caractères par bloc

class CustomCrew:
    def __init__(self, text_section):
        self.text_section = text_section

    def run(self):
        agents = CustomAgents()
        tasks = CustomTasks()

        translator = agents.translator()

        translate = tasks.translate(
            translator,
            self.text_section
        )

        crew = Crew(
            agents=[translator],
            tasks=[translate],
            verbose=True,
        )

        result = crew.kickoff()
        return result

def save_translations_to_file(translations, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for section in translations:
            f.write(section + "\n\n")

def extract_sections_from_epub(epub_path, char_limit):
    book = epub.read_epub(epub_path)
    sections = []
    current_section = ""
    current_length = 0

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            for paragraph in soup.find_all('p'):
                paragraph_text = paragraph.get_text()
                if current_length + len(paragraph_text) > char_limit:
                    sections.append(current_section)
                    current_section = paragraph_text
                    current_length = len(paragraph_text)
                else:
                    if current_section:
                        current_section += " " + paragraph_text
                    else:
                        current_section = paragraph_text
                    current_length += len(paragraph_text)

    if current_section:
        sections.append(current_section)
    
    return sections

def create_epub_from_txt(txt_file, epub_file, title="Title", author="Author"):
    # Read the content from the text file
    with open(txt_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content into paragraphs based on double newlines
    paragraphs = content.split('\n\n')

    # Create an EPUB book
    book = epub.EpubBook()

    # Set the metadata
    book.set_identifier('id123456')
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # Create an EPUB chapter from the text content
    chapter_content = f'<h1>{title}</h1>'
    for para in paragraphs:
        # Replace single newlines within paragraphs with <br /> for line breaks
        para = para.replace("\n", "<br />")
        chapter_content += f'<p>{para}</p>'

    chapter = epub.EpubHtml(title=title, file_name='chap_01.xhtml', lang='en')
    chapter.content = chapter_content

    # Add chapter to the book
    book.add_item(chapter)

    # Define Table Of Contents
    book.toc = (epub.Link('chap_01.xhtml', title, 'intro'),)

    # Add default NCX and Nav files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: Times, serif;
    }
    h1 {
        text-align: center;
    }
    p {
        text-align: justify;
    }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # Add CSS file
    book.add_item(nav_css)

    # Create spine
    book.spine = ['nav', chapter]

    # Write the EPUB file
    epub.write_epub(epub_file, book, {})

def text_to_speech(text_file, output_audio_file):
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()

    tts = gTTS(text, lang='fr')
    tts.save(output_audio_file)

if __name__ == "__main__":
    sections = extract_sections_from_epub(epub_path, CHAR_LIMIT)
    translated_sections = []
    i = 0

    for section in sections:
        if i >= skip:
            custom_crew = CustomCrew(section)
            result = custom_crew.run()
            translated_sections.append(result)
            save_translations_to_file(translated_sections, output_text_file)
        print(i)
        i = i + 1

    #(txt_file, epub_file, title="Title", author="Author")
    create_epub_from_txt(output_text_file, result_epub_path, epub_path, "script Benjamin De Almeida")
    #text_to_speech(output_text_file, output_audio_file)
