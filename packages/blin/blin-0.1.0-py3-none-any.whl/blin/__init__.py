import requests

################################################
url = "https://blin.lemeni.cloud"
################################################
def version():
    """
    Returns blin package version

    Returns:
    str: blin package version
    """
    return "0.1.0"


class HTTPError(Exception):
    def __init__(self, response):
        super().__init__(f'HTTPError {response.status_code}: {response.reason}. Content: {response.text}' )

class Error(Exception):
    def __init__(self, what):
        super().__init__(what)

def result(response, expectedResult=None, orError=None):
    if response.status_code != 200:
        raise HTTPError(response)

    if expectedResult and response.json()['result'] != expectedResult:
        raise Error(orError)

    return response.json()['result']



def create_project(project_id, project_settings, authorizationToken):
    """
    Creates project

    Parameters:
    project_id (str)         : project identifier 
    project_settings (dict)  : project settings dict with following required fields:
         {
            'assistant_name':<name>,
            'pinecone_index_name': <index_name>,
            'keys': {
                "key1": <openapi_key>,
                "key2": <pinecone_key>
            }
         }
    authorizationToken (str) : blin auth token

    Returns:
    None
    """
    print(f'[blin] {url}/project/{project_id}')
    response = requests.post(f"{url}/project/{project_id}",
        headers={"authorizationToken": authorizationToken},
        json   ={"project_settings": project_settings})
        
    return result(response, expectedResult='Created', orError="Project with this id already exists")
    

def open_project(project_id, authorizationToken):
    """
    Opens previously created project

    Parameters:
    project_id (str)         : project identifier     
    authorizationToken (str) : blin auth token

    Returns:
    Project: Project object
    """
    return Project(project_id, authorizationToken)

def delete_project(project_id, authorizationToken):
    """
    Deletes the project

    Parameters:
    project_id (str)         : project identifier     
    authorizationToken (str) : blin auth token

    Returns:
    None
    """
    response = requests.delete(f"{url}/project/{project_id}", 
        headers={"authorizationToken": authorizationToken})

    return result(response, expectedResult='Deleted', orError="Error during project deletion")
   

class Project():
    def __init__(self, project_id, authorizationToken):
        self.project_id         = project_id
        self.authorizationToken = authorizationToken

        self.headers={ "authorizationToken": self.authorizationToken }
                     
    
    def learn(self, knowledge_id, data_string):
        """
        Adds knowledge to the project 

        Parameters:
        knowledge_id (str)  : knowledge identifier
        data_string (str)   : knowledge itself as a data string

        Returns:
        None
        """
        knowledge = {"knowledge": data_string}
        return self._call_learn(knowledge_id, knowledge) 

    def get_commands(self, user_request):     
        """
        Returns command to execute based on user request and previously learned knowledge

        Parameters:
        user_request (str)  : user request 

        Returns:
        dict: command to execute based on user request and previously learned knowledge
        """    
        response = requests.get(f"{url}/project/{self.project_id}/command",
            headers=self.headers,
            json   ={'request':user_request})
        
        return result(response)


    def get_knowledge_ids(self):
        """
        Returns a list of all knowledge IDs on which the project was learned

        Returns:
        list: knowledge IDs on which the project was learned
        """  
        response = requests.get(f"{url}/project/{self.project_id}/knowledge", headers=self.headers)

        return result(response)


    def get_knowledge(self, knowledge_id):
        """
        Returns knowledge data string  for given knowledge id

        Parameters:
        knowledge_id (str) : knowledge identifier

        Returns:
        list: knowledge IDs on which the project was learned
        """  
        response = requests.get(f"{url}/project/{self.project_id}/knowledge/{knowledge_id}", headers=self.headers)

        return result(response)
        
    def forget_knowledge(self, knowledge_id):
        """
        Deletes the knowledge

        Parameters:
        knowledge_id (str)         : knowledge identifier

        Returns:
        None
        """  
        response = requests.delete(f"{url}/project/{self.project_id}/knowledge/{knowledge_id}", headers=self.headers)
        
        return result(response, expectedResult='Deleted', orError="Error during knowledge deletion")


    def _call_learn(self, knowledge_id, knowledge):        
        response = requests.post(f"{url}/project/{self.project_id}/knowledge/{knowledge_id}",
            headers=self.headers,
            json   =knowledge)
               
        return result(response)





