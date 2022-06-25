from nameko.rpc import rpc
import users_databasewrapper

class UserService:
    name = 'user_service'
    database = users_databasewrapper.Database()

    @rpc
    def user_add(self, username, password):
        res = self.database.add_user(username,password)
        return res

    @rpc
    def user_login(self, username, password):
        res = self.database.login_user(username, password)
        return res