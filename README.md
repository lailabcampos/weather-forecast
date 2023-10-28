# Projeto API Previsão do Tempo
Projeto com o objetivo de consultar a API Open Weather utilizando Python para apresentar as informações de previsão do tempo para determinada cidade, com possibilidade de geração de gráficos e alertas em caso de condições climáticas precárias.

## Arquitetura do projeto
A estrutura do projeto pode ser definida em três etapas, sendo elas:
- 1ª etapa - Requisição: Camada responsável por buscar informações de previsão do tempo da cidade desejada pelo usuário na API Open Weather. Essa etapa é construída no arquivo conexao_api.py;
- 2º etapa - Processamento: Camada que faz o tratamento dos resultados recebidos pelo OpenWeatherMap, transformando-os em informações mais legíveis, e gerando fráficos, caso requisitado pelo usuário. Essa etapa é construída no arquivo database.py
- 3ª etapa - Resposta:  Camada responsável por enviar a resposta final ao usuário, contendo informações sobre a previsão do tempo, gráficos (se forem solicitados) e alertas, caso haja algum. Essa etapa é construída no arquivo dashboard.py.

## Dependências
Para que o weather-forecast seja executado é necessário ter:
- Python
- Requests
- NumPy
- Pandas
- Plotly
- Datetime
- Streamlit

## Outros acessos ao weather-forecast
O projeto final também pode ser acessado e executado no streamlit cloud através do link https://weather-forecast-xbganh7ckeqpv8ckytdxyk.streamlit.app/