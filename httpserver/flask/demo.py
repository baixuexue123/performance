#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<p>100Credit--Api</p>'


if __name__ == '__main__':
    app.run()

# gunicorn --workers=4 demo:app -b 0.0.0.0:8080 --access-logfile=access.log
# --access-logfile=-  > stdout
