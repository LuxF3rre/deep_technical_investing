# -*- coding: utf-8 -*-

import io

import cherrypy
import requests
from bottle import get, route, run, static_file, template
#from bottle_sqlite import SQLitePlugin

# install(SQLitePlugin(dbfile='db.db'))


@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="/static/css")


@get("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="static/font")


@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")


@get("/static/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/js")


@route('/')
def index():
    return template('index')


@route('/about')
def index():
    return template('index')


@route('/contact')
def index():
    return template('index')


def main(debug=True):
    if debug:
        run(host='localhost', port=8080, debug=True, reloader=True)
    else:
        run(server='cherrypy')


if __name__ == '__main__':
    main()
