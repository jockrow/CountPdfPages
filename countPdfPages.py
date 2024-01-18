import os
import PyPDF2
import zipfile
import xml.dom.minidom
import warnings
import gettext
import logging
import locale
from typing import Iterable
from gettext import translation
import configparser

logger = logging.getLogger("PyPDF2")
logger.setLevel(logging.ERROR)

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
language = config.get("Settings", "language")
languages = [language]
# print(f"languages: {language}")

# if language != "en":
desired_language = language
languages = [desired_language]
# Initialize the translation system
translations = translation("messages", localedir="locales", languages=languages)
translations.install()

total_pages = 0


def printMessage(num_pages, file_name):
    global total_pages
    print(str(num_pages) + "\t" + file_name)
    total_pages += num_pages


def countPdfPages():
    current_page = str(os.getcwd())

    for archiveDirPath, dirNames, fileNames in os.walk(current_page):
        for file_name in fileNames:
            # TODO: when can't open the file pass to next and register and log
            extension = os.path.splitext(file_name)[1]
            try:
                if extension == ".pdf":
                    pdf = PyPDF2.PdfReader(file_name)
                    printMessage(len(pdf.pages), file_name)
                elif extension == ".docx":
                    document = zipfile.ZipFile(file_name)
                    dxml = document.read("docProps/app.xml")
                    uglyXml = xml.dom.minidom.parseString(dxml)
                    printMessage(
                        int(
                            uglyXml.getElementsByTagName("Pages")[0]
                            .childNodes[0]
                            .nodeValue
                        ),
                        file_name,
                    )
            except Exception as exc:
                print("...Exception: " + str(exc))

    if total_pages == 0:
        print("Files not found")
        quit()

    print(str(total_pages) + "\t" + _("Total Pages"))


countPdfPages()

