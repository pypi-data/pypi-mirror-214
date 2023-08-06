from erniebot.service import Explain
import asyncio


class Erniebot:
    def __init__(self,apikey,secretkey):
        self.apikey = apikey
        self.secretkey = secretkey
    async def main(self,message,bot):
        explain = Explain(self.apikey,self.secretkey)
        resp  = await explain.ernieBot(message,bot)
        return resp
    def chat(self,message,bot):
        result = asyncio.get_event_loop().run_until_complete(self.main(message,bot))
        return result
        
