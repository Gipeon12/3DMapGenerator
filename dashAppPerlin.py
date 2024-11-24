# Author: Jose Martinez-Ponce
# Date: Sat. Nov. 16
# Purpose: Dash App to incorprate everything together
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import numpy as np
from perlin import generatePerlin
import pandas as pd
initialSeed = None
initialOctave = None # cannot be a non-positive num
initialX = 100
initialY = 100

# TODO: update to new Perlin Generator
perlinMapGen = generatePerlin(initialSeed, initialOctave)
print("Map has been generated")
fig = px.imshow(perlinMapGen, color_continuous_scale='gray') # assigns the perlin map
fig.update_layout(
    # Set Title of Graph
    title = {
        'text': "Binarized Sum Map",
        'y' : 0.95,
        'x' : 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    coloraxis_showscale=False # Remove gradient bar on the side, not needed
)

app = Dash()

app.layout = html.Div([
    html.H1(children='Perlin Noise Generator', style={'textAlign': 'center'}),

    # Description
    html.Div(children=[
        html.P('''
            Perlin noise is a type of gradient noise used in computer graphics and procedural 
            generation to create smooth, natural-looking textures and patterns. It was developed 
            by Ken Perlin in 1983 to improve the visual complexity of computer-generated imagery.
        ''')
    ], style={'marginBottom': '20px'}),

    # Flex container for input fields and graph
    html.Div([
        # Input Fields Container
        html.Div([
            html.Div([
                html.Label("Seed:"),
                dcc.Input(
                    id='seed-input', type='number', value=initialSeed, step=1,
                    placeholder="Enter Seed Value", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

            html.Div([
                html.Label("Octaves: (Default = 20)"),
                dcc.Input(
                    id='octave-input', type='number', value=initialOctave, step=1,
                    placeholder="Enter Octave Value", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

            html.Div([
                html.Label("X Dimension:"),
                dcc.Input(
                    id='x-size', type='number', value=initialX, step=1,
                    placeholder="Enter X Dimension", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

            html.Div([
                html.Label("Y Dimension:"),
                dcc.Input(
                    id='y-size', type='number', value=initialY, step=1,
                    placeholder="Enter Y Dimension", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

            html.Div([
                html.P(
                    '''
                    Note: X and Y Dimension should generally be equal in value
                    for square maps are preferred. 
                    ''',
                    style = {'width': '150px', 'marginTop': '10px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

        ], style={'marginRight': '20px'}),  # Space between inputs and graph


        # Graph Container
        html.Div([
            dcc.Loading(
                id="loading",
                type="default",
                children=dcc.Graph(id='Perlin-Graph', figure=fig),
                style={'height': '400px', 'width': '400px'}
            ),
        ], style={'flex': '1'})
    ], style={'display': 'flex', 'alignItems': 'flex-start'}),
], style={'padding': '20px'})


@callback(
    Output('Perlin-Graph', 'figure'),
    Input('seed-input', 'value',),
    Input('octave-input', 'value'),
    Input('x-size', 'value'),
    Input('y-size', 'value'),
)
def updateGraph(seed, noct, xDim, yDim):
    updatedPerlinMap = generatePerlin(seed, noct, xDim, yDim) # Call the function from perlin.py
    fig = px.imshow(updatedPerlinMap, color_continuous_scale='gray')
    fig.update_layout(
        # Set Title of Graph
        title={
            'text': "Binarized Sum Map",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        coloraxis_showscale=False  # Remove gradient bar on the side, not needed
    )
    #print("Map Updated!") # Debug print statement
    return fig

#updatePerlinMap(seed)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) # MACOS = Needed to use use_reloader=False or else webpage wont load


