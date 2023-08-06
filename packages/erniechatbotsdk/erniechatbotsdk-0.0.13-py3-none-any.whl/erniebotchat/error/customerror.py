class CustomError(Exception):
    def __str__(self,error_code,message):
        super().__init__(message)
        self.error_code = error_code
    
