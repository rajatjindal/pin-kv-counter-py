from spin_sdk import http, key_value
from spin_sdk.http import IncomingHandler, Request, Response
import json

class Counter:
    def __init__(self, count):
        self.count = count
    
def asCounter(dct):
    return Counter(dct['count'])

class IncomingHandler(IncomingHandler):
    def handle_request(self, request: Request) -> Response:
        store = key_value.open_default()
        
        raw = store.get("counter")
        if raw is not None:
            counter: Counter = asCounter(json.loads(store.get("counter")))
        else:
            counter = Counter(0)
        
        counter.count += 1
        
        store.set("counter", bytes(json.dumps(counter.__dict__), "utf-8"))
        
        return Response(
            200,
            {"content-type": "application/json"},
            bytes(json.dumps(counter.__dict__), "utf-8")
        )
