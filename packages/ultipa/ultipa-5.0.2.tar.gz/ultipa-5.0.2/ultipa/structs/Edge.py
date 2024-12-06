# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:19
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Edge.py
from typing import Dict

from ultipa.structs.BaseModel import BaseModel


class Edge(BaseModel):
	'''
	    Data class for edge.
	'''
	_index = None
	def getUUID(self):
		return self._uuid



	def __init__(self,
				 _uuid: int = None,
				 _from: str =  '',
				 _to: str = '',
				 _from_uuid: str = '',
				 _to_uuid:str='',
				 schema: str = None,
				 values: Dict = None):

		self.schema = schema
		self._uuid = _uuid
		self._from = _from
		self._from_uuid=_from_uuid
		self._to = _to
		self._to_uuid = _to_uuid
		self.values = values

	def getFrom(self):
		return self._from

	def getTo(self):
		return self._to

	def getId(self):
		return self._id

	def getFromUUID(self):
		return self._from_uuid

	def getToUUID(self):
		return self._to_uuid

	def getValues(self):
		return self.values

	def getSchema(self):
		return self.schema

	def get(self, propertyName: str):
		return self.values.get(propertyName)

	def set(self, propertyName: str, value):
		self.values.update({propertyName: value})

	def _getIndex(self):
		return self._index