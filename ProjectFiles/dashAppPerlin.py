# Author: Jose Martinez-Ponce
# Date: Sat. Nov. 16
# Purpose: Dash App to incorporate everything together
from dash import Dash, html, dcc, Input, Output, callback, State, callback_context
from datetime import datetime
import plotly.express as px
import numpy as np
import base64 # needed to decode files from DASH input


from perlinMapGen import PerlinMap
from FileProcess import PerlinFile


# **IMPORTANT: MUST NEED pycollada, NetworkX, trimesh, scipy Packages in order for Export feature to work **

# I made the seeds global because otherwise the seeds wouldn't sync across
global_seed1 = None
global_seed2 = None


def update_seeds(seed1=None, seed2=None):
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


initOct1 = 20  # cannot be a non-positive num or none
initOct2 = 20
initSize = 500

# Start Time Counter
initStartTime = datetime.now()

# Init Map Generation
perlin_map = PerlinMap(size=initSize, seed1=global_seed1, seed2=global_seed2, oct1=initOct1, oct2=initOct2)
perlinMapGen, seed = perlin_map.generate_perlin()

map2D = perlin_map.display_2d()
map3D = perlin_map.display_3d()

# End Time Counter
initEndTime = datetime.now()
initTimeTaken = (initEndTime - initStartTime).total_seconds()
initMessage = f"""
    Map generated in *{initTimeTaken:.2f}* seconds.\n
    **Seed:** {seed}\n
    **Map Size:** {initSize}\n
    **Octave 1:** {initOct1}\n
    **Octave 2:** {initOct2}\n
    """

explainMessage = f"""
    **Seed**: A numerical input that initializes the random number generator used to create the Perlin noise. Allows for 
    reproducibility.\n
    **Map Size**: Specifies the dimensions of the Perlin Noise Map. The random perlin noise generator limits the map to
     500 in size. \n
    **Octave 1 and 2**: Determines how many layers of noise are combined to create the final pattern. Higher octaves 
    add finer details whereas lower octaves contribute to coarser details. \n
"""

hardwareMessage = "**Note:** If you experience lag with the 3D Map, " \
                  "turning on Hardware Acceleration for your browser removes the lag from the 3D Map. "

file_upload_message = """
### File Upload Instructions ###

To upload a file for generating a Perlin map, the file must follow the exact format below:

#### Example Format: ###
seed1: 11 \n
seed2: 21 \n
oct1: 1 \n 
oct2: 14 \n 
size: 300


- Ensure **each parameter** is listed on a separate line.
- Use only **integer values** for all parameters.
- Do not include any additional lines or content in the file.

**Note:** Files that do not use this format may result in processing errors.
"""

print("Map has been generated")
fig = px.imshow(perlinMapGen, color_continuous_scale='gray')  # assigns the perlin map
fig2 = map2D  # shows the generated perlin map into a 2D Map
fig3 = map3D  # map3D already made into figure in perlinMapGen.py, no need to do imshow
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

fig2.update_layout(
    title={
        'text': "2D Map of Perlin Noise",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    coloraxis_showscale=False
)

fig3.update_layout(
    title={
        'text': "3D Map of Perlin Noise",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    scene=dict(
        aspectratio=dict(x=1, y=1, z=0.5),  # Aspect Ratio
        camera=dict(
            eye=dict(x=0.5, y=0.5, z=1)  # How Close camera is
        )
    ),
    margin=dict(l=0, r=0, t=50, b=0,),  # Controls White Space around graph
    height=700,  # Controls Height of graph
    width=700,
)

app = Dash()

app.layout = html.Div(
    id="main-div",
    children=[
        html.Div([
            html.Label("Theme:"),
            dcc.RadioItems(
                id="theme-toggle",
                options=[
                    {"label": "Light Mode", "value": "light"},
                    {"label": "Dark Mode", "value": "dark"}
                ],
                value="light",  # Default value is light mode
                inline=True,
                style={
                    "marginLeft": "10px",
                    "display": "inline-block",
                    "fontSize": "16px"
                }
            )
        ], style={"marginBottom": "10px", "textAlign": "left"}),

        html.H1(
            children='Perlin Noise Generator',
            id="main-title",
        ),

        # Description
        html.Div(
            children=[
                html.P(
                    '''
                    Perlin noise is a type of gradient noise used in computer graphics and procedural 
                    generation to create smooth, natural-looking textures and patterns. It was developed 
                    by Ken Perlin in 1983 to improve the visual complexity of computer-generated imagery.
                    '''
                )
            ],
            style={'marginBottom': '20px'}
        ),

        # Message container
        dcc.Markdown(
            id='explain-message',
            children=explainMessage,
            style={'textAlign': 'left', 'marginBottom': '20px', 'fontSize': '16px'}
        ),

        dcc.Markdown(
            id='format-upload-message',
            children=file_upload_message,
            style={'textAlign': 'left', 'marginBottom': '20px', 'fontSize': '16px'}
        ),

        dcc.Markdown(
            id='message',
            children=initMessage,
            style={'textAlign': 'left', 'marginBottom': '20px', 'fontSize': '16px'}
        ),


        # Checkbox to enable Advanced Options
        html.Div([
            dcc.Checklist(
                options=[
                    {"label": "Show Advanced Options", "value": "show_advanced"}
                ],
                value=[],
                id="toggle-advanced",
                inline=True,
            )
        ], style={'textAlign': 'left', 'marginBottom': '20px'}),

        # Buttons for generating and exporting
        html.Div([
            html.Div([
                html.Button(
                    'Generate Random Perlin Map',
                    id='generate-random-button',
                    n_clicks=0,
                    style={'marginRight': '20px'}
                ),
                dcc.Store(id='random-trigger', data=False),
            ]),
            html.Div([
                html.Button(
                    'Export Map',
                    id='export-mesh-button',
                    n_clicks=0,
                    style={'marginRight': '20px'},
                ),
                html.Div([
                    dcc.Loading(
                        id='loading-export',
                        type="circle",
                        children=[
                            html.Div(id='export-message')
                        ]
                    )
                ]),
            ]),
            html.Div([
               html.Label("Upload Parameter File:"),
               dcc.Upload(
                   id="upload-file",
                   children=html.Div(["Drag and Drop or ", html.A("Select a File")]),
                   style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "marginBottom": "20px",
                   },
                   multiple=False  # prevent multiple uploads at the same time
               ),
                html.Div(id="upload-message")
            ])

        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'center',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),

        # Flex container for input fields and graph
        html.Div([
            html.Div(
                id='advanced-options',
                children=[
                    # Seed Input 1
                    html.Div([
                        html.Label("Seed 1:"),
                        dcc.Input(
                            id='seed-input-1',
                            type='number',
                            value=global_seed1,
                            step=1,
                            placeholder="Enter Seed 1 Value",
                            debounce=True,
                            style={'width': '150px'}
                        )
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'marginBottom': '10px'
                    }),
                    # Seed Input 2
                    html.Div([
                        html.Label("Seed 2:"),
                        dcc.Input(
                            id='seed-input-2',
                            type='number',
                            value=global_seed2,
                            step=1,
                            placeholder="Enter Seed 2 Value",
                            debounce=True,
                            style={'width': '150px'}
                        )
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'marginBottom': '10px'
                    }),
                    # Octave 1 Input
                    html.Div([
                        html.Label("Octave 1:"),
                        dcc.Input(
                            id='octave-input-1',
                            type='number',
                            value=initOct1,
                            step=1,
                            placeholder="Enter Octave 1 Value",
                            debounce=True,
                            style={'width': '150px'}
                        )
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'marginBottom': '10px'
                    }),
                    # Octave 2 Input
                    html.Div([
                        html.Label("Octave 2:"),
                        dcc.Input(
                            id='octave-input-2',
                            type='number',
                            value=initOct2,
                            step=1,
                            placeholder="Enter Octave 2 Value",
                            debounce=True,
                            style={'width': '150px'}
                        )
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'marginBottom': '10px'
                    }),
                    # Size Input
                    html.Div([
                        html.Label("Size:"),
                        dcc.Input(
                            id='size-input',
                            type='number',
                            value=initSize,
                            step=1,
                            placeholder="Enter Size",
                            debounce=True,
                            style={'width': '150px'}
                        )
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'marginBottom': '10px'
                    }),
                    # Generate Perlin Map Button
                    html.Div([
                        html.Button(
                            'Generate Perlin Map',
                            id='generate-manual-button',
                            n_clicks=0,
                            style={'marginBottom': '20px'}
                        ),
                        dcc.Store(id='manual-trigger', data=False),
                    ]),
                    html.Div([
                        html.P(
                            '''
                            Note: Maps are only displayed in square dimensions
                            ''',
                            style={'width': '150px', 'marginTop': '10px'}
                        )
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'marginBottom': '10px'
                    }),
                ]
            ),

            html.Div([
                # Graph 1: Perlin Noise
                html.Div([
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(id='Perlin-Graph', figure=fig),
                        style={'height': '400px', 'width': '400px'}
                    ),
                ], style={'textAlign': 'center', 'margin': '10px'}),

                # Graph 2: 2D Map
                html.Div([
                    dcc.Loading(
                        id="loading-2",
                        type="default",
                        children=dcc.Graph(id='2D-Perlin-Map', figure=fig2),
                        style={'height': '400px', 'width': '400px'}
                    ),
                ], style={'textAlign': 'center', 'margin': '10px'}),
            ], style={
                'display': 'flex',
                'alignItems': 'flex-start'
            }),
        ], style={
            'display': 'flex',
            'alignItems': 'flex-start',
            'justifyContent': 'center'
        }),

        # Graph 3: 3D Map (can be in separate container)
        html.Div([
            dcc.Loading(
                id="loading-3",
                type="default",
                children=dcc.Graph(id='3D-Perlin-Map', figure=map3D),
                style={'height': '800px', 'width': '80%', 'margin': '0 auto'}
            ),
        ], style={
            'display': 'flex',
            'height': '800px',
            'justifyContent': 'center',
            'alignItems': 'center'
        }),

        dcc.Markdown(
            id='hardware-message',
            children=hardwareMessage,
            style={'textAlign': 'left', 'marginBottom': '20px', 'fontSize': '16px'}
        ),

        dcc.Store(id='perlin-map-object'),
    ],
    style={'padding': '10px'}
)


# Function to help generate random params for generate button
def generate_random_params():
    seed1 = np.random.randint(1, 1000)
    seed2 = np.random.randint(1001, 2000)
    octave1 = np.random.randint(1, 20)
    octave2 = np.random.randint(1, 20)
    size = 500

    return seed1, seed2, octave1, octave2, size


# Callback for initial perlin noise
@callback(
    Output('Perlin-Graph', 'figure'),
    Output('2D-Perlin-Map', 'figure'),
    Output('3D-Perlin-Map', 'figure'),
    Output('message', 'children'),
    Output('random-trigger', 'data'),
    Output('manual-trigger', 'data'),
    Output('perlin-map-object', 'data'),
    Output("upload-message", "children"),

    [
        Input('generate-random-button', 'n_clicks'),
        Input('generate-manual-button', 'n_clicks'),
        Input("upload-file", "contents"),
    ],
    [
        # seed1, seed2, oct1, oct2, size need to be first 5 states
        State('seed-input-1', 'value',),
        State('seed-input-2', 'value'),
        State('octave-input-1', 'value'),
        State('octave-input-2', 'value'),
        State('size-input', 'value'),
        State('random-trigger', 'data'),
        State('manual-trigger', 'data'),
    ],

    prevent_initial_call=True

)
# TODO: Figure out why it takes 10 seconds to generate map, should be shorter
def update_graph(rand_n_clicks, man_n_clicks, file_contents, seed1, seed2, oct1, oct2, size, random_trigger, manual_trigger):
    # rand_n_clicks and man_n_clicks needed in order to check if button is pressed

    # Starts Timer
    start_time = datetime.now()

    upload_message = "Please Upload a File"

    # Identify which button was clicked
    ctx = callback_context
    if not ctx.triggered:
        raise ValueError("No valid trigger.")
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] # need this in order to see what actions gets done

    if triggered_id == "upload-file":
        content_type, content_string = file_contents.split(",")
        decoded = base64.b64decode(content_string).decode("utf-8")

        processor = PerlinFile(decoded)
        params = processor.read_file()

        # Extract parameters from the file
        seed1, seed2 = params["seed1"], params["seed2"]
        oct1, oct2 = params["oct1"], params["oct2"]
        size = params["size"]

        upload_message = f"Parameters extracted: {params}"

    else:
        # Handle button logic
        if triggered_id == 'generate-random-button':
            # Generate random parameters
            seed1, seed2, oct1, oct2, size = generate_random_params()
            random_trigger = True
            manual_trigger = False

        elif triggered_id == 'generate-manual-button':
            # check for manual inputs
            if None in [seed1, seed2, oct1, oct2, size]:
                raise ValueError("All fields must be filled for manual generation.")
            random_trigger = False
            manual_trigger = True

        # print(f"seed1={seed1}, seed2={seed2}, oct1={oct1}, oct2={oct2}, size={size}") # debug

    map_state = {
        'seed1': seed1,
        'seed2': seed2,
        'oct1': oct1,
        'oct2': oct2,
        'size': size,
    }

    print(f"Updated map-state: {map_state}")

    # Update the global seed vars
    seed1, seed2 = update_seeds(seed1, seed2)

    # Call the function from perlinMapgen.py
    # Creates the Perlin Noise
    updated_perlin_map = PerlinMap(size=size, seed1=seed1, seed2=seed2, oct1=oct1, oct2=oct2)
    updatedPerlinMap, gener_seed = updated_perlin_map.generate_perlin()

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

    new_fig2 = updated_perlin_map.display_2d()
    new_fig2.update_layout(
         title={
             'text': "2D Perlin Map",
             'y': 0.95,
             'x': 0.5,
             'xanchor': 'center',
             'yanchor': 'top'
         },
         coloraxis_showscale=False
     )

    new_fig3 = updated_perlin_map.display_3d()
    new_fig3.update_layout(
         title={
             'text': "3D Perlin Map",
             'y': 0.95,
             'x': 0.5,
             'xanchor': 'center',
             'yanchor': 'top'
         }
     )

    print("Map Updated!")  # Debug print statement
    end_time = datetime.now()  # End the timer
    time_taken = (end_time - start_time).total_seconds()
    print(f"Final seed used in the message: {gener_seed}")  # debug

    message = f"""
     Map generated in {time_taken:.2f} seconds.\n
     **Seed:** {gener_seed} \n
     **Map Size:** {size} \n
     **Octave 1:** {oct1} \n
     **Octave 2:** {oct2} \n
     """

    perlin_map_data = {
        'size': size,
        'seed1': seed1,
        'seed2': seed2,
        'oct1': oct1,
        'oct2': oct2,
    }

    return fig1, new_fig2, new_fig3, message, random_trigger, manual_trigger, perlin_map_data, upload_message


# Callback for Hidden Advanced Options
@callback(
    Output('advanced-options', 'style'),
    Input('toggle-advanced', 'value')
)
def toggle_advanced_options(toggle_value):
    if "show_advanced" in toggle_value:
        return{'display': 'block', 'marginBottom': '20px', 'marginLeft': '100px', 'textAlign': 'left'}
    return{'display': 'none'}


@callback(
    Output('export-message', 'children'),
    Input('export-mesh-button', 'n_clicks'),
    State('perlin-map-object', 'data'),

    prevent_initial_call=True
)
def export_mesh(export_n_clicks, perlin_map_data):
    print(f"Perlin map data received: {perlin_map_data}")
    print(f"Export button clicked: {export_n_clicks}")
    if not perlin_map_data:
        # TODO: fix this bug where on first generation it wont populate the perlin_map_data
        return "Error: No Perlin map data available for export."

    try:
        new_perlin_map = PerlinMap(
            size=perlin_map_data['size'],
            seed1=perlin_map_data['seed1'],
            seed2=perlin_map_data['seed2'],
            oct1=perlin_map_data['oct1'],
            oct2=perlin_map_data['oct2']
        )

        new_perlin_map.generate_perlin(
            size=perlin_map_data['size'],
            seed1=perlin_map_data['seed1'],
            seed2=perlin_map_data['seed2'],
            oct1=perlin_map_data['oct1'],
            oct2=perlin_map_data['oct2']
        )
        new_perlin_map.exportmesh(len_side=60)
        return "Mesh exported successfully!"
    except KeyError as e:
        return f"Error: Missing data key - {str(e)}"
    except Exception as e:
        return f"Error during export: {str(e)}"


@callback(
    Output("main-div", "style"),
    Input("theme-toggle", "value")
)
def toggle_theme(theme):
    # TODO: Fix the weird white edge while in dark mode
    if theme == "dark":
        return {
            "backgroundColor": "#1e1e1e",  # Dark background
            "color": "#ffffff",  # Light text
        }
    else:
        return {
            "backgroundColor": "#ffffff",  # Light background
            "color": "#000000",  # Dark text
        }


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # MACOS = Needed to use use_reloader=False or else webpage wont load
