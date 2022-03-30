from ctypes import alignment
from flask import Flask, render_template, redirect, url_for,session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from matplotlib.pyplot import figure
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators  import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.middleware.dispatcher import DispatcherMiddleware 


from datetime import datetime as dt
import dash_daq as daq
from dash_extensions import Lottie
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


url_coonections = "https://assets3.lottiefiles.com/packages/lf20_lglwitrl.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


df = pd.read_csv("Node_2_30d.csv")
df["Time"] = pd.to_datetime(df["Time"], format="%Y-%m-%d")
df.sort_values("Time", inplace=True)


server =Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])



################################################################################################################
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "right":0,
    "width": "12rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#55b3b8",
}


SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 55,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#55b3b8",
}


# padding for the page content
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "12rem",
    "margin-right": "0rem",
    "padding": "0.6rem 0.5rem",
    "background-color": "#edf0ef",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "0.6rem 0.5rem",
    "background-color": "#edf0ef",
}

menu={

   "color":"#ffffff"

}

search_bar = dbc.Row(
    [
       dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(color="primary", className="bi bi-search ms-2",outline="True", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 ml-auto",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.Button("≡", outline=True, color="secondary", className="me-1", id="btn_sidebar")),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(html.Img(src="https://www.ispacoustics.com/wp-content/uploads/Integrate-Systems-Panel-ISP-Logo-Google.png", height="30px"),className="ms-4"),
                        dbc.Col(dbc.NavbarBrand("INFORMATION SYSTEM PROJECT", className="ms-4")),
                    ],
                    #align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),

            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
            dbc.Col(),
            dbc.Col(dbc.Badge(dbc.NavLink("LOGOUT", href="/dashboard/logout", active="exact", className="blockquote-reverse text-white"),color="#3043b7",className="border me-1",pill=True)),
        ]
    ),
    color="#55b3b8",
    dark=True,
)





sidebar = html.Div(
    [
         dbc.Row(
            [dbc.Col(Lottie(options=options, width="30", height="30", url=url_coonections),),
            dbc.Col(dbc.Button("≡", outline=True, color="Secondary", className="me-1 lead text-white", id="btn_sidebar1")),
            dbc.Row([html.H6("  Welcome User",className="text-white")]),   
            ]
        ),
        #html.Hr(className="lead text-white"),
        dbc.Row(
            [
            dbc.Col(),
            ]
        ),

        html.Hr(className="lead text-white"),
        html.Hr(className="lead text-white"),
        html.P(
            "FAULT DETECTION AND ANALYSIS", className="lead text-white"
        ),
        dbc.Nav(
            [
                
                dbc.NavLink("  Dashboard", href="/dashboard", active="exact", className="bi bi-bar-chart-line blockquote-reverse text-white"),
                dbc.NavLink("  Faults", href="/dashboard/Faults", active="exact", className="bi bi-alt blockquote-reverse text-white"),
                dbc.NavLink("  Alerts", href="/dashboard/Alerts", active="exact", className="bi bi-alarm blockquote-reverse text-white"),
                dbc.NavLink("  Reports", href="/dashboard/Reports", active="exact", className="bi bi-clipboard-data blockquote-reverse text-white"),

            ],className="menu",
            vertical=True,
            pills=True,
        ),
        html.Hr(className="lead text-white"),
        html.Hr(className="lead text-white"),
        dbc.NavLink(children=(html.I(className="bi bi-facebook ms-2" ),html.I(className="bi bi-envelope ms-4"),html.I(className="bi bi-twitter ms-4"),))
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,

)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)


#######################################################################################
my_input = dbc.Form([
    #html.H6("Select Variable"),
    dcc.Dropdown(id='my-dpdn', multi=True, value='Temperature',
                 options=[{'label':"Temperature", 'value':"Temperature"},
                          {"label":"Humidity","value":"Humidity"},
                          {"label":"CO2","value":"co2ppm"},
                          {"label":"Ethylene","value":"ethylene1"}
                          ],
                style={'backgroundColor': '#111635', 'color': '#111635'} ,        
                )
])
#########################################################################################

my_output1=dcc.Graph(id='line-fig',figure={},style={'height': '60vh'}),



##########################################################################################


app.layout = html.Div([
    dcc.Store(id='side_click'),
    dcc.Location(id="url"),
    navbar,
    sidebar,
    content
])



############################################################################################

@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [
        Input("btn_sidebar", "n_clicks"),
        Input("btn_sidebar1", "n_clicks")
    ],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n,n1, nclick):
    if n or n1:
        if nclick == "SHOW" or n1=="SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

