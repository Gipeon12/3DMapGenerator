# Author: Jose Martinez-Ponce
# Date: Sat. Nov. 16
# Purpose: Dash App to incorprate everything together
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import numpy as np
from perlin import generatePerlin
# Function generPerlin creates the perlin Map
from perlinMapGen import generPerlin, perlin2map, disp3Dmap
import pandas as pd
initSeed1 = None
initSeed2 = None
initOct1 = 20 # cannot be a non-positive num
initOct2 = 20
initSize = 500
initialX = 100
initialY = 100

# TODO: update to new Perlin Generator
#perlinMapGen = generatePerlin(initialSeed, initialOctave)
perlinMapGen, seed = generPerlin(initSeed1, initSeed2, initOct1, initOct2, initSize)
map2D, fseed = perlin2map(perlinMapGen)
map3D = disp3Dmap(map2D, fseed)
print("Map has been generated")
fig = px.imshow(perlinMapGen, color_continuous_scale='gray') # assigns the perlin map
fig2 = px.imshow(map2D, color_continuous_scale= 'gray') # shows the generated perlin map into a 2D Map
#fig3 = px.imshow(map3D, color_continuous_scale= 'gray')
fig.update_layout(
    # Set Title of Graph
    title = {
        'text': "Perlin Noise",
        'y' : 0.95,
        'x' : 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    coloraxis_showscale=False # Remove gradient bar on the side, not needed
)

fig2.update_layout(
    title = {
        'text': "2D Map of Perlin Noise",
        'y': 0.95,
        'x': 0.5,
        'xanchor' : 'center',
        'yanchor' : 'top'
    },
    coloraxis_showscale = False
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
            # Seed Input 1
            html.Div([
                html.Label("Seed 1:"),
                dcc.Input(
                    id='seed-input-1', type='number', value=initSeed1, step=1,
                    placeholder="Enter Seed 1 Value", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),
            # Seed Input 2
            html.Div([
                html.Label("Seed 2:"),
                dcc.Input(
                    id='seed-input-2', type='number', value=initSeed2, step=1,
                    placeholder="Enter Seed 2 Value", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

            html.Div([
                html.Label("Octave 1:"),
                dcc.Input(
                    id='octave-input-1', type='number', value=initOct1, step=1,
                    placeholder="Enter Octave 1 Value", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

            html.Div([
                html.Label("Octave 2:"),
                dcc.Input(
                    id='octave-input-2', type='number', value=initOct2, step=1,
                    placeholder="Enter Octave 2 Value", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

            html.Div([
                html.Label("Size:"),
                dcc.Input(
                    id='size-input', type='number', value=initSize, step=1,
                    placeholder="Enter Size", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

            html.Div([
                html.P(
                    '''
                    Note: Maps are only displayed in square dimensions
                    ''',
                    style = {'width': '150px', 'marginTop': '10px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),

        ], style={'marginRight': '20px'}),  # Space between inputs and graph


        # Graph Container
        html.Div([
            dcc.Loading(
                id="loading-1",
                type="default",
                children=dcc.Graph(id = 'Perlin-Graph', figure = fig),
                style={'height': '400px', 'width': '400px'}
            ),
        ], style={'flex': '1'}),

        # Second Graph Container
        html.Div([
            dcc.Loading(
                id = "loading-2",
                type= "default",
                children = dcc.Graph(id = '2D-Perlin-Map', figure = fig2),
                style={'height': '400px', 'width': '400px'}
            ),
        ], style = {'flex': '2'}),

        html.Div([
            dcc.Loading(
                id = "loading-3",
                type = "default",
                children = dcc.Graph(id = '3D-Perlin-Map', figure = map3D),
                style = {'height': '400px', 'width': '400px'}
            ),
        ], style = {'flex' : '3'}),
    ], style={'display': 'flex', 'alignItems': 'flex-start'}),
], style={'padding': '20px'}),



# Callback for initial perlin noise
@callback(
    Output('Perlin-Graph', 'figure'),
    [
        Input('seed-input-1', 'value',),
        Input('seed-input-2', 'value'),
        Input('octave-input-1', 'value'),
        Input('octave-input-2', 'value'),
        Input('size-input', 'value'),
    ]

)
def updateGraph(seed1, seed2, oct1, oct2, size):
    updatedPerlinMap, seed = generPerlin(seed1, seed2, oct1, oct2, size) # Call the function from perlinMapgen.py
    fig = px.imshow(updatedPerlinMap, color_continuous_scale='gray')
    fig.update_layout(
        # Set Title of Graph
        title={
            'text': "Perlin Noise",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        coloraxis_showscale=False  # Remove gradient bar on the side, not needed
    )
    #print("Map Updated!") # Debug print statement
    return fig

# Callback for 2D Map

@callback(
    Output('2D-Perlin-Map', 'figure'),
    [
        Input('seed-input-1', 'value', ),
        Input('seed-input-2', 'value'),
        Input('octave-input-1', 'value'),
        Input('octave-input-2', 'value'),
        Input('size-input', 'value'),
    ]
)
def update2DMap(seed1, seed2, oct1, oct2, size):
    updatedPerlinMap, seed = generPerlin(seed1, seed2, oct1, oct2, size)

    map2D, fseed = perlin2map(updatedPerlinMap)
    fig2 = px.imshow(map2D, color_continuous_scale='gray')

    fig2.update_layout(
        # Set Title of Graph
        title={
            'text': "2D Perlin Map",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        coloraxis_showscale=False  # Remove gradient bar on the side
    )
    return fig2

#updatePerlinMap(seed)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) # MACOS = Needed to use use_reloader=False or else webpage wont load


