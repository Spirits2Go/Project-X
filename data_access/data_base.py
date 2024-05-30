import os
from pathlib import Path
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker

from data_models.models import Base, Role, Login, Address, Hotel, Room, Booking, RegisteredGuest, Guest
from data_access.data_generator import generate_system_data, generate_hotels, generate_guests, generate_registered_guests, generate_random_bookings, generate_random_registered_bookings

def init_db(file_path: str, create_ddl: bool = False, generate_example_data: bool = False, verbose: bool = False):
    path = Path(file_path)
    data_folder = path.parent
    engine = create_engine(f"sqlite:///{file_path}")

    if path.is_file():
        Base.metadata.drop_all(engine)
    else:
        if not data_folder.exists():
            data_folder.mkdir(parents=True)

    Base.metadata.create_all(engine)

    if create_ddl:
        with open(path.with_suffix(".ddl"), "w") as ddl_file:
            for table in Base.metadata.tables.values():
                create_table = str(CreateTable(table).compile(engine)).strip()
                ddl_file.write(f"{create_table};{os.linesep}")

    if generate_example_data:
        generate_system_data(engine, verbose=verbose)
        generate_hotels(engine, verbose=verbose)
        generate_guests(engine, verbose=verbose)
        generate_registered_guests(engine, verbose=verbose)
        generate_random_bookings(engine, verbose=verbose)
        generate_random_registered_bookings(engine, verbose=verbose)

        with sessionmaker(bind=engine)() as session:
            admin_role = Role(name='admin', access_level=10)
            user_role = Role(name='user', access_level=1)
            admin_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_password = bcrypt.hashpw('user'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            session.add_all([
                admin_role,
                user_role,
                Login(username='admin', password=admin_password, role=admin_role),
                Login(username='user', password=user_password, role=user_role)
            ])
            session.commit()
            if verbose:
                print("Added example roles and users.")
