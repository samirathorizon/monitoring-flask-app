import time
import random
from flask import Flask
from prometheus_client import Counter, generate_latest, Summary

app = Flask(__name__)
view_metric = Counter('view', 'Product view', ['product'])
buy_metric = Counter('buy', 'Product buy', ['product'])
view_duration = Summary('view_duration_seconds', 'Time spent in product view')
buy_duration = Summary('buy_duration_seconds', 'Time spent to buy a product')


@app.route('/view/<id>')
@view_duration.time()
def view_product(id):
    time.sleep(random.uniform(1, 2))
    view_metric.labels(product=id).inc()
    return "View %s" % id

@app.route('/buy/<id>') 
@buy_duration.time()
def buy_product(id):
    time.sleep(random.uniform(1, 2))
    buy_metric.labels(product=id).inc()
    return "Buy %s" % id

@app.route('/metrics')
def metrics():
    return generate_latest()
