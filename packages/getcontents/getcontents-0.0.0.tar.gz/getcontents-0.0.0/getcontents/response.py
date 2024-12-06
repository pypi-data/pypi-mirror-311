# Copyright (c) 2024 nggit

import json


class Response:
    def __init__(self, header, body, reader, writer):
        self._header = header
        self._body = body
        self._reader = reader
        self._writer = writer

    @property
    def header(self):
        return self._header

    @property
    def body(self):
        return self._body

    @property
    def reader(self):
        return self._reader

    @property
    def writer(self):
        return self._writer

    def json(self, **kwargs):
        return json.loads(self._body, **kwargs)
