from typing import Protocol

class AuthRepositoryInterface(Protocol) : 
    def create_user(data) : 
        pass 

    def login(data) :
        pass 