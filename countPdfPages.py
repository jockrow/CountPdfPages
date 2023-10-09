import os
import PyPDF2
import zipfile
import xml.dom.minidom
import warnings

warnings.filterwarnings("ignore")


def countPdfPages():
    current_page = str(os.getcwd())
    total_pages = 0

    for (archiveDirPath, dirNames, fileNames) in os.walk(current_page):
        for file_name in fileNames:
            extension = os.path.splitext(file_name)[1]
            if extension == ".pdf":
                pdf = PyPDF2.PdfFileReader(file_name)
                total_pages += pdf.getNumPages()
            elif extension == ".docx":
                document = zipfile.ZipFile(file_name)
                dxml = document.read('docProps/app.xml')
                uglyXml = xml.dom.minidom.parseString(dxml)
                total_pages += int(uglyXml.getElementsByTagName('Pages')
                                   [0].childNodes[0].nodeValue)

    if total_pages == 0:
        print("No se encontraron archivos PDF")
        quit()

    print("Pdf Páginas Totales:\t" + str(total_pages))


countPdfPages()
