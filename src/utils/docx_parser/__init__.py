
import docx
import pathlib

STARTUP_APPLICATION = 'startup_form.docx'
cur_path = pathlib.Path(__file__).parent.resolve()
word_path = cur_path.joinpath(pathlib.Path(STARTUP_APPLICATION))

doc = docx.Document(word_path)
properties = doc.core_properties


for i, paragraph in enumerate(doc.paragraphs):
    if i != 0:
        _, right_text = paragraph.text.rsplit('.')
        text, _ = right_text.split('*')
        print(text)
