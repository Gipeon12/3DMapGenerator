# Author: Jose Martinez-Ponce
# Date: Sat. Nov. 16
# Purpose: Dash App to incorprate everything together
from dash import Dash, html, dcc, Input, Output, callback, State
from datetime import datetime
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

initOct1 = 20 # cannot be a non-positive num or none
initOct2 = 20
initSize = 500

# Start Time Counter
initStartTime = datetime.now()

# Init Map Generation
perlinMapGen, seed = generPerlin(global_seed1, global_seed2, initOct1, initOct2, initSize)
map2D, fseed = perlin2map(perlinMapGen)
map3D = disp3Dmap(map2D, fseed)

# End Time Counter
initEndTime = datetime.now()
initTimeTaken = (initEndTime - initStartTime).total_seconds()
initMessage = f"""
    Map generated with in {initTimeTaken:.2f} seconds.\n
    **Seed:** {seed}\n
    **Map Size:** {initSize}\n
    **Octave 1:** {initOct1}\n
    **Octave 2:** {initOct2}\n
    """

print("Map has been generated")
fig = px.imshow(perlinMapGen, color_continuous_scale='gray') # assigns the perlin map
fig2 = px.imshow(map2D, color_continuous_scale= 'gray') # shows the generated perlin map into a 2D Map
fig3 = map3D # map3D already made into figure in perlinMapGen.py, no need to do imshow
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
    margin = dict(l = 0, r = 0, t = 50, b = 0,), # Controls White Space around graph
    height = 700, # Controls Height of graph
    width = 700,
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

    # Message container
    dcc.Markdown(
        id = 'message',
        children = initMessage,
        style = {'textAlign': 'left', 'marginBottom': '20px', 'fontSize': '16px'}
    ),

    # Checkbox to enable Advanced Options
    html.Div([
        dcc.Checklist(
            options = [
                {"label": "Show Advanced Options", "value": "show_advanced"}
            ],
            value = [],
            id = "toggle-advanced",
            inline = True,
        )
    ], style = {'textAlign': 'left', 'marginBottom': '20px'}),

    # Generate Random Perlin Map Container
    html.Div([
        html.Button('Generate Random Perlin Map',
                    id = 'generate-button',
                    n_clicks = 0,
                    style = {'marginBottom' : '20px'}),
        dcc.Store(id = 'random-trigger', data = False),
    ], style = {'textAlign' : 'center '}),

    # Flex container for input fields and graph
    html.Div([
        # Input Fields Container
        html.Div(
            id = 'advanced-options',
            children = [
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
    ], style={'display': 'flex', 'height': '800px','justifyContent': 'center', 'alignItems' : 'center'}),

], style={'padding': '20px'}),


# Function to help generate random params for generate button
def generateRandomParams():
    seed1 = np.random.randint(1,1000)
    seed2 = np.random.randint(1001, 2000)
    octave1 = np.random.randint(1,20)
    octave2 = np.random.randint(1,20)
    size = np.random.randint(100,700)

    return seed1, seed2, octave1, octave2, size


# Callback for initial perlin noise
@callback(
    Output('Perlin-Graph', 'figure'),
    Output('2D-Perlin-Map', 'figure'),
    Output('3D-Perlin-Map', 'figure'),
    Output('message', 'children'),
    Output('random-trigger', 'data'),
    [
        Input('generate-button', 'n_clicks'),
        Input('seed-input-1', 'value',),
        Input('seed-input-2', 'value'),
        Input('octave-input-1', 'value'),
        Input('octave-input-2', 'value'),
        Input('size-input', 'value'),
    ],

    State('random-trigger', 'data'),
    prevent_initial_call=True

)
def updateGraph(n_clicks, seed1, seed2, oct1, oct2, size, randomTrigger):
    # Starts Timer
    startTime = datetime.now()

    if n_clicks and not randomTrigger:
        seed1, seed2, oct1, oct2, size = generateRandomParams()
        #print(f"n_clicks: {n_clicks}") # debug
        randomTrigger = True
    else:
        randomTrigger = False

    # Update the global seed vars
    seed1, seed2 = updateSeeds(seed1, seed2)

    # Call the function from perlinMapgen.py
    # Creates the Perlin Noise
    updatedPerlinMap, generSeed = generPerlin(seed1, seed2, oct1, oct2, size)

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

    map2D, finalSeed = perlin2map(updatedPerlinMap)
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
    endTime = datetime.now()  # End the timer
    timeTaken = (endTime - startTime).total_seconds()
    print(f"Final seed used in the message: {generSeed}") # debug

    message = f"""
    Map generated with in {timeTaken:.2f} seconds.\n
    **Seed:** {generSeed} \n
    **Map Size:** {size} \n
    **Octave 1:** {oct1} \n
    **Octave 2:** {oct2} \n
    """

    return fig1, fig2, fig3, message, randomTrigger

@callback(
    Output('advanced-options', 'style'),
    Input('toggle-advanced', 'value')
)
def toggleAdvancedOptions(toggle_value):
    if "show_advanced" in toggle_value:
        return{'display': 'block', 'marginBottom': '20px', 'textAlign': 'left'}
    return{'display': 'none'}

#updatePerlinMap(seed)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) # MACOS = Needed to use use_reloader=False or else webpage wont load


