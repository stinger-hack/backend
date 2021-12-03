
import pathlib
STARTUP_APPLICATION = 'startup_form.docx'
cur_path = pathlib.Path(__file__).parent.resolve()
word_path = cur_path.joinpath(pathlib.Path(STARTUP_APPLICATION))
with open(word_path, 'r') as file:
    print(file.encoding)
    print(file.read())
