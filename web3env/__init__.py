import sys
import os
# import dotenv

# add the path to the web3env module to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# dotenv.load_dotenv()

# create data folder if not exist
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'data')):
    os.mkdir(os.path.join(os.path.dirname(__file__), 'data'))
    
# store the path to the data folder into the environment variable
os.environ['DATA_PATH'] = os.path.join(os.path.dirname(__file__), 'data')