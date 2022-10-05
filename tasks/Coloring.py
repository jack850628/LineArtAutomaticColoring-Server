import redis

from tasks import app
from flaskr.Model.Pix2pix import create

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

@app.task
def doColoring(userID: str, image: str):
    image = create(image)
    if len(r.hgetall(userID + '佔位')) != 0:
        r.rpush(userID, image)
