from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# This decorator demonstrates dynamic URL routing
@app.route('/home/<string:name>')
def hello(name):
    return f"Hello {name}!"

# This decorator restricts the HTTP request types that are allowed on our webpage
@app.route('/onlyget', methods=['GET'])
def get_req():
    return 'You can only GET this webpage. POST methods will fail.'

# Boiler plate
if __name__ == "__main__":
    app.run(debug=True)

