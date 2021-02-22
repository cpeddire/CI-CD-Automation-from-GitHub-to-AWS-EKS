from flask import Flask
from flask import make_response
app = Flask(__name__)
@app.route('/')
def home():
    return "Hello World!"
@app.route('/<page_name>')
def other_page(page_name):
    response = make_response('Hello World-test-master! response from %s environment' \
                             % page_name, 200)
    return response
if __name__ == '__main__':
    app.run(host="0.0.0.0",port="80",debug=True)
