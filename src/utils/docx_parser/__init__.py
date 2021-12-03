from functools import cached_property
from enum import Enum
from typing import Mapping


class FieldResolve(str, Enum):
    startup_name = 'Наименование команды/организации'
    stage = 'Стадия готовности продукта'
    description = 'Краткое описание продукта'
    cases = 'Кейсы использования продукта'
    benefit = 'Польза продукта'
    transport = 'Организация Московского транспорта, интересная в первую очередь'
    acceleration = ''
    certification = ''
    full_name = ''
    position = ''
    phone = ''
    legal_entity = ''
    tax_id_number = ''
    personal_count = ''

    @staticmethod
    def repr_map() -> Mapping:
        return {
            "startup_name": tuple(),
            "stage": tuple(),
            "description": tuple(),
            "cases":  tuple(),
            "benefit": tuple(),
            "transport": tuple(),
            "acceleration": tuple(),
            "certification": ('да, требуется сертификация и у нас она есть',
                              'да, требуется сертификация, но  у нас ее нет',
                              'нет, не требуется'),
            "full_name": tuple(),
            "position": tuple(),
            "phone": tuple(),
            "legal_entity": tuple(),
            "tax_id_number": tuple(),
            "personal_count": ('Менее 20', 'от 20 до 100', 'от 100 до 500', 'более 500')
        }

    @cached_property
    def repr_doc(self) -> Mapping:
        return (

        )


class DocxParserService():

    def __init__(self) -> None:
        import docx
        import pathlib

        self.docx = docx
        self.pathlib = pathlib
        self.current_path = pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve().parent.resolve()
        self.field_resolve = FieldResolve

    async def __call__(self, file_path: str):
        def get_assets_folder():
            ...
        async def proccess_docx_db():
            word_path = self.current_path.joinpath(self.pathlib.Path(f"assets/{file_path}"))

            doc = self.docx.Document(word_path)

            i = 0
            result = {}
            form_fields = self.field_resolve.repr_map().keys()
            for paragraph, field_name in zip(doc.paragraphs, form_fields):
                if i != 0:
                    result[field_name] = paragraph.text
                i += 1
            return result

        return await proccess_docx_db()


my_docx_parser_service = DocxParserService()
