# run: mitmproxy -k -p 8090 -s oauth-mitmproxy-addon.py
# optional: set Burp upstream proxy to :8090

from mitmproxy import ctx
import re
import oauth_template as ot

class OAuthBurp:
    def __init__(self, refresh_token):
        ctx.log(refresh_token)
        self.refresh_token, self.auth_token = ot.refresh_token(refresh_token)
        ctx.log("init refreshed authorization Bearer token")

    def request(self, flow):
        flow.request.headers["authorization"] = "Bearer %s" % self.auth_token
        ctx.log("authorization Bearer token patched")

    def response(self, flow):
        if flow.request.is_replay:
            self._flow.response = flow.response
            self._flow.resume()
            return
        if flow.response.status_code == 401:
            self.refresh_token, self.auth_token = ot.refresh_token(self.refresh_token)
            ctx.log("refreshed authorization Bearer token")
            flow2 = flow.copy()
            ctx.master.commands.call("replay.client", [flow2])
            flow.intercept()
            self._flow = flow

addons = [
    OAuthBurp(ot.REFRESH_TOKEN)
]
