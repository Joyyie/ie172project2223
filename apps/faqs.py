import dash_bootstrap_components as dbc
from dash import html

question_style = {
        'color': '#000000',
        'font-family': 'Arial',
        'font-weight': 'bold',
        'font-size': '16px',
        'text-align':'left',
        'position': 'relative',
        'left': '50px'                     
}

answer_style = {
        'color': '#000000',
        'font-family': 'Arial',
        'font-style': 'italic',
        'font-size': '16px',
        'text-align':'left',
        'position': 'relative',
        'left': '50px'                     
}

divone_style ={
    "padding": "1em 1em",
    'background-color':'#F7EAE4'
}

divtwo_style ={
    "padding": "1em 1em",
    'background-color':'#ffffff'
}

layout = html.Div(
    [
    html.H2('Frequently Asked Questions',
        style = {
            'color': '#000000',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '40px',
            'text-align':'center',
            'position': 'center'
        }
        ),
    html.Hr(),
    html.Br(),

    html.H2('SELF-SERVICE',
        style = {
            'color': '#E18AAA',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '25px',
            'text-align':'left',
            'position': 'relative',
            'left': '50px'
        }
        ),
    html.Br(),

    html.Div(
        [
        html.P('1. Where is Clean-and-Go located?', style = question_style),
        html.P('It is located at Lt. J. Francisco St., Krus na Ligas, Diliman, Kyusi.',
        style = answer_style),
        ],
        style = divone_style
    ),

    html.Div(
        [
        html.P('2. What hours are you open?', style = question_style),
        html.P('We are open from 7AM to 10 PM on weekdays and 6 AM to 10 PM on weekends. Business hours may change during holidays.',
        style = answer_style),
        ],
        style = divtwo_style
    ),

    html.Div(
        [
        html.P('3. Do I need to bring laundry detergent?', style = question_style),
        html.P('Yes, you need to bring your own laundry detergent and/or fabric conditioner when you avail the self-service laundry.',
        style = answer_style),
        ],
        style = divone_style
    ),

    html.Div(
        [
        html.P('4. Do I need to bring coins?', style = question_style),
        html.P('No, the machines are not coin operated. You may ask for assistance from the laundry shop employees in operating the machines.',
        style = answer_style),
        ],
        style = divtwo_style
    ),

    html.Hr(),
    html.Br(),

    html.H2('DROP-OFF',
        style = {
            'color': '#E18AAA',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '25px',
            'text-align':'left',
            'position': 'relative',
            'left': '50px'
        }
        ),
    html.Br(),

    html.Div(
        [
        html.P('1. What time can I pick up my laundry?', style = question_style),
        html.P('After 2 business days, you may pick up your laundry from 1 PM to 10 PM.',
        style = answer_style),
        ],
        style = divone_style
    ),

    html.Div(
        [
        html.P('2. What kind of payment do you accept?', style = question_style),
        html.P('We accept cash and e-wallet payments.',
        style = answer_style),
        ],
        style = divtwo_style
    ),

    html.Div(
        [
        html.P('3. Will you sort whites from colors?', style = question_style),
        html.P('No. We request you to sort the clothes yourself. We will not be responsible for any instances of bleeding of clothes.',
        style = answer_style),
        ],
        style = divone_style
    ),

    html.Div(
        [
        html.P('4. What laundry detergents do you use?', style = question_style),
        html.P('We use standard detergents which we have carefully chosen to ensure the good quality of our services. You may directly reach out to us through our contact information if you would like to know the exact brands we use.',
        style = answer_style),
        ],
        style = divtwo_style
    ),

    html.Div(
        [
        html.P('5. Are your machines environmentally friendly?', style = question_style),
        html.P('Yes, all of our washers and dryers are energy efficient. They have the technology to use just the right amount of energy they need for your load.',
        style = answer_style),
        ],
        style = divone_style
    ),

    html.Hr(),  
    ]
)

    # html.Div(
    #     [dbc.Placeholder(size="xs", color = 'secondary', className="me-1 mt-1 w-100")]
    # ),  