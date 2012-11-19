import bottle


app_id = '409886029080423'
app_secret = '65045404878c33bac7b538f6f6dbeab9'
tokens = {}

app = bottle.Bottle()
access_token = facebook.get_app_access_token(app_id, app_secret)  

@app.route('/')
def home():
    bottle.redirect('/login')

@app.route('/login')
def login():
    args = dict(client_id=app_id, redirect_uri='http://localhost:8080/callback')
    bottle.redirect("https://graph.facebook.com/oauth/authorize?" +
                    urllib.urlencode(args))

@app.route('/callback')
def callback():
    args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=self.request.path_url)
    args['client_secret'] = app_secret
    return "hi"
