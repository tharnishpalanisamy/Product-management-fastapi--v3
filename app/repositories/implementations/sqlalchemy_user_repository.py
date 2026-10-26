from sqlalchemy.exc import IntegrityError
from app.exceptions import EmailAlreadyExists

class UserRepository : 
    def __init__(self , db ) : 
        self.db = db 

    async def create(self , user) : 
        try : 
            self.db.add(user) 
            await self.db.flush() 
            await self.db.commit()  
            return {
                'message' : 'User created successfully ' , 
                'user_id' : user.id
            }
        # except IntegrityError : 
        #     raise EmailAlreadyExists(f'Email already exists')  
        except Exception as error :
            raise 

    def get_by_id(self , id ) :
        pass 

    def get_by_email(self , email ) :
        pass 