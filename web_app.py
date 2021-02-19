# -*- coding: utf-8 -*-

from bottle import route, run, template
# from bottle_sqlite import SQLitePlugin
# import cherrypy  #for deployment

app = Bottle()

with app:
    # install(SQLitePlugin(dbfile='database/db.db'))

    @route('/')
    def index():
        return template('index')

    run(host='localhost', port=8080, debug=True, reloader=True)
    # bottle.run(server='cherrypy')  # for deployment
