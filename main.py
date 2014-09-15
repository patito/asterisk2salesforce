from app import AsteriskHandler
from flask import Flask, render_template

import thread


app = Flask(__name__)


def asterisk_connect(t, y):
    ast = AsteriskHandler()
    ast.connect()
    ast.subscribe_cdr_event()
    ast.get_all_extensions()
    ast.loop()

@app.route('/')
def login():
    return render_template('index.html')


if __name__ == '__main__':
    thread.start_new_thread(asterisk_connect, ("ThreadAsterisk", 1))
    app.run()

