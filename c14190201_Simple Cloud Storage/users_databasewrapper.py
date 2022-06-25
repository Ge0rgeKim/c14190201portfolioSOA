import queue
from nameko.extensions import DependencyProvider
import mysql.connector
import uuid
import hashlib
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def user_add(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        res = {
            'status':'error',
            'message':"Error data",
        }
        query = "SELECT * FROM users WHERE username='"+username+"'"
        cursor.execute(query)
        if(len(cursor.fetchall()) == 0):
            if(len(password) >= 8):
                hashing = hashlib.md5(password.encode())
                query = "INSERT INTO users (id_users,username,password) VALUES ('"+str(uuid.uuid4())+"','"+username+"','"+hashing.hexdigest()+"')"
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
                res['status'] = 'success'
                res['message'] = "Success to add user"
            else:
                res['message'] = "Password must contain 8 characters or more"
        else:
            res['message'] = "Username already exists"
        return res

    def __del__(self):
        self.connection.close()

    def user_login(self,username,password):
        cursor = self.connection.cursor(dictionary=True)
        res = {
            'status':"error",
            'message':"Something went wrong!!!",
            'data': {}
        }
        hashing = hashlib.md5(password.encode())
        query = "SELECT COUNT(id_users) AS count FROM users WHERE username='"+username+"'"
        cursor.execute(query)
        count = cursor.fetchone()['count']
        if(count == 1):
            query = "SELECT * FROM users WHERE username='"+username+"' AND password='"+hashing.hexdigest()+"'"
            cursor.execute(query)
            row = cursor.fetchone()

            if(row == None):
                res['message'] = "Wrong Password"
            else:
                res['data'] = row
                res['message'] = "Login Success"
                res['status'] = "success"
        else:
            res['message'] = "User "+username+" not found"
        
        return res



class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='simplecloudstorage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL` using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())