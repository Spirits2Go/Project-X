import os


class Console(object):
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError("Implement this method")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')


class Application(object):

    def __init__(self, start: Console):
        self._current: Console = start

    def run(self):
        while self._current:
            self._current = self._current.run()


class MenuOption(object):
    def __init__(self, title):
        self._title = title

    def get_title(self) -> str:
        return self._title

    def __str__(self):
        return self._title

    def __len__(self):
        return len(self._title)


class Menu(Console):
    def __init__(self, title, width=50):
        super().__init__()
        self._title = title
        self._options = []
        self._width = width

    def __iter__(self):
        return iter(self._options)

    def get_options(self) -> list:
        return self._options

    def add_option(self, option: MenuOption):
        self._options.append(option)

    def remove_option(self, option: MenuOption):
        self._options.remove(option)

    def _show(self):
        print("#" * self._width)
        left = "# "
        right = "#"
        space = " " * (self._width - len(left) - len(self._title) - len(right))
        print(f"{left}{self._title}{space}{right}")
        print("#" * self._width)
        for i, option in enumerate(self, 1):
            index = f"{i}: "
            space = " " * (self._width - len(left) - len(index) - len(option) - len(right))
            print(f"{left}{index}{option}{space}{right}")
        print("#" * self._width)

    def _make_choice(self) -> int:
        choice = input("Enter Option: ")
        options = [f"{i}" for i, option in enumerate(self._options, 1)]
        while choice not in options:
            self._show()
            print("Invalid Option")
            choice = input("Enter Option: ")
        return int(choice)

    def _navigate(self, choice: int):
        raise NotImplementedError("Implement this method")

    def run(self) -> Console:
        self.clear()
        self._show()
        return self._navigate(self._make_choice())
