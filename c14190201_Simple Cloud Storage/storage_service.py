from http import HTTPStatus
import json
from nameko.rpc import rpc
import storage_databasewrapper
import requests

class StorageService:
    name = 'storage_service'
    db = storage_databasewrapper.Database()

    @rpc
    def file_upload(self, data):
        db_response = self.database.file_upload(data)
        return db_response
    
    @rpc
    def file_download(self,data):
        file = json.loads(data)
        fetch_response = requests.get('http://localhost:8000/file/'+file['file_id']+'/access')
        
        db_response = {
            "message":"",
            "data":[],
            "status":""
        }

        if fetch_response.status_code == 200:
            fetch_file_data = fetch_response.json()
            if file['user_id'] == fetch_file_data['data']['owner']['id']:
                db_response = self.database.file_download(file['file_id'])
                return db_response
            elif file['user_id'] == fetch_file_data['data']['share_to']['id']:
                db_response = self.database.file_download(file['file_id'])
                return db_response
            else:
                db_response['status'] = HTTPStatus.FORBIDDEN
                return json.dumps(db_response)
        else:
            fetch_file_data = fetch_response.json()
            print(json.dumps(fetch_response.json()))
            db_response['status'] = fetch_response.status_code
            return json.dumps(db_response)

    @rpc
    def file_sharing(self,data):
        sharing_req = json.loads(data)
        fetch_response = requests.get('http://localhost:8000/file/'+sharing_req['file_id']+'/access')
        
        db_response = {
            "message":"",
            "data":[],
            "status":""
        }

        if fetch_response.status_code == 200:
            fetch_file_data = fetch_response.json()
            if sharing_req['user_id'] == fetch_file_data['data']['owner']['id']:
                db_response = self.database.file_sharing(sharing_req['file_id'],sharing_req['share_to'])
                return db_response
            else:
                db_response['status'] = HTTPStatus.FORBIDDEN
                return json.dumps(db_response)
        else:
            #file tidak ditemukan
            fetch_file_data = fetch_response.json()
            print(json.dumps(fetch_response.json()))
            db_response['status'] = fetch_response.status_code
            return json.dumps(db_response)

    @rpc
    def fetch_file_access(self,id_file):
        db_response = self.database.fetch_file_access(id_file)
        return db_response