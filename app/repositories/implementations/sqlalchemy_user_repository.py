from sqlalchemy.exc import IntegrityError
from app.exceptions import EmailAlreadyExists
from app.models import User
from sqlalchemy import select
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
        except Exception as error :
            raise 

    async def get_by_id(self , id ) :
        query = select(User).where(User.id == id) 
        result = await self.db.scalar(query) 
        return result

    async def get_by_email(self , email ) :
        query = select(User).where(User.email == email) 
        result = await self.db.scalar(query) 
        return result

    async def get_all(self) :
        query = select(User) 
        result = await self.db.scalars(query) 
        return result.all()  

    async def delete(self , id ) :
        try :
            query = select(User).where(
                User.id == id 
            ) 

            user = await self.db.scalar(query) 

            if user : 
                await self.db.delete(user)
                # await self.db.flush() 
                await self.db.commit() 
                return True 
            return False


        except Exception :
            await self.db.rollback() 
            raise 