
class CompilationError(Exception):
    def __init__(self, message:str, status_code:int,sub_type: str):
        self.status_code = status_code
        self.sub_type = sub_type
        self.message = message

    def __str__(self):
        text =  f'Mensage: {self.message}\n'
        text += f'Sub Type : {self.sub_type}\n'
        text += f'Status Code: {self.status_code}\n'
        return text

