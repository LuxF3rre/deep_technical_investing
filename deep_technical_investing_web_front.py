# -*- coding: utf-8 -*-

import fastai
import mplfinance as fplt
import numpy as np
import pandas as pd
from bottle import route, run, template


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


run(host='localhost', port=8080)
