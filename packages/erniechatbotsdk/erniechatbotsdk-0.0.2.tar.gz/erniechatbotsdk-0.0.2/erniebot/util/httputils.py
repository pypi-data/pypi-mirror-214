from erniebot.error.customerror import CustomError
class Message:
    def __init__(self,role,content):
        self.role = role
        self.content = content
    def validate(self):
        if self.role != "user" or self.role != "assistant":
            raise CustomError(9528,"role can only be user or assistant")
        if len(self.content) == 0:
            raise CustomError(9528,"The dialog content cannot be empty")
    def to_dict(self):
        return {"role": self.role,"content":self.content}

        
class RequestBody:
    def __init__(self,messages,temperature=None,top_p=None,penalty_score=None,stream=None,user_id=None):
        self.messages=messages
        self.temperature = temperature
        self.top_p=top_p
        self.penalty_score=penalty_score
        self.stream=stream
        self.user_id=user_id
    def validate(self):
        if not isinstance(self.messages,list) or len(self.messages)==0:
            raise CustomError(9528,"messages requires a list and cannot be empty")
        if not self.temperature:
            self.temperature = float(self.temperature)
            if self.temperature <= 0 or self.temperature >1.0:
                raise CustomError(9528,"temperature can only be >0 temperature <=1.0")
        if not self.top_p:
            self.top_p = float(self.top_p)
            if self.top_p < 0 or self.top_p >1.0:
                raise CustomError(9528,"top_p can only be >=0 top_p <=1.0")
        if not self.penalty_score:
            self.penalty_score = float(self.penalty_score)
            if self.penalty_score < 1.0 or self.penalty_score >2.0:
                raise CustomError(9528,"penalty_score can only be >=1.0 penalty_score <=2.0")
    def to_dict(self):
        return {
            "messages": [message.to_dict() for message in self.messages],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "penalty_score": self.penalty_score,
            "stream": self.stream,
            "user_id": self.user_id
        }

class Usage:
    def __init__(self,prompt_tokens,completion_tokens,total_tokens):
        self.prompt_tokens=prompt_tokens
        self.completion_tokens=completion_tokens
        self.total_tokens=total_tokens

class ResponseBody:
    def __init__(self,object,created,sentence_id,is_end,result,need_clear_history,usage):
        self.object=object
        self.created=created
        self.sentence_id=sentence_id
        self.is_end=is_end
        self.result=result
        self.need_clear_history=need_clear_history
        self.usage=usage


