from http import HTTPStatus
import json
from itsdangerous import base64_decode, base64_encode
from nameko.extensions import DependencyProvider
import mysql.connector
import uuid
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection
    
    def file_upload(self, data):
        dataUpload = json.loads(data)
        cursor = self.connection.cursor(prepared=True)
        query = """
                INSERT INTO files (id_file,owner_file,file_name,mime_type,Base64Content) 
                VALUES (%s,%s,%s,%s,%s)
                """
        cursor.execute(query,(str(uuid.uuid4()),dataUpload['user_id'],dataUpload['filename'],dataUpload['mimetype'],dataUpload['base64Content']))
        self.connection.commit()
        cursor.close()

    def file_sharing(self,id_file, share_to):
        print(id_file)
        print(share_to)
        cursor = self.connection.cursor(prepared=True)
        query = """
            UPDATE files
            SET sharing=%s
            WHERE id_file=%s"""
        cursor.execute(query,(share_to, id_file, ))
        row = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        
    def file_download(self,id_file):
        cursor = self.connection.cursor(prepared=True)
        query = "SELECT file_name,mime_type,Base64Content from files WHERE id_file=%s"
        cursor.execute(query,(id_file, ))
        row = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        
        datafile = {
            'file_name': row[0],
            'mime_type':row[1],
            'base64Content':row[2]
        }

    def fetch_file_access(self,id_file):
        cursor = self.connection.cursor(prepared=True)
        query = """
        SELECT u.name,f.owner,f.sharing, 
            (SELECT name FROM users WHERE id_file = f.sharing) 
        FROM files f 
        JOIN users u 
        ON f.owner=u.id_file 
        WHERE f.id_file=%s"""
        cursor.execute(query,(id_file, ))
        row = cursor.fetchone()
        self.connection.commit()
        cursor.close()

        data = {
            'owner':{
                'id':row[1],
                'name':row[0]
            },
            'share_to':{
                'id':row[2],
                'name':row[3]
            }
        }

    def __del__(self):
        self.connection.close()



class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="database_pool",
            pool_size=5,
            pool_reset_session=True,
            host='localhost',
            database='simplecloudstorage',
            user='root',
            password=''
        )
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())