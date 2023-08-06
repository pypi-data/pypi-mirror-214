
class CommandLineError(Exception):
    def __init__(self, message:str, status_code:int):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        text = f'Mensage: {self.message}'
        text += f'Status Code: {self.status_code}'
        return text

