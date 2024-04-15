import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sqlalchemy.schema import CreateTable

from data_models.models import *

from data_access.data_generator import generate_hotels, generate_guests, generate_registered_guests, generate_random_bookings, \
    generate_random_registered_bookings


def load_data_from_sqlite():
    data_path = Path(os.getcwd()).joinpath("data")
    data_path.mkdir(exist_ok=True)

    engine = create_engine("sqlite:///data/example.data_access")
    with open(data_path.joinpath("example.ddl"), "w") as ddl_file:
        for table in Base.metadata.tables.values():
            create_table = str(CreateTable(table).compile(engine)).strip()
            ddl_file.write(f"{create_table};{os.linesep}")

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    generate_hotels(engine)
    with Session(engine) as session:
        result = session.query(Hotel).all()
        for hotel in result:
            print(f"{hotel}")
            for room in hotel.rooms:
                print(f"{' ' * 5}{room}")
                for amenity in room.amenities:
                    print(f"{' ' * 10}{amenity}")

    print()
    print("#" * 20 + "Guests" + "#" * 20)
    generate_guests(engine)
    with Session(engine) as session:
        result = session.query(Guest).all()
        for guest in result:
            print(f"{guest}")

    print()
    print("#" * 20 + "Bookings" + "#" * 20)
    generate_random_bookings(engine)
    with Session(engine) as session:
        result = session.query(Booking).all()
        for booking in result:
            print(f"{booking}")

    print()
    print("#" * 20 + "Registered Guests" + "#" * 20)
    generate_registered_guests(engine)
    with Session(engine) as session:
        result = session.query(RegisteredGuest).all()
        for registered_guest in result:
            print(f"{registered_guest}")

    print()
    print("#" * 20 + "Registered Bookings" + "#" * 20)
    generate_random_registered_bookings(engine, k=5)
    with Session(engine) as session:
        result = session.query(Booking, RegisteredGuest).filter(Booking.guest.of_type(RegisteredGuest)).all()
        for booking in result:
            print(f"{booking}")
