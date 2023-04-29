from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .consensus import consensus
    app.register_blueprint(consensus, url_prefix='/consensus')
    
    @app.route('/')
    def hello():
        return 'Welcome to Web3Env UI!'

    return app