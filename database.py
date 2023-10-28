# streamlit run dashboard.py

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime


class Database:
    def __init__(self, data, dados):
        self.data = datetime(data.year, data.month, data.day)
        self.dados = dados.iniciar()

    def database(self):
        # Criando dataframe dos dados de previsão
        self.COLUMNS = [
            "timestamp",
            "temp_media",
            "umidade",
            "pressao",
            "vel_vento",
            "precipitacao",
            "descricao",
        ]
        self.clima = pd.DataFrame(columns=self.COLUMNS)
        self.dias = self.dados["list"]

        for i in range(len(self.dias)):
            # Identificando se houve precipitação ou não
            self.precipitacao = float()
            if "rain" in self.dias[i]:
                self.precipitacao = self.dias[i]["rain"]["3h"]
            else:
                self.precipitacao = 0

            self.clima.loc[len(self.clima)] = {
                self.COLUMNS[0]: pd.to_datetime(self.dias[i]["dt_txt"]),
                self.COLUMNS[1]: self.dias[i]["main"]["temp"],
                self.COLUMNS[2]: self.dias[i]["main"]["humidity"],
                self.COLUMNS[3]: self.dias[i]["main"]["pressure"],
                self.COLUMNS[4]: self.dias[i]["wind"]["speed"],
                self.COLUMNS[5]: self.precipitacao,
                self.COLUMNS[6]: self.dias[i]["weather"][0]["description"]
            }

        # Selecionando dados para o dia escolhido
        self.str_data = (
            str(self.data.day) + "-" + str(self.data.month) + "-" + str(self.data.year)
        )

        self.clima_dia = self.clima[
            self.clima["timestamp"].apply(lambda row: row.day == self.data.day)
        ]

        # Relatório do tempo
        self.t_ymax = np.max(self.clima_dia["temp_media"])
        self.t_ymin = np.min(self.clima_dia["temp_media"])

        self.u_ymax = np.max(self.clima_dia["umidade"])
        self.u_ymin = np.min(self.clima_dia["umidade"])

        self.p_ymax = np.max(self.clima_dia["pressao"])
        self.p_ymin = np.min(self.clima_dia["pressao"])

        self.v_ymax = np.max(self.clima_dia["vel_vento"])
        self.v_ymin = np.min(self.clima_dia["vel_vento"])

        self.c_ymax = np.max(self.clima_dia['precipitacao'])
        self.c_ymin = np.min(self.clima_dia['precipitacao'])

        self.previsao = np.max(self.clima_dia["descricao"])

        relatorio = pd.DataFrame(
            {
                "Temperatura [°C]": [self.t_ymax, self.t_ymin],
                "Umidade [%]": [self.u_ymax, self.u_ymin],
                "Pressão [hPa]": [self.p_ymax, self.p_ymin],
                "Velocidade do Vento [m/s]": [self.v_ymax, self.v_ymin],
                "Precipitação [mm]": [self.c_ymax, self.c_ymin]
            },
            index=["Máxima", "Mínima"],
        )

        # Criando alertas
        self.c_soma = np.sum(self.clima_dia['precipitacao'])
        self.v_max_km = self.v_ymax * 3.6
        alerta = None

        alertas = [
            {
                "grau": "perigo potencial",
                "definicao": "Chuva entre 20 e 30 mm/h ou até 50 mm/dia, ventos intensos (40-60 km/h), e queda de granizo.\n",
                "riscos": "Baixo risco de corte de energia elétrica, estragos em plantações, queda de galhos de árvores e de alagamentos.\n",
                "instrucoes": f'''- Em caso de rajadas de vento: não se abrigue debaixo de árvores, pois há leve risco de queda e descargas elétricas,
                e não estacione veículos próximos a torres de transmissão e placas de propaganda).\n'''
                f"- Evite usar aparelhos eletrônicos ligados à tomada."
            },

            {
                "grau": "perigo",
                "definicao": "Chuva entre 30 e 60 mm/h ou 50 e 100 mm/dia, ventos intensos (60-100 km/h), e queda de granizo.\n",
                "riscos": "Risco de corte de energia elétrica, estragos em plantações, queda de árvores e de alagamentos.\n",
                "instrucoes": f'''- Em caso de rajadas de vento: não se abrigue debaixo de árvores, pois há risco de queda e descargas,
                elétricas e não estacione veículos próximos a torres de transmissão e placas de propaganda.\n'''
                f"- Se possível, desligue aparelhos elétricos e quadro geral de energia."
            },
        
            {
                "grau": "grande perigo",
                "definicao": "Chuva superior a 60 mm/h ou maior que 100 mm/dia, ventos superiores a 100 km/h, e queda de granizo.\n",
                "riscos": '''Grande risco de danos em edificações, corte de energia elétrica, estragos em plantações, queda,
                de árvores, alagamentos e transtornos no transporte rodoviário.\n''',
                "instrucoes": f"- Desligue aparelhos elétricos e quadro geral de energia.\n"
                f"- Em caso de enxurrada, ou similar, coloque documentos e objetos de valor em sacos plásticos.\n"
                f"- Em caso de situação de grande perigo confirmada: Procure abrigo, evite permanecer ao ar livre."
            }]
        
        if 25 <= self.c_soma <= 50 or 40 <= self.v_max_km <= 60:
            alerta = alertas[0]
        elif 50 <= self.c_soma <= 100 or 60 <= self.v_max_km <= 100:
            alerta = alertas[1]
        elif 100 <= self.c_soma or 100 <= self.v_max_km:
            alerta = alertas[2]
        else:
            pass

        return relatorio, alerta      

    def graficos(self):
        # Criando figura
        fig = go.Figure()

        # Plotando os gráficos
        fig.add_trace(
            go.Scatter(
                x=list(self.clima_dia["timestamp"]),
                y=list(self.clima_dia["temp_media"]),
                name="Temperatura",
                visible=True,
                line=dict(color="#33CFA5"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=list(self.clima_dia["timestamp"]),
                y=list(self.clima_dia["umidade"]),
                name="Umidade",
                visible=False,
                line=dict(color="#F06A6A"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=list(self.clima_dia["timestamp"]),
                y=list(self.clima_dia["pressao"]),
                name="Pressão",
                visible=False,
                line=dict(color="#1260CC"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=list(self.clima_dia["timestamp"]),
                y=list(self.clima_dia["vel_vento"]),
                name="Vento",
                visible=False,
                line=dict(color="#993399"),
            )
        )

        fig.add_trace(
            go.Bar(
                x=list(self.clima_dia["timestamp"]),
                y=list(self.clima_dia["precipitacao"]),
                name="Precipitação",
                visible=False
            )
        )

        # Botões para cada gráfico

        fig.update_layout(
            title_text="Gráfico Previsão do Tempo " + self.str_data,
            xaxis_domain=[0.05, 1.0],
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    active=0,
                    x=1.0,
                    y=1.2,
                    buttons=list(
                        [
                            dict(
                                label="Temperatura",
                                method="update",
                                args=[{"visible": [True, False, False, False, False]}],
                            ),
                            dict(
                                label="Umidade",
                                method="update",
                                args=[{"visible": [False, True, False, False, False]}],
                            ),
                            dict(
                                label="Pressão",
                                method="update",
                                args=[{"visible": [False, False, True, False, False]}],
                            ),
                            dict(
                                label="Vento",
                                method="update",
                                args=[{"visible": [False, False, False, True, False]}],
                            ),
                            dict(
                                label="Precipitação",
                                method="update",
                                args=[{"visible": [False, False, False, False, True]}],
                            ),
                        ]
                    ),
                )
            ],
        )

        return fig
