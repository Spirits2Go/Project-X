import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable

from data_models.models import *
from data_access.data_generator import *

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