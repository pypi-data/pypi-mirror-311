import os

import execjs
import geoip2.database

current_dir = os.path.dirname(__file__)
parse_path = os.path.join(current_dir, '..', 'xbase_util_assets', 'arkimeparse.js')
geo_path = os.path.join(current_dir, '..', 'xbase_util_assets', 'GeoLite2-City.mmdb')


def parse_expression(expression):
    if expression:
        with open(parse_path, "r") as f:
            ctx = execjs.compile(f.read())
            return ctx.call("parse_exp", expression)
    else:
        return None


def geo_reader():
    return geoip2.database.Reader(geo_path)
