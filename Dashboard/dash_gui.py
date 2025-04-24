import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import random
from flask import Flask

# Charger la base de données CSV
food_data = pd.read_csv("data/cleaned_food_wastage_data.csv")

# Initialiser l'app Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname="/dash/", external_stylesheets=external_stylesheets)

# Simuler les données dynamiques du modèle Mesa
# (à connecter plus tard aux vraies métriques en temps réel)
def get_simulation_metrics():
    return {
        "tick": random.randint(0, 100),
        "successful_deliveries": random.randint(20, 80),
        "failures": random.randint(0, 10),
        "delivered_food_types": food_data['type_of_food'].sample(50, replace=True).value_counts().to_dict(),
        "regional_shortages": food_data['geographical_location'].sample(100, replace=True).value_counts().to_dict()
    }

# Layout de l'interface Dash
app.layout = html.Div([
    html.H1("📦 Suivi de la Livraison Alimentaire - Dashboard"),

    dcc.Tabs(id="tabs", value='tab-metrics', children=[
        dcc.Tab(label='📊 Métriques Optimisation', value='tab-metrics'),
        dcc.Tab(label='📜 Logs Agents', value='tab-logs'),
        dcc.Tab(label='🔮 Prédictions', value='tab-predictions'),
    ]),

    html.Div(id='tabs-content')
])

# Callbacks des tabs
@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    metrics = get_simulation_metrics()

    if tab == 'tab-metrics':
        line_chart = px.line(x=list(range(metrics['tick'])),
                             y=[random.randint(20, 80) for _ in range(metrics['tick'])],
                             labels={'x': 'Tick', 'y': 'Livraisons'},
                             title='Volume des livraisons au fil du temps')

        pie_chart = px.pie(values=list(metrics['delivered_food_types'].values()),
                           names=list(metrics['delivered_food_types'].keys()),
                           title='Types de nourriture livrés')

        heatmap = px.density_heatmap(
            x=list(metrics['regional_shortages'].keys()),
            y=["Zone"] * len(metrics['regional_shortages']),
            z=list(metrics['regional_shortages'].values()),
            title="Pénuries régionales (zones à forte demande)",
            labels={"x": "Région", "z": "Niveau de pénurie"})

        return html.Div([
            dcc.Graph(figure=line_chart),
            dcc.Graph(figure=pie_chart),
            dcc.Graph(figure=heatmap)
        ])

    elif tab == 'tab-logs':
        # Exemple simulé de logs agent (à lier au backend réel)
        logs = [f"Tick {i} - Agent {random.randint(0,10)} a livré 1 unité." for i in range(10)]
        return html.Ul([html.Li(log) for log in logs])

    elif tab == 'tab-predictions':
        pred_chart = px.line(x=list(range(30)),
                             y=[random.randint(50, 100) for _ in range(30)],
                             labels={'x': 'Temps futur', 'y': 'Livraisons prévues'},
                             title='Prévision des livraisons')
        return dcc.Graph(figure=pred_chart)

if __name__ == '__main__':
    app.run(debug=True, port=8051)
