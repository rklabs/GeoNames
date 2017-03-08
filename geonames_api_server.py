#!/usr/bin/env python
import connexion


def app():
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('geonames.yaml')
    app.run(port=8080)

if __name__ == '__main__':
    app()
