import envconfiguration as env_config
from requests.auth import HTTPBasicAuth
import requests
import json

class CamundaAPI:
    def __init__(self):
        self.__host = env_config.ENG_REST_URL
        self.__autenticacao = HTTPBasicAuth(env_config.ENG_REST_USERNAME, env_config.ENG_REST_PASSWORD)
    
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
    
    #INICIA O PREENCHIMENTO DO FORMULÁRIO
    def completeTask(self, taskId, variables):
        print("host ",self.__host, taskId)
        url =f'{self.__host}task/{taskId}/complete'        
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=variables,headers=headers,auth=self.__autenticacao)
        
        #RETORNA O ID DA INSTÂNCIA E O CÓDIGO DE SUCESSO
        return response