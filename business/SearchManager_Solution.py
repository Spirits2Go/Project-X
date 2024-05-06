import os
from pathlib import Path

from data_access.data_base import init_db
from sqlalchemy import select, func, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from data_models.models import *


class SearchManager(object):
    def __init__(self) -> None:
        self.__load_db()

    def __load_db(self):
        # Ensure the environment Variable is set
        if not os.environ.get("DB_FILE"):
            raise ValueError("You have to define the environment variable 'DB_FILE'")
        self.__db_filepath = Path(os.environ.get("DB_FILE"))

        # Ensure the db file exists, if not initialize a new db with or without example data
        # You have to delete the db file, if you need a new fresh db.
        if not self.__db_filepath.is_file():
            init_db(str(self.__db_filepath), generate_example_data=True)

        self._engine = create_engine(f'sqlite:///{self.__db_filepath}')
        self._session = scoped_session(sessionmaker(bind=self._engine))

    def get_hotels(self, name: str = "", city: str = ""):
        query = select(Hotel)
        if name != "":
            query = query.where(Hotel.name.like(f'%{name}%'))
        if city != "":
            query = query.join(Address).where(Address.city.like(f"%{city}%"))

        print(query)
        return self._session.execute(query).scalars().all()

    def get_hotels_by_name(self, name: str = ""):
        query = select(Hotel)
        if name != "":
            query = query.where(Hotel.name.like(f'%{name}'))
        print(query)
        return self._session.execute(query).scalars().all()

    def get_hotels_by_city(self, city: str = ""):
        query = select(Hotel)
        if city != "":
            query = query.join(Address).where(Address.city.like(f"%{city}%"))
        print(query)
        return self._session.execute(query).scalars().all()


def show(hotels):
    for hotel in hotels:
        print(hotel)


if __name__ == '__main__':
    # This is only for testing without Application

    # You should set the environment variable in the run configuration.
    # However, we can set it here in python as well.
    # Because we are executing this file in the folder ./business/
    # we need to relatively navigate first one folder up and therefore,
    # use ../data in the path instead of ./data
    # if the environment variable is not set, set it to a default
    if not os.environ.get("DB_FILE"):
        os.environ["DB_FILE"] = input("Enter relative Path to db file: ")
        while not Path(os.environ.get("DB_FILE")).parent.is_dir():
            os.environ["DB_FILE"] = input("Enter relative Path to db file: ")
    search_manager = SearchManager()
    all_hotels = search_manager.get_hotels()
    show(all_hotels)
    input("Press Enter to continue...")

    city_in = input('City: ')
    hotels_by_city = search_manager.get_hotels_by_city(city_in)
    show(hotels_by_city)
    input("Press Enter to continue...")

    name_in = input('Name: ')
    city_in = input('City: ')
    found_hotels = search_manager.get_hotels(name_in, city_in)
    show(found_hotels)
    input("Press Enter to continue...")
