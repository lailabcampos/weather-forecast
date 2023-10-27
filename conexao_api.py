import requests


class Conexao_API:
    def __init__(self, cidade):
        self.cidade = cidade
        self.key = "aa98651cbc2b13fb493344dbb5ae0fb1"
        self.geo = f"https://api.openweathermap.org/geo/1.0/direct?q={self.cidade}&appid={self.key}"
        self.coord = requests.get(self.geo).json()

    def iniciar(self):
        lat = round(self.coord[0]["lat"], 5)
        lon = round(self.coord[0]["lon"], 5)
        self.link = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.key}&units=metric&lang=pt_br"
        self.requisicao = requests.get(self.link)
        requisicao = self.requisicao.json()
        return requisicao
