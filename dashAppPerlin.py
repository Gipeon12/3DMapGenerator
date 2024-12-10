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


global_seed1 = None
global_seed2 = None

def updateSeeds(seed1 = None, seed2 = None):
    global global_seed1, global_seed2

    if seed1 is not None:
        global_seed1 = seed1
    if seed2 is not None:
        global_seed2 = seed2

    if global_seed1 is None:
        global_seed1 = np.random.randint(1, 1000)
    if global_seed2 is None:
        global_seed2 = np.random.randint(1001, 2000)
    return global_seed1, global_seed2

initOct1 = 20 # cannot be a non-positive num
initOct2 = 20
initSize = 500
#initialX = 100
#initialY = 100

# TODO: update to new Perlin Generator
#perlinMapGen = generatePerlin(initialSeed, initialOctave)
perlinMapGen, seed = generPerlin(global_seed1, global_seed2, initOct1, initOct2, initSize)
map2D, fseed = perlin2map(perlinMapGen)
map3D = disp3Dmap(map2D, fseed)
print("Map has been generated")
fig = px.imshow(perlinMapGen, color_continuous_scale='gray') # assigns the perlin map
fig2 = px.imshow(map2D, color_continuous_scale= 'gray') # shows the generated perlin map into a 2D Map
fig3 = map3D
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

fig3.update_layout(
    title = {
        'text': "3D Map of Perlin Noise",
        'y': 0.95,
        'x' : 0.5,
        'xanchor' : 'center',
        'yanchor' : 'top',
    },
    scene = dict(
        aspectratio = dict(x = 1, y = 1, z = 0.5), # Aspect Ratio
        camera = dict(
            eye = dict (x = 0.5, y = 0.5, z = 1) # How Close camera is
        )
    ),
    margin = dict(l = 0, r = 0, t = 50, b = 0,),# Controls White Space around graph
    height = 700 # Controls Height of graph
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
                    id='seed-input-1', type='number', value=global_seed1, step=1,
                    placeholder="Enter Seed 1 Value", debounce=True, style={'width': '150px'}
                )
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginBottom': '10px'}),
            # Seed Input 2
            html.Div([
                html.Label("Seed 2:"),
                dcc.Input(
                    id='seed-input-2', type='number', value=global_seed2, step=1,
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
        ]),

        # Second Graph Container
        html.Div([
            dcc.Loading(
                id = "loading-2",
                type= "default",
                children = dcc.Graph(id = '2D-Perlin-Map', figure = fig2),
                style={'height': '400px', 'width': '400px'}
            ),
        ]),

    ], style={'display': 'flex', 'alignItems': 'flex-start'}),

    html.Div([
        dcc.Loading(
            id = "loading-3",
            type = "default",
            children = dcc.Graph(id = '3D-Perlin-Map', figure = map3D),
            style = {'height': '800px', 'width': '80%', 'margin':'0 auto'}
        ),
    ], style={'height': '800px'}),

], style={'padding': '20px'}),



# Callback for initial perlin noise
@callback(
    Output('Perlin-Graph', 'figure'),
    Output('2D-Perlin-Map', 'figure'),
    Output('3D-Perlin-Map', 'figure'),
    [
        Input('seed-input-1', 'value',),
        Input('seed-input-2', 'value'),
        Input('octave-input-1', 'value'),
        Input('octave-input-2', 'value'),
        Input('size-input', 'value'),
    ],

    prevent_initial_call=True

)
def updateGraph(seed1, seed2, oct1, oct2, size):
    # Update the global seed vars
    seed1, seed2 = updateSeeds(seed1, seed2)

    # Call the function from perlinMapgen.py
    # Creates the Perlin Noise
    updatedPerlinMap, seed = generPerlin(seed1, seed2, oct1, oct2, size)

    # Creates Perlin Noise
    fig1 = px.imshow(updatedPerlinMap, color_continuous_scale='gray')
    fig1.update_layout(
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

    map2D, seed = perlin2map(updatedPerlinMap)
    fig2 = px.imshow(map2D, color_continuous_scale= 'gray')
    fig2.update_layout(
        title = {
            'text' : "2D Perlin Map",
            'y' : 0.95,
            'x' : 0.5,
            'xanchor' : 'center',
            'yanchor' : 'top'
        },
        coloraxis_showscale = False
    )

    fig3 = disp3Dmap(map2D, seed)
    fig3.update_layout(
        title = {
            'text' : "3D Perlin Map",
            'y' : 0.95,
            'x' : 0.5,
            'xanchor' : 'center',
            'yanchor' : 'top'
        }
    )

    #print("Map Updated!") # Debug print statement
    return fig1, fig2, fig3

#updatePerlinMap(seed)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) # MACOS = Needed to use use_reloader=False or else webpage wont load