########################################################################################

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
   
    if pathname in[ "/dashboard","/dashboard/"]:
        return [
                html.Div([
                    dbc.Row([
                                dbc.Col(dbc.Card([html.H6("TEMPERATURE", className="text-sm-center card-title text-primary"),
                                                html.H2("{:.2f}".format(df['Temperature'].iloc[-1]),className="card-title text-lg-center text-primary")],color='#ffffff',inverse=True,style={"height":"86%"})),
                                dbc.Col(dbc.Card([html.H6("HUMIDITY", className="text-sm-center card-title text-primary"),
                                                html.H2("{:.2f}".format(df['Humidity'].iloc[-1]),className="card-title text-lg-center text-primary")],color='#ffffff',inverse=True,style={"height":"86%"})),
                                dbc.Col(dbc.Card([html.H6("CO2", className="text-sm-center card-title text-primary"),
                                                html.H2("{:.2f}".format(df['co2ppm'].iloc[-1]),className="card-title text-lg-center text-primary")],color='#ffffff',inverse=True,style={"height":"86%"})),
                                dbc.Col(dbc.Card([html.H6("ETHYLENE", className="text-sm-center card-title text-primary"),
                                                html.H2("{:.2f}".format(df['ethylene1'].iloc[-1]),className="card-title text-lg-center text-primary")],color='#ffffff',inverse=True,style={"height":"86%"})),
                                    ],className="",style={"height":"14vh","padding":"0rem 0.8rem 0rem 0.8rem"},
                            ),
                                    
                      dbc.Container([dbc.Row([
                                             dbc.Col([dbc.Card([dbc.Row([my_input]),
                                                                dbc.Row([ dcc.DatePickerRange(
                                                                            id='my-date-picker-range',  # ID to be used for callback
                                                                            calendar_orientation='horizontal',  # vertical or horizontal
                                                                            day_size=39,  # size of calendar image. Default is 39
                                                                            end_date_placeholder_text="Return",  # text that appears when no end date chosen
                                                                            with_portal=False,  # if True calendar will open in a full screen overlay portal
                                                                            first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                                                                            reopen_calendar_on_clear=True,
                                                                            is_RTL=False,  # True or False for direction of calendar
                                                                            clearable=True,  # whether or not the user can clear the dropdown
                                                                            number_of_months_shown=1,  # number of months shown when calendar is open
                                                                            min_date_allowed=dt(2021, 8, 4),  # minimum date allowed on the DatePickerRange component
                                                                            max_date_allowed=dt(2021, 9, 3),  # maximum date allowed on the DatePickerRange component
                                                                            initial_visible_month=dt(2021, 8, 1),  # the month initially presented when the user opens the calendar
                                                                            start_date=dt(2021, 8, 4).date(),
                                                                            end_date=dt(2021, 9, 3).date(),
                                                                            display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
                                                                            month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                                                                            minimum_nights=2,  # minimum number of days between start and end date

                                                                            persistence=True,
                                                                            persisted_props=['start_date'],
                                                                            persistence_type='session',  # session, local, or memory. Default is 'local'

                                                                            updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
                                                                        ),]),
                                                                dbc.Row(my_output1)])],width=8),  
                                                    
                                             dbc.Col(dbc.Card(children=piechart(),outline=True,color="primary", inverse=True),width=4,
                                                    ), 
                                      ],className="h-100"),
                                    ],style={"height": "75vh"},),  
                  ])      
     ]
###################################################################################################################
    elif pathname == "/dashboard/Faults":
        return [
                dbc.Container([

                dbc.Row(
                        dbc.Col(html.H4("FAULT DETECTION",
                        className='text-center text-primary mb-4'),
                        width=12)
                        ),
                dbc.Row(
                        dbc.Col(html.P("WORK STILL IN PROGRESS PLEASE WAIT",
                        className='text-center text-primary mb-4'),
                        width=12)
                        )  # Horizontal:start,center,end,between,around

                ],fluid="True"

                        )
            ]
    elif pathname == "/dashboard/Alerts":
        return [
                dbc.Container([

                dbc.Row(
                        dbc.Col(html.H4("Alerts",
                        className='text-center text-primary mb-4'),
                        width=12)
                        ),
                dbc.Row(
                        dbc.Col(html.P("WORK STILL IN PROGRESS PLEASE WAIT",
                        className='text-center text-primary mb-4'),
                        width=12)
                        )  # Horizontal:start,center,end,between,around

                ],fluid="True"

                        )
            ]
    elif pathname == "/dashboard/Reports":
        return [
                dbc.Container([

                dbc.Row(
                        dbc.Col(html.H4("Reports",
                        className='text-center text-primary mb-4'),
                        width=12)
                        ),
                dbc.Row(
                        dbc.Col(html.P("WORK STILL IN PROGRESS PLEASE WAIT",
                        className='text-center text-primary mb-4'),
                        width=12)
                        )  # Horizontal:start,center,end,between,around

                ],fluid="True"

                        )
            ]
    elif pathname=="/dashboard/logout":
        @login_required
        def logout():
            logout_user()
        return [html.Meta(httpEquiv="refresh",content="0")]  


    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
 )


#########################################################################################


server.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(server)
db = SQLAlchemy(server)
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])



##########################################################################################



@server.route('/')
def index():
    return render_template('index.html')

@server.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@server.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@server.route('/dashboard')
@login_required
def dashboard():
    return Flask.redirect('/dash1')


@server.route('/dashboard/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



##########################################################################################
@app.callback(
    Output('line-fig', 'figure'),
    [Input('my-dpdn', 'value'),Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_graph(variable,start_date, end_date):
    dff = df.loc[(df['Time'] > start_date) & (df['Time'] <= end_date)]
    figln = px.line(dff, x='Time', y=variable)
    figln.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font_color='#050505')
    figln.update_xaxes(
    rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="Daily", step="day", stepmode="backward"),
            dict(count=7, label="Weekly", step="day", stepmode="backward"),
            dict(count=30, label="Monthly", step="day", stepmode="backward"),
            dict(count=1, label="Yearly", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
    return figln

    
def piechart():
    return[dcc.Graph(figure=go.Figure(data=[go.Pie(labels=['Fault1','Fault2','Fault3','Fault4'], values = [4500, 2500, 1053, 500])]),style={'height': '75vh'})]
   



#############################################################################################


app = DispatcherMiddleware(server, {
    '/dash1': app.server
})

if __name__ == '__main__':
    server.run(debug=True)
