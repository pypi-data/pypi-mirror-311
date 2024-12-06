# -*- coding: utf-8 -*-
# @Time    : 2024/05/14 11:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Privilege.py
from typing import List
from ultipa.structs.BaseModel import BaseModel


class Process(BaseModel):
    '''
        Data class for Privilege.
    '''

    def __init__(self, processId: str, processUql: str, duration: str):
        self.processId = processId
        self.processUql = processUql
        self.duration = duration
