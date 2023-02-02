import envconfiguration as env_config
from requests.auth import HTTPBasicAuth
import requests
import json

class CamundaAPI:
    def __init__(self):
        self.__host = env_config.ENG_REST_URL
        self.__autenticacao = HTTPBasicAuth(env_config.ENG_REST_USERNAME, env_config.ENG_REST_PASSWORD)

    def camundaVariableFormat(self, variableName, variableValue, variableType):
        return { variableName: {
            "value": variableValue,
            "type": variableType,
            "name": variableName
        }}

    def startProcess(self, processName, dados):
        url = f'{self.__host}/process-definition/key/{processName}/start'
        requisicao = requests.post(url,json=dados,auth=self.__autenticacao)
        retorno = requisicao.text
        json_object = json.loads(retorno)
        
        return json_object
    
    def getBinaryVariable(self, processId, variableName):
        url = f'{self.__host}process-instance/{processId}/variables/{variableName}/data'
        requisicao = requests.get(url,auth=self.__autenticacao)
        
        return requisicao
    
    def getTasks(self, instanceId):
        payload = {
            "processInstanceId": instanceId,
        }
        resposta = requests.post(self.__host+"/task", json=payload, auth=self.__autenticacao)
        return resposta

    def completeTask(self, taskId, variables):
        resposta = requests.post(self.__host+"/task/"+taskId+"/complete", json=variables, auth=self.__autenticacao)
        return resposta