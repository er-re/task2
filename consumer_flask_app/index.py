from flask import Flask, Response

from consume import consume

app = Flask(__name__)


@app.route('/')
def get_assignment():
    return Response(consume.consume_loop(), mimetype="text/event-stream")


if __name__ == '__main__':
   app.run(port=2727)


