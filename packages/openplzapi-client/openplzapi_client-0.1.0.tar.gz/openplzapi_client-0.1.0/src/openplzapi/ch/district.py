##
# Copyright (c) STÜBER SYSTEMS GmbH
# Licensed under the MIT License, Version 2.0. 
##

from openplzapi.ch.canton_summary import CantonSummary

class District:
    """
    Representation of a Swiss district (Bezirk)
    """

    def __init__(self, name, key, canton):
        self.name = name
        self.key = key
        self.canton = canton

    @classmethod
    def from_json(cls, data):
        return cls(
            key=data.get("key"),
            name=data.get("name"),
            canton=CantonSummary.from_json(data.get("canton")))
