# Hector --- A collection manager.
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import datetime
from typing import Type

import bl3d
from isbnlib import is_isbn13, mask

from bl_hector.domain.collection_management.errors import IncorrectValue


class String(bl3d.String):
    @classmethod
    def instanciate(cls: Type[bl3d.TypeString], value: str) -> bl3d.TypeString:
        try:
            return super().instanciate(value)
        except bl3d.InvalidValue as exc:
            raise IncorrectValue(cls.__name__, str(exc).split(":", 1)[1])


class Integer(bl3d.Integer):
    @classmethod
    def instanciate(cls: Type[bl3d.TypeInteger], value: int) -> bl3d.TypeInteger:
        try:
            return super().instanciate(value)
        except bl3d.InvalidValue as exc:
            raise IncorrectValue(cls.__name__, str(exc).split(":", 1)[1])


class Date(bl3d.Date):
    @classmethod
    def instanciate(cls: Type[bl3d.TypeDate], value: datetime.date) -> bl3d.TypeDate:
        try:
            return super().instanciate(value)
        except bl3d.InvalidValue as exc:
            raise IncorrectValue(cls.__name__, str(exc).split(":", 1)[1])


class Isbn(String):
    """
    The International Standard Book Number (ISBN) of a book,
    for instance 978-0-7653-9277-0.
    """

    MIN = 13
    MAX = 17  # 13 numbers plus 4 `-` for masked ISBN

    @classmethod
    def instanciate(cls, value: str) -> "Isbn":
        __value = value.replace("-", "")

        super().instanciate(__value)
        if is_isbn13(__value):
            return cls(__value)

        raise IncorrectValue(cls.__name__, "This value doesn't look like an ISBN-13.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Isbn):
            return NotImplemented
        # Isbn built with `__init__` might still contain `-`,
        # for instance, the ones loaded from the database
        return str(other) == str(self)

    def __str__(self) -> str:
        return str(mask(super().__str__()))


class Title(String):
    MIN = 1
    MAX = 256


class Author(String):
    MIN = 1
    MAX = 64


class Authors:
    list_of_authors: list[Author]

    def __init__(self, authors_as_list: str) -> None:
        self.list_of_authors = [Author(a.strip()) for a in authors_as_list.split(",")]

    def __str__(self) -> str:
        return ", ".join([str(a) for a in self.list_of_authors])


class Genre(String):
    MIN = 1
    MAX = 64


class Year(Integer):
    # Books published before the introduction of the ISBN system can have an ISBN!
    MIN = 1900


class Cover(String):
    MIN = 1
