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
    args['scope'] = 'friends_likes'
    bottle.redirect("https://graph.facebook.com/oauth/authorize?" +
                    urllib.urlencode(args))

@app.route('/callback')
def callback():
    if bottle.request.query.error:
        return '''%s\n<a href="/login">Click here to retry.</a>'''%bottle.request.query.error_description

    args = dict(client_id=app_id, redirect_uri='http://localhost:8080/callback')
    args['client_secret'] = app_secret
    args['code'] = bottle.request.query.code
    response = facebook.cgi.parse_qs(urllib.urlopen(
        "https://graph.facebook.com/oauth/access_token?" +
            urllib.urlencode(args)).read())
    print response
    access_token = response["access_token"][-1]
    f = facebook.GraphAPI(access_token)
    uid = f.get_object('me')['id']
    bottle.response.set_cookie('access_token', access_token)
    bottle.redirect('/home')

@app.route('/home')
def home():
    try:
        access_token = bottle.request.get_cookie('access_token')
        f = crawl.FBGraph(access_token)
        f.run()
        return bottle.static_file('graph.png', '.') 
    except Exception as e:
        return e.message

@app.route('/logout')
def logout():
    bottle.response.delete_cookie('access_token') 

@app.route('/loading')
def loading():
    return 'Loading...'

if __name__ == '__main__':
    ip = bottle.request.environ.get('REMOTE_ADDR')
    app.run(host = 'localhost', port = '8080', debug = True)
