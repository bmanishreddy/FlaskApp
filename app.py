from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hellow')
def hello_world_two():
    return 'Hello World two!'

if __name__ == '__main__':
    app.run()
