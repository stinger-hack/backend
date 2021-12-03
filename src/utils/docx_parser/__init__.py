
import docx
import pathlib

STARTUP_APPLICATION = 'startup_form.docx'
cur_path = pathlib.Path(__file__).parent.resolve()
word_path = cur_path.joinpath(pathlib.Path(STARTUP_APPLICATION))

doc = docx.Document(word_path)
properties = doc.core_properties

def process_field():
    ...

text = []

for paragraph in doc.paragraphs:
    text.append(paragraph.text[:-2])

print('\n'.join(text))