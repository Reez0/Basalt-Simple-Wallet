from basalt_simple_wallet.celery import app


@app.task
def do_something(x, y):
    return x + y
