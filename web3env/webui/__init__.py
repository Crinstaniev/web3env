from flask import Flask, redirect

def create_app():
    app = Flask(__name__)
    
    from .consensus import consensus
    app.register_blueprint(consensus, url_prefix='/consensus')
    
    # config secret key
    app.config['SECRET_KEY'] = 'secret_key'
    
    @app.route('/')
    def hello():
        # return 'Welcome to Web3Env UI!'
        return redirect('/consensus')

    return app