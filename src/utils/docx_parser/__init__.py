




class DocxParserService():

    def __init__(self) -> None:
        import docx
        import pathlib

        self.docx = docx
        self.pathlib = pathlib
        self.current_path = pathlib.Path(__file__).parent.resolve()

    async def __call__(self, file_path: str):
        async def proccess_docx_db():
            word_path = self.current_path.joinpath(self.pathlib.Path(file_path))

            doc = self.docx.Document(word_path)

            for i, paragraph in enumerate(doc.paragraphs):
                if i != 0:
                    _, right_text = paragraph.text.rsplit('.')
                    text, _ = right_text.split('*')
                    return text

        return await proccess_docx_db()


my_showcase_service = DocxParserService()
