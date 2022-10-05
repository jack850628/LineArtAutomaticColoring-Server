import time
import redis
from flaskr.Model.JException import *
from flaskr.Values import Locales as Locales
from flaskr.Model.JException import *
from tasks import Coloring as coloring

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def doColoring(userID, image):
    coloring.doColoring.delay(userID, image)

def waitImage(userID: str):
    r.hset(userID + '佔位', '佔位', '佔位資料')
    try:
        while True:
            image = r.lpop(userID)
            if image != None:
                yield "event: image\ndata: %s\n\n" % image
            else:
                yield "event: heartbeat\ndata: ok\n\n"
            time.sleep(1)
    finally:
        r.delete(userID)
        r.delete(userID + '佔位')

    