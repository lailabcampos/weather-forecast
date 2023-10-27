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
            "descricao",
        ]
        self.clima = pd.DataFrame(columns=self.COLUMNS)
        self.dias = self.dados["list"]

        for i in range(len(self.dias)):
            self.clima.loc[len(self.clima)] = {
                self.COLUMNS[0]: pd.to_datetime(self.dias[i]["dt_txt"]),
                self.COLUMNS[1]: self.dias[i]["main"]["temp"],
                self.COLUMNS[2]: self.dias[i]["main"]["humidity"],
                self.COLUMNS[3]: self.dias[i]["main"]["pressure"],
                self.COLUMNS[4]: self.dias[i]["wind"]["speed"],
                self.COLUMNS[5]: self.dias[i]["weather"][0]["description"],
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

        self.previsao = np.max(self.clima_dia["descricao"])

        relatorio = pd.DataFrame(
            {
                "Temperatura [°C]": [self.t_ymax, self.t_ymin],
                "Umidade [%]": [self.u_ymax, self.u_ymin],
                "Pressão [hPa]": [self.p_ymax, self.p_ymin],
                "Velocidade do Vento [m/s]": [self.v_ymax, self.v_ymin],
            },
            index=["Máxima", "Mínima"],
        )

        return relatorio

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

        ### TODO 3: Criar alertas com descrição ? (IMPORTANTE!)

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
                                args=[{"visible": [True, False, False, False]}],
                            ),
                            dict(
                                label="Umidade",
                                method="update",
                                args=[{"visible": [False, True, False, False]}],
                            ),
                            dict(
                                label="Pressão",
                                method="update",
                                args=[{"visible": [False, False, True, False]}],
                            ),
                            dict(
                                label="Vento",
                                method="update",
                                args=[{"visible": [False, False, False, True]}],
                            ),
                        ]
                    ),
                )
            ],
        )

        return fig
