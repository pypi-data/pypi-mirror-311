# from ultipa.types.types import TruncateType
from ultipa.operate.base_extra import BaseExtra
from ultipa.utils import UQLMAKER, CommandList
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs import DBType

JSONSTRING_KEYS = ["graph_privileges", "system_privileges", "policies", "policy", "privilege"]
formatdata = ['graph_privileges']


class TruncateExtra(BaseExtra):
    
	'''
        Processing class that defines settings for advanced operations on graphset.
	'''

	def truncate(self, request: ULTIPA_REQUEST.Truncate,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Truncate graphset.

		Args:
			request: An object of Truncate class

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		uqlResponse=ULTIPA_RESPONSE.Response()
		command = CommandList.truncate
		requestConfig.graphName = request.graphSetName

		if request.dbType is None and request.schema is not None:
				uqlResponse.status = ULTIPA.Status(code=ULTIPA.Code.UQL_ERROR, message="To truncate schema, DbType is required in the parameters")
				return uqlResponse

		uqlMaker = UQLMAKER(command, commonParams=requestConfig)
		uqlMaker.addParam("graph", request.graphSetName)
		
		if request.dbType is not None:
			if request.dbType == DBType.DBNODE:
				if request.schema=="*" or request.schema is None:
					uqlMaker.addParam("nodes", "*")
				else:
					uqlMaker.addParam("nodes", "@" + request.schema, notQuotes=True)
			if request.dbType == DBType.DBEDGE:
				if request.schema=="*" or request.schema is None:
					uqlMaker.addParam("edges", "*")
				else:
					uqlMaker.addParam("edges", "@" + request.schema, notQuotes=True)


		return self.uqlSingle(uqlMaker)

	def compact(self, graphName: str,
				requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Compact graphshet.

		Args:
			graph: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		command = CommandList.compact
		uqlMaker = UQLMAKER(command, commonParams=requestConfig)
		uqlMaker.addParam("graph", graphName)
		return self.uqlSingle(uqlMaker)

	def mountGraph(self, graphName: str,
			  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Mount graphshet.

		Args:
			graph: The name of graphset
			
			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		commonP = []
		if graphName:
			commonP = graphName
			requestConfig.graphName = graphName
		uqlMaker = UQLMAKER(command=CommandList.mount, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commonP)
		return self.uqlSingle(uqlMaker)

	def unmountGraph(self, graphName: str,
				requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Unmount graphshet.

		Args:
			graph: The name of graphset
			
			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		commonP = []
		if graphName:
			commonP = graphName
			requestConfig.graphName = graphName
		uqlMaker = UQLMAKER(command=CommandList.unmount, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commonP)
		return self.uqlSingle(uqlMaker)
