# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 10:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Graph.py
from ultipa.structs.BaseModel import BaseModel

class GraphSet(BaseModel):
    id: int
    name: str
    totalNodes: int
    totalEdges: int
    description: str
    status: str

    def __init__(self, name: str, id: int = None, totalNodes: int = None,
                 totalEdges: int = None, description: str = None, status: str = None):
        self.id = id
        self.name = name
        self.totalNodes = totalNodes
        self.totalEdges = totalEdges
        self.description = description
        self.status = status



