import os

import execjs
current_dir = os.path.dirname(__file__)
parse_path = os.path.join(current_dir, '..', 'assets', 'arkimeparse.js')


def parse_expression(expression):
    if expression:
        with open(parse_path, "r") as f:
            ctx = execjs.compile(f.read())
            return ctx.call("parse_exp", expression)
    else:
        return None
