from logging import  getLogger
from Application.Helpers.Cipher.HashGeneratorHelper import HashGeneratorHelper
from Infrastructure.DAO.Users.UserDAO import UserDAO
from Infrastructure.Providers.JwtProvider import JwtProvider
from Presentation.DTOS.Users.UserResponse import UserResponse


class GetCurrentUserUseCase:
    def __init__(self,dao:UserDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao
        self.cipherHelper = HashGeneratorHelper()
        self.jwtHelper = JwtProvider()
    async def Execute(self,token:str)->UserResponse:
       try:
        cod_user  =self.jwtHelper.decode_token(token)['sub'].replace("\"","")
        print(cod_user.replace("\"",""))
        user = await self.dao.get_user_by_cod(cod_user)
        if(user == None):
            raise Exception("NO tenemos nada en usuario ")

        res = UserResponse(cod=cod_user,full_name=user.first_name + " " + user.last_name,email=str(user.email),age=user.age,birth_date=str(user.date_of_birth),username=user.username)

        self.log.info(f"usuario ha iniciado seccion de manera correcta y se le asigno el token :{res} ")
        return res
       except Exception as e:
           self.log.error(f"hemos tenido un error en el caso de uso de login {e} ")
           raise e


