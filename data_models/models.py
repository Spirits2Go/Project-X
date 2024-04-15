from __future__ import annotations

from datetime import date

from typing import List
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Base(DeclarativeBase):
    '''
    Basis Klasse für unser Model. Daraus kann SQLAlchemy herleiten welche Klassen zu unserem Modell gehören.
    '''
    pass


class Address(Base):
    '''
    Adress Entitätstyp.
    '''
    __tablename__ = "address"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    street: Mapped[str] = mapped_column("street")
    zip: Mapped[str] = mapped_column("zip")
    city: Mapped[str] = mapped_column("city")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, street={self.street!r}, city={self.city!r}, zip={self.zip!r})"


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    name: Mapped[str] = mapped_column("name", unique=True)
    access_level: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r}, access_level={self.access_level!r})"


class Login(Base):
    __tablename__ = "login"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    username: Mapped[str] = mapped_column("username", unique=True)
    password: Mapped[str] = mapped_column("password")
    role_id: Mapped[int] = mapped_column("role_id", ForeignKey("role.id"))
    role: Mapped[Role] = relationship()

    def __repr__(self):
        return f"Login(id={self.id!r}, username={self.username!r}, password={self.password!r}, role={self.role!r})"


class Guest(Base):
    '''
    Gast Entitätstyp.
    '''
    __tablename__ = "guest"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    firstname: Mapped[str] = mapped_column("firstname")
    lastname: Mapped[str] = mapped_column("lastname")
    email: Mapped[str] = mapped_column("email")
    address_id: Mapped[int] = mapped_column("address_id", ForeignKey("address.id"))
    address: Mapped["Address"] = relationship()
    bookings: Mapped[List["Booking"]] = relationship(back_populates="guest")

    type: Mapped[str]
    __mapper_args__ = {
        "polymorphic_identity": "guest",
        "polymorphic_on": "type",
    }

    def __repr__(self) -> str:
        return f"Guest(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r}, address={self.address!r})"


class RegisteredGuest(Guest):
    '''
    Registrier Gast Entitätstyp.
    '''
    __tablename__ = "registred_guest"

    id: Mapped[int] = mapped_column("id", ForeignKey("guest.id"), primary_key=True)
    login_id: Mapped[int] = mapped_column("login_id", ForeignKey("login.id"))
    login: Mapped[Login] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "registered"
    }

    def __repr__(self) -> str:
        return f"RegisteredGuest(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r}, email={self.email!r}, address={self.address!r})"


class Hotel(Base):
    '''
    Hotel Entitätstyp.
    '''
    __tablename__ = "hotel"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    stars: Mapped[int] = mapped_column("stars", default=0)
    address_id: Mapped[int] = mapped_column("address_id", ForeignKey("address.id"))
    address: Mapped["Address"] = relationship()
    rooms: Mapped[List["Room"]] = relationship(back_populates="hotel")

    def __repr__(self) -> str:
        return f"Hotel(id={self.id!r}, name={self.name!r}, stars={self.stars}, address={self.address})"


class Room(Base):
    '''
    Raum Entitätstyp.
    '''
    __tablename__ = "room"

    hotel_id: Mapped[int] = mapped_column("hotel_id", ForeignKey("hotel.id"), primary_key=True)
    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    number: Mapped[str] = mapped_column("number", primary_key=True)
    type: Mapped[str] = mapped_column("type", nullable=True) # e.g. "family room", "single room", etc.
    max_guests: Mapped[int] = mapped_column("max_guests")
    description: Mapped[str] = mapped_column("description", nullable=True) # e.g. "Room with sea view"
    amenities: Mapped[str] = mapped_column("amenities", nullable=True)
    price: Mapped[float] = mapped_column("price")

    def __repr__(self) -> str:
        return f"Room(hotel={self.hotel!r}, room_number={self.number!r}, type={self.type!r}, description={self.description!r}, amenities={self.amenities!r}, price={self.price!r})"


class Booking(Base):
    '''
    Buchungs Entitätstyp.
    '''
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    room_hotel_id: Mapped[int] = mapped_column("room_hotel_id")
    room_number: Mapped[str] = mapped_column("room_number")
    room: Mapped["Room"] = relationship()
    guest_id: Mapped[int] = mapped_column("guest_id", ForeignKey("guest.id"))
    guest: Mapped["Guest"] = relationship(back_populates="bookings")
    number_of_guests: Mapped[int] = mapped_column("number_of_guests")
    start_date: Mapped[date] = mapped_column("start_date")
    end_date: Mapped[date] = mapped_column("end_date")
    comment: Mapped[str] = mapped_column("comment", nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['room_hotel_id', 'room_number'],
            ['room.hotel_id', 'room.number'],
        ),
    )

    def __repr__(self) -> str:
        return f"Booking(room={self.room!r}, guest={self.guest!r}, start_date={self.start_date!r}, end_date={self.end_date!r}, comment={self.comment!r})"
