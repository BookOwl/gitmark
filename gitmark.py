"""
gitmark.py - Markdown to HTML conversion using Github's API
Created by Matthew (@BookOwl)
Released under the MIT license
"""

import json, requests

class Converter:
    SERVER     = "https://api.github.com"
    MARKDOWN   = ("POST", "/markdown")
    RATE_LIMIT = ("GET",  "/rate_limit")

    def __init__(self, auth=None):
        """Inits the Converter object.
        auth is (username, password) tuple. It is optional, but
        including it means you can convert more documents per hour
        (5000 vs 60)"""
        self.authenticate(auth)

    def authenticate(self, auth):
        "Sets the authorization used to the (username, password) tuple."
        self.auth = auth

    def ratelimit(self):
        """Returns the current rate limit as a dict
        with the keys remaining, limit, and reset"""
        r = requests.request(self.RATE_LIMIT[0],
                             self.SERVER + self.RATE_LIMIT[1],
                             auth = self.auth)
        r.raise_for_status()
        obj = r.json()["resources"]["core"]
        return obj

    def convert(self, md, mode="markdown", context=""):
        """Converts the markdown text md to HTML using the Github API
        mode can be either "markdown" (the default) or "gfm"
        context is the repository context
        See https://developer.github.com/v3/markdown/ for more info."""
        r = requests.request(self.MARKDOWN[0],
                             self.SERVER + self.MARKDOWN[1],
                             data = json.dumps(dict(
                                     text=md,
                                     mode=mode,
                                     context=context)),
                             auth = self.auth
                             )
        r.raise_for_status()
        return r.text
