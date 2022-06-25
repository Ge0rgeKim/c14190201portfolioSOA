from distutils.log import debug
from flask import request, Flask

from calculator import bil_palindrom_prima, bil_palindrom_primal
from calculator import bil_prima


app = Flask(__name__)

@app.route('/prima/<int:index>', methods=['GET'])
def prima(index):
    result = bil_prima.delay(index)
    return {'result': result.get()}

@app.route('/palindrom_prima/<int:index>', methods=['GET'])
def palindrom_prima(index):
    result = bil_palindrom_prima.delay(index)
    return {'result': result.get()}

app.run(port=8000, debug = True)