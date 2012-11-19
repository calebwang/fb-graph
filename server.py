import bottle
import urllib
import facebook
import crawl


app_id = '409886029080423'
app_secret = '65045404878c33bac7b538f6f6dbeab9'
tokens = {}

app = bottle.Bottle()
app_access_token = facebook.get_app_access_token(app_id, app_secret)  

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
    args = dict(client_id=app_id, redirect_uri='http://localhost:8080/callback')
    args['client_secret'] = app_secret
    args['code'] = bottle.request.query.code
    response = facebook.cgi.parse_qs(urllib.urlopen(
        "https://graph.facebook.com/oauth/access_token?" +
            urllib.urlencode(args)).read())
    print response
    access_token = response["access_token"][-1]
    bottle.response.set_cookie('access_token', access_token)
    bottle.redirect('/home')

@app.route('/home')
def home():
    access_token = bottle.request.get_cookie('access_token')
    f = crawl.FBGraph(access_token)
    f.run()
    return bottle.static_file('graph.png') 

if __name__ == '__main__':
    app.run(host = 'localhost', port = '8080', debug = True)
