from typing import Protocol

class UserRepositoryInterface(Protocol) : 
    def create(self , user) : 
        ... 

    def get_by_id(self , id) :
        ... 

    def get_by_email(self , email) :
        ...