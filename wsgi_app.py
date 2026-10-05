import os
import sys

# the folder this file lives in (works on any machine / server)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# loader.py and classifier use relative paths (data/..., models/...)
os.chdir(BASE_DIR)

from pipeline import load_context
from dashboard import build_dashboard

# load library + model once when the server starts
ctx = load_context()

app = build_dashboard(ctx)

# the variable PythonAnywhere / gunicorn looks for
server = app.server