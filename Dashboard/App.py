import sys
import os

# Ajouter le dossier parent (ou celui contenant src) au chemin Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from src.simulation import simulate_distribution  # Assure-toi que cette fonction existe


# Charger les données
df = pd.read_csv('data/cleaned_food_wastage_data.csv')
df.rename(columns={'geographical_location': 'Region'}, inplace=True)

# Créer l'application Dash
app = dash.Dash(__name__)

# Graphique initial
initial_fig = px.line(df, x='wastage_food_amount', y='quantity_of_food', title="Variation du gaspillage alimentaire")

# Layout
app.layout = html.Div([
    html.H2("Smart Food Redistribution Dashboard", style={'textAlign': 'center'}),

    # Dropdown de sélection de la région
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in df['Region'].unique()],
        value=df['Region'].unique()[0],
        style={'width': '50%', 'margin': '20px auto'}
    ),

    # Graphique dynamique
    dcc.Graph(id='wastage-graph', figure=initial_fig),

    # Bouton pour lancer la simulation
    html.Button('Lancer la simulation', id='run-simulation-button', n_clicks=0, style={'margin': '20px auto', 'display': 'block'}),

    # Zone de chargement + résultats
    dcc.Loading(
        id="loading",
        type="circle",
        children=html.Div(
            id='simulation-results',
            children="Cliquez sur le bouton pour lancer la simulation.",
            style={
                'padding': '20px',
                'border': '2px solid #ddd',
                'border-radius': '5px',
                'background-color': '#f4f4f4',
                'max-width': '600px',
                'margin': '20px auto',
                'textAlign': 'left'
            }
        )
    )
])

# Callback pour mettre à jour le graphique selon la région
@app.callback(
    Output('wastage-graph', 'figure'),
    Input('region-dropdown', 'value')
)
def update_graph(region):
    filtered_df = df[df['Region'] == region]
    fig = px.line(filtered_df, x='wastage_food_amount', y='quantity_of_food',
                  title=f"Gaspillage alimentaire - {region}")
    return fig

# Callback pour lancer la simulation
# Callback pour lancer la simulation et afficher un graphique
@app.callback(
    [Output('simulation-results', 'children'),
     Output('wastage-graph', 'figure')],  # Ajouter un graphique pour la simulation
    Input('run-simulation-button', 'n_clicks')
)
def update_simulation(n_clicks):
    if n_clicks > 0:
        try:
            # Appel de la fonction simulate_distribution
            resultats = simulate_distribution()  # Utilise la simulation avec l'algorithme par défaut
            if isinstance(resultats, dict):
                # Création d'un graphique avec les résultats
                simulation_df = pd.DataFrame(resultats)  # Supposons que 'resultats' soit un dict de données
                simulation_fig = px.bar(simulation_df, x='region', y='redistributed_food', title="Redistribution des Aliments par Région")
                # Retourner les résultats et le graphique mis à jour
                return html.Ul([html.Li(f"{k}: {v}") for k, v in resultats.items()]), simulation_fig
            return html.Pre(str(resultats)), initial_fig  # Assurez-vous de renvoyer initial_fig si nécessaire
        except Exception as e:
            return html.Pre(f"Erreur pendant la simulation : {str(e)}"), initial_fig  # Garder le graphique initial en cas d'erreur
    return "Cliquez sur le bouton pour lancer la simulation.", initial_fig

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import random

# Sample data
regions = ['North', 'South', 'East', 'West']
categories = ['Perishable', 'Canned', 'Dairy', 'Bakery']

# Inventory data
inventory_data = pd.DataFrame({
    'Region': random.choices(regions, k=100),
    'Category': random.choices(categories, k=100),
    'Quantity': [random.randint(20, 300) for _ in range(100)]
})

# Time-series redistribution efficiency
date_range = pd.date_range(start='2024-01-01', periods=30)
efficiency_data = pd.DataFrame({
    'Date': date_range,
    'Efficiency (%)': [random.uniform(60, 98) for _ in date_range]
})

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Smart Food Redistribution Dashboard', style={'textAlign': 'center'}),

    html.Div([
        html.Label('Select Region:'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': r, 'value': r} for r in regions],
            value='North',
            style={'width': '50%'}
        )
    ], style={'padding': '10px'}),

    html.Div([
        dcc.Graph(id='inventory-bar-chart')
    ]),

    html.Div([
        dcc.Graph(
            figure=px.line(efficiency_data, x='Date', y='Efficiency (%)',
                          title='Redistribution Efficiency Over Time')
        )
    ]),

    html.Div([
        html.Div([
            html.H4('Waste Reduced'),
            html.P(f"{random.randint(1000, 5000)} kg")
        ], className='card'),

        html.Div([
            html.H4('Delivery Success'),
            html.P(f"{random.randint(85, 99)}%")
        ], className='card'),

        html.Div([
            html.H4('Cost Savings'),
            html.P(f"${random.randint(10000, 50000)}")
        ], className='card'),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'})
])

@app.callback(
    Output('inventory-bar-chart', 'figure'),
    Input('region-dropdown', 'value')
)
def update_bar_chart(selected_region):
    filtered_data = inventory_data[inventory_data['Region'] == selected_region]
    fig = px.bar(filtered_data, x='Category', y='Quantity',
                 color='Category', title=f'Food Inventory in {selected_region}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
