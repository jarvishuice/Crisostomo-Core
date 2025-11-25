from logging import  getLogger
from Application.Helpers.Cipher.HashGeneratorHelper import HashGeneratorHelper
from Infrastructure.DAO.Users.UserDAO import UserDAO
from Infrastructure.Providers.JwtProvider import JwtProvider

class LoginUseCase:
    def __init__(self,dao:UserDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao
        self.cipherHelper = HashGeneratorHelper()
        self.jwtHelper = JwtProvider()
    async def Execute(self,username:str,password:str)->str:
       try:
        user = await self.dao.get_user_by_username(username.upper())
        if user.cod == None and user.cod == "":
            raise Exception("usuario Invalido")
        password_cipher = self.cipherHelper.generate(password)
        if password_cipher != user.password_hash:
            raise Exception("contrasena  Invalida")
        res = self.jwtHelper.create_token(str(user.cod))

        self.log.info(f"usuario ha iniciado seccion de manera correcta y se le asigno el token :{res} ")
        return res
       except Exception as e:
           self.log.error(f"hemos tenido un error en el caso de uso de login {e} ")
           raise e


