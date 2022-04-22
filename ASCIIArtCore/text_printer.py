import sys
from pathlib import Path


class TextPrinter:
    def __init__(self):
        self.art = []

    def add_char(self, char: str) -> None:
        self.art.append(char)

    def save(self, path: Path):
        """ 
            Функция печатает ascii арт в текстовый файл по указанному пути
            Если файл с таким именем уже существует, будет выведено сообщение
            и приложение завершит работу
        """

        if len(self.art) == 0:
            raise Exception('Арт для печати в файл не может быть пустым')

        if path.exists():
            print(f'Текстовый файл с именем {path.name} уже существует')
            sys.exit(1)

        with path.open('w') as file:
            for c in self.art:
                file.write(c)
