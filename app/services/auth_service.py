from repositories.interfaces.auth_repository import AuthRepositoryInterface

class AuthService: 
    def __init__(self, repository:AuthRepositoryInterface) :
        self.repository = repository 

    def login_user(login_data) :
        pass 

    def create_user(user_data) :
        pass 