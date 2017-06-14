"""Directly from the example of Kyoukai's GitHub repo README.md, solely for testing right now."""
import json
from kyoukai import Kyoukai, HTTPRequestContext

kyk = Kyoukai("example_app")

@kyk.route("/")
async def index(ctx: HTTPRequestContext):
    return json.dumps(dict(ctx.request.headers)), 200, {"Content-Type": "application/json"}