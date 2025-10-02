import json
from abc import ABC, abstractmethod
from xml.etree import ElementTree


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


class DisplayStrategy(ABC):
    @abstractmethod
    def display(self, book: Book) -> None:
        pass


class ConsoleDisplay(DisplayStrategy):
    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplay(DisplayStrategy):
    def display(self, book: Book) -> None:
        print(book.content[::-1])


class PrintStrategy(ABC):
    @abstractmethod
    def print_book(self, book: Book) -> None:
        pass


class ConsolePrint(PrintStrategy):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrint(PrintStrategy):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class Serializer(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JsonSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        root = ElementTree.Element("book")
        title = ElementTree.SubElement(root, "title")
        title.text = book.title
        content = ElementTree.SubElement(root, "content")
        content.text = book.content
        return ElementTree.tostring(root, encoding="unicode")


class BookService:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.display_strategies = {
            "console": ConsoleDisplay(),
            "reverse": ReverseDisplay(),
        }
        self.print_strategies = {
            "console": ConsolePrint(),
            "reverse": ReversePrint(),
        }
        self.serializers = {
            "json": JsonSerializer(),
            "xml": XmlSerializer(),
        }

    def execute(self, cmd: str, method_type: str) -> None | str:
        if cmd == "display":
            self.display_strategies[method_type].display(self.book)
        elif cmd == "print":
            self.print_strategies[method_type].print_book(self.book)
        elif cmd == "serialize":
            return self.serializers[method_type].serialize(self.book)
        else:
            raise ValueError(f"Unknown command: {cmd}")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    service = BookService(book)
    result = None
    for cmd, method_type in commands:
        result = service.execute(cmd, method_type)
    return result


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
