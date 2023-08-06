from erniebot.config.baseconfig import BaseConfig
from erniebot.error.customerror import CustomError
from erniebot.util.httputils import RequestBody
import aiohttp
import json
TOKEN = None
Templat='{"messages": [{"role": "user", "content": "message"}], "temperature": null, "top_p": null, "penalty_score": null, "stream": null, "user_id": null}'
class Explain(BaseConfig):
    
    def __init__(self,apikey,secretkey):
        self.apikey=apikey
        self.secretkey=secretkey

    async def getToken(self):
        global TOKEN
        tokenurl=self.TOKEN.format(apikey=self.apikey,secretkey=self.secretkey)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if TOKEN is None:
            async with aiohttp.ClientSession() as session:
                response = await session.get(tokenurl,headers=headers)
                response_data = await response.json()
                if response_data.get('error') == "invalid_client":
                    raise CustomError(9526,"Please check apikey and secretkey")
                TOKEN = response_data.get('access_token')     
        return TOKEN
    
    async def ernieBot(self,data,bot):

        token = await self.getToken()
        if bot == self.ERNIEBOT_NAME:
            ernieurl=self.ERNIEBOT.format(access_token=token)
        elif bot == self.ERNIEBOTTURBO_NAME:
            ernieurl=self.ERNIEBOTTURBO.format(access_token=token)
        else:
            raise CustomError(9627,"No model you accessed, please check the model name you passed in, currently only erniebot and erniebotturbo are supported")

        if not isinstance(data,RequestBody):
            raise CustomError(9528,"The passed parameter is incorrect,example:{}".format(Templat))
        json_data=json.dumps(data.to_dict(),ensure_ascii=False)
        print("json_data",json_data)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(ernieurl,data=json_data,headers=headers) as response:
                response_data =await response.json()
                return response_data


    
    

        



