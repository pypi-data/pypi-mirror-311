##
# Copyright (c) STÜBER SYSTEMS GmbH
# Licensed under the MIT License, Version 2.0. 
##

class CantonSummary:
    """
    Reduced representation of a Swiss canton (Kanton)
    """

    def __init__(self, key, name, code):
        self.key = key
        self.name = name
        self.code = code

    @classmethod
    def from_json(cls, data):
        return None if not data else cls(
            key=data.get("key"),
            name=data.get("name"),
            code=data.get("code")
        ) 
