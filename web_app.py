# -*- coding: utf-8 -*-

from bottle import route, run, template, static_file, get
# from bottle_sqlite import SQLitePlugin
# import cherrypy  #for deployment
# import pendulum


# install(SQLitePlugin(dbfile='database/db.db'))

@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/css")

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

run(host='localhost', port=8080, debug=True, reloader=True)
#run(server='cherrypy')  # for deployment
