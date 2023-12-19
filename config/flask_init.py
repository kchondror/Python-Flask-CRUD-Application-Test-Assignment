# Creating a Flask application instance and configuring various settings.
from lib.flask_imports import *

template_dir = os.path.abspath('../frontend - views')
static_dir = os.path.abspath('../../web')

app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)

app.config['SECRET_KEY'] = 'demo_key'

