#!/usr/bin/env python3
"""This module contains the Base class."""

from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}

class Base():
    """The Base class provides a template for other classes."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a Base instance."""
        sclass = str(self.__class__.__name__)
        if DATA.get(sclass) is None:
            DATA[sclass] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'), TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'), TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Checks if two instances are equal."""
        if type(self) != type(other):
            return False
        if not isinstance(self, Base):
            return False
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """Converts the object to a JSON dictionary."""
        respnd = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                respnd[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                respnd[key] = value
        return respnd

    @classmethod
    def load_from_file(cls):
        """Loads all objects from a file."""
        sclass = cls.__name__
        files_path = ".db_{}.json".format(sclass)
        DATA[sclass] = {}
        if not path.exists(files_path):
            return

        with open(files_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[sclass][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """Saves all objects to a file."""
        sclass = cls.__name__
        files_path = ".db_{}.json".format(sclass)
        objs_json = {}
        for obj_id, obj in DATA[sclass].items():
            objs_json[obj_id] = obj.to_json(True)

        with open(files_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """Saves the current object."""
        sclass = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[sclass][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Removes an object."""
        sclass = self.__class__.__name__
        if DATA[sclass].get(self.id) is not None:
            del DATA[sclass][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Counts all objects."""
        sclass = cls.__name__
        return len(DATA[sclass].keys())

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Returns all objects."""
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """Returns an object by ID."""
        sclass = cls.__name__
        return DATA[sclass].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Searches all objects with matching attributes."""
        sclass = cls.__name__
        def _search(obj):
            if len(attributes) == 0:
                return True
            for k, v in attributes.items():
                if (getattr(obj, k) != v):
                    return False
            return True
        
        return list(filter(_search, DATA[sclass].values()))
