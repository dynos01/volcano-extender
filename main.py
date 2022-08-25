import json
from flask import Flask, abort, request
from actions import Ext

extender = Flask(__name__)
ext = Ext()

@extender.route('/<path:verb>', methods=['POST'])
def proc(verb):
    if verb not in ext.verbs.keys():
        abort(404)

    return ext.verbs[verb](request)


if __name__ == '__main__':
    extender.run(host='0.0.0.0', port='2333', debug=True)