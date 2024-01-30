# -*- coding: utf-8 -*-
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import dash
import base64
import pandas as pd
import pickle
import requests
import smtplib
import ssl
import time
from email.message import EmailMessage


def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


def sendMail(receiverAddress, subject, body):
    try:
        # Define email sender and receiver
        email_sender = 'cwakhusama@gmail.com'
        email_password = 'eaqz wixf plnz nxzr'
        email_receiver = receiverAddress

        # Set the subject and body of the email
        subject = subject
        body = body

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # # Add the attachment
        # with open(attachment_path, 'rb') as f:
        #     file_data = f.read()
        #     file_name = f.name
        # em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)

        return "email sent successfully"

    except:

        return "Please check your Username or Password"


def send_sms(phonenumber: int, sms: str):
    url = 'https://mysms.celcomafrica.com/api/services/sendsms/'

    data = {'partnerID': '435',
            'apikey': '1c37d5b44c805abf79800477e8af91d9',
            'mobile': phonenumber,
            'message': sms,
            'shortcode': 'OSL',
            'pass_type': 'plain'}

    response = requests.post(url=url, json=data)
    return response


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title='Rhys')

server = app.server


app.layout = dbc.Container([
    dbc.Row([
        html.Div([html.P(['Importer Quotation Checker!'], id='import',
                         style={'marginBottom': 10, 'marginTop': 10, 'font-family': 'cursive',
                                'text-align': 'center', 'color': '#00FFFF',
                                'fontSize': 20})]),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Label('Product'),
                    dcc.Dropdown(['metal', 'oil', 'gas', 'maize', 'wheat'
                                  ], multi=False, placeholder='Product', id='product', clearable=True,
                                 optionHeight=50),
                ], style={'marginBottom': 10, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dbc.FormText('Please enter product', style={'marginBottom': 10, 'marginTop': 5}),
                html.Div([
                    dbc.Label('Quote'),
                    dcc.Dropdown([1000, 2000, 2500, 3000, 4500, 4000, 5000, 6000, 0
                                  ], multi=False, placeholder='Quote', id='quote', clearable=True, optionHeight=50)
                ], style={'marginBottom': 10, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dbc.FormText('Please enter quote'),
                html.Div(id="alert"),
                html.Div([
                    dbc.Label('Enter Mail',
                              style={'color': 'Green', 'marginBottom': 10, 'marginTop': 10, 'fontSize': 14}),
                    dcc.Input(placeholder='Mail', id='mail',
                              style={'marginBottom': 10, 'marginTop': 5, 'width': '100%', 'height': '36px',
                                     'color': 'Green', 'borderRadius': '4px',
                                     'border': '1px solid rgba(0, 0, 0, 0.5)', 'paddingLeft': '10px',
                                     'fontSize': 14})
                ]),
                dbc.FormText('Please enter mail'),
                html.Div([
                    dbc.Label('Enter Telephone No:'),
                    dcc.Input(placeholder='Tel', id='tel',
                              style={'marginBottom': 10, 'marginTop': 5, 'width': '100%', 'height': '36px',
                                     'color': 'Green', 'borderRadius': '4px',
                                     'border': '1px solid rgba(0, 0, 0, 0.5)', 'paddingLeft': '10px',
                                     'fontSize': 14})
                ], style={'marginBottom': 5, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dbc.FormText('Please TelNo.'),
                html.Br(),
                html.Br(),
                dbc.Button('Submit quote', id='submitTextarea', n_clicks=1)
            ], style={'width': '100%', 'height': 200, 'marginBottom': 15,
                      'marginTop': 15, 'color': '#00FFFF',
                      'font-family': 'cursive', 'fontSize': 14}),

            dbc.Col([
                dbc.Label('Model Response',
                          style={'marginBottom': 15, 'color': '#800040', 'marginTop': 15, 'fontSize': 16}),
                html.Div(id='parsed',
                         style={'marginBottom': 15, 'color': '#080040', 'marginTop': 15, 'fontSize': 14}),
                html.Br(),
                html.Br(),
                dbc.Label('Email is sent to Importer and Customs',
                          style={'marginBottom': 15, 'color': '#800040', 'marginTop': 15, 'fontSize': 16}),
                html.Div(id='payload',
                         style={'marginBottom': 15, 'color': '#080040', 'marginTop': 15, 'fontSize': 14}),
                html.Br(),
            ], style={'width': '100%', 'height': 200, 'marginBottom': 15,
                      'marginTop': 15, 'color': '#00FFFF', 'text-align': 'center',
                      'font-family': 'cursive', 'fontSize': 14})
        ]),
    ])
], style={'backgroundColor': 'F0E68C', 'marginTop': '20px', 'font-family': 'cursive', 'marginBottom': '40px',
          'border': '2px', 'color': 'cyan'})


@app.callback(Output('alert', 'children'),
              Output('parsed', 'children'),
              Output('payload', 'children'),
              Input('quote', 'value'),
              Input('product', 'value'),
              Input('mail', 'value'),
              Input('tel', 'value'),
              Input('submitTextarea', 'n_clicks'), prevent_initial_call=True)
def update_output(quote, product, mail, tel, n_clicks):
    if n_clicks == 2:

        if mail and tel:

            test = {'quote': quote, 'product': product}

            new_df = pd.DataFrame(test, index=[8])

            amp = pd.get_dummies(new_df)

            amp = amp.to_dict()

            sch = {'quote': {8: 0},
                   'product_gas': {8: 0},
                   'product_maize': {8: 0},
                   'product_metal': {8: 0},
                   'product_oil': {8: 0},
                   'product_wheat': {8: 0}}

            test_df = {**sch, **amp}

            pred = pd.DataFrame(test_df, index=[8])

            with open('predicktor.pkl', 'rb') as f:
                predictor_load = pickle.load(f)

            parsed = predictor_load.predict(pred)[0]

            if parsed == 1:
                parsed = "Accepted"
                receiverAddress = mail
                subject = "Quotation Accepted!"
                body = "Congratulations! Your quotation for this product is under review!"
                send_sms(tel, body)
                sendMail(receiverAddress, subject, body)
                reject = "your quote for this project is accepted"

            else:
                parsed = "Rejected"
                receiverAddress = mail
                subject = "Quotation Rejected!"
                body = "Please review the amount quoted for this product and re-submit!"
                send_sms(tel, body)
                sendMail(receiverAddress, subject, body)
                reject = "your quote for this project is rejected"

            payload = f"Your quote for this product is {parsed}"

            alert = html.Div([html.Br(),
                              html.Hr(),
                              dbc.Alert(id="toss", children=reject, color="primary"),
                              html.Hr(),
                              html.Br()])

            time.sleep(5)

            return alert, parsed, payload,

        else:
            return dash.no_update
    else:
        return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True, port=5050, host="192.168.11.108")
