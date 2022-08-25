import json
from flask import Response

class Ext:
    def __init__(self):
        self.verbs = {
            'onSessionClose': self.onSessionClose,
            'onSessionOpen': self.onSessionOpen,
            'predicate': self.predicate,
            'prioritize': self.prioritize,
            'jobEnqueueable': self.jobEnqueueable
        }


    def onSessionOpen(self, request):
        try:
            self.session = request.get_json()
            return Response('', mimetype='application/json', status=200)
        except:
            return Response('', mimetype='application/json', status=400)


    def onSessionClose(self, request):
        return Response('', mimetype='application/json', status=200)


    def predicate(self, request):
        try:
            req = request.get_json()
        except:
            return Response('', mimetype='application/json', status=400)

        if 'task' not in req or 'node' not in req:
            return Response('', mimetype='application/json', status=400)

        resp = {'ErrorMessage': ''}
        if req['task']['BestEffort'] and len(req['node']['Tasks']) > 10:
            resp['ErrorMessage'] = 'Already too tasks on this node!'

        return Response(json.dumps(resp), mimetype='application/json', status=200)


    def prioritize(self, request):
        try:
            req = request.get_json()
        except:
            return Response('', mimetype='application/json', status=400)

        if 'task' not in req or len(req['nodes']):
            return Response('', mimetype='application/json', status=400)

        resp = {'NodeScore': {}, 'ErrorMessage': ''}
        for node in req['nodes']:
            if req['task']['BestEffort'] and len(req['nodes'][node]['Tasks']) > 10:
                resp['NodeScore'][req['nodes'][node]['name']] = 0.0
            else:
                resp['NodeScore'][req['nodes'][node]['name']] = 1.0

        return Response(json.dumps(resp), mimetype='application/json', status=200)


    def jobEnqueueable(self, request):
        try:
            req = request.get_json()
        except:
            return Response('', mimetype='application/json', status=400)

        if 'task' not in req or len(req['nodes']):
            return Response('', mimetype='application/json', status=400)

        resp = 1

        return Response(json.dumps(resp), mimetype='application/json', status=200)