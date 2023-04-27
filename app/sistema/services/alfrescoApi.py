import json
import requests
from decouple import config
from ..models.alfrescoNode import AlfrescoNode
class AlfrescoAPI:
    def __init__(self):
        self.__auth_url = config("AUTH_URL")
        self.__base_url = config("ALFRESCO_BASE_URL")
        self.__username = config("ALFRESCO_USERNAME")
        self.__password = config("ALFRESCO_PASSWORD")
        self.__rootFolder = config("ALFRESCO_ROOT_FOLDER_ID")
        self.__alf_ticket = self.login() 

        self.headers = {'content-type': 'application/json'}

    def login(self):
        credentials = {
            "username": self.__username,
            "password": self.__password,
        }

        url = self.__auth_url+"/login"
        response = requests.post(url,json.dumps(credentials))
        if response.status_code == 200:
            response = json.loads(response.content)
            return response["data"]["ticket"]
        else: 
            print("Houve um erro com a requisição",response.status_code, response.content)
            return ""
    
    def createNode(self, file, type, name):
        body = {
            "filedata": open(file, "rb"),
        }

        params = {
            "name": name,
            "type": type,
        }
        url = self.__base_url+"nodes/"+self.__rootFolder+"/children?alf_ticket="+self.__alf_ticket
        response = requests.post(url, files=body, data=params)
        if response.status_code == 200 or response.status_code == 201:
            # replace this by alfrescoNode class
            return AlfrescoNode.createAlfrescoNodeFromResponse(response.content)
        else: 
            print("Houve um erro com a requisição",response.status_code, response.content)
            return ""
    
    def getNodeContent(self, path, nodeId):
        url = self.__base_url+"nodes/"+nodeId+"/content?alf_ticket="+self.__alf_ticket
        response = requests.get(url, allow_redirects=True)

        if response.status_code == 200 or response.status_code == 201:
            open(path, 'wb').write(response.content)
            return response.status_code
        else: 
            print("Houve um erro com a requisição",response.status_code, response.content)
            return ""
    
    def getNodeInfo(self, nodeId):
        url = self.__base_url+"nodes/"+nodeId+"?alf_ticket="+self.__alf_ticket
        response = requests.get(url, allow_redirects=True)

        if response.status_code == 200 or response.status_code == 201:
            return response
        else: 
            print("Houve um erro com a requisição",response.status_code, response.content)
            return ""

    def nodeChildrens(self, nodeId=""):
        url = self.__base_url+"nodes/"+self.__rootFolder+"/children?alf_ticket="+self.__alf_ticket
        response = requests.get(url)

        if response.status_code == 200 or response.status_code == 201:
            return json.loads(response.content)
        else: 
            print("Houve um erro com a requisição",response.status_code, response.content)
            return ""
    
    def createSharedLink(self, nodeId):
        params = {
            "nodeId": nodeId,
        }

        url = self.__base_url+"shared-links?alf_ticket="+self.__alf_ticket
        response = requests.post(url, json=params)

        if response.status_code == 200 or response.status_code == 201:
            return response.content
        else: 
            print("Houve um erro com a requisição",response.status_code, response.content)
            return ""
        
    def deleteNode(self, nodeId):
        url = self.__base_url+"nodes/"+nodeId+"?alf_ticket="+self.__alf_ticket
        response = requests.delete(url)

        if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
            return response
        else: 
            print("Houve um erro com a requisição",response.status_code, response.content)
            return ""
