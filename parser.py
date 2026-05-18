import PyPDF2

def extract_text_from_pdf(pdf_file):
    text = ""

    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            text += page.extract_text()

    return text