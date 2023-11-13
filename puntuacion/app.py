from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import logging

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

def distancia_manhattan(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Los arrays deben tener la misma longitud")

    distance = 0

    for x, y in zip(array1, array2):
        if x is not None and y is not None:
            distance += abs(x - y)

    return distance


@app.route("/", methods=['POST','GET'])
def hello():
  Angelica = [3.5,2,None,4.5,5,1.5,2.5,2]
  Bill = [2, 3.5,4,None,2,3.5,None,3]
  Chan = [5,1,1,3,5,1,None,None]
  Dan = [3,4,4.5,None,3,4.5,4,2]
  Hailey = [None,4,1,4,None,None,4,1]
  Jordyn = [None,4.5,4,5,5,4.5,4,4]
  Sam = [5,2,None,3,5,4,5,None]
  Veronica = [3,None,None,5,4,2.5,3,None]
  distancia = distancia_manhattan(Angelica,Bill)
  print(distancia)
  if request.method == 'POST':
        redis = get_redis()
        print(distancia)
        redis.rpush('distancia', distancia)
        print("--------------------------------------------------------------------")
        print("Se enviaron los datos a REDIS")
        print(distancia)
  resp = make_response(render_template('index.html'))
  return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
