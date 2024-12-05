import execjs


def parse_expression(expression):
    if expression:
        with open(f"assets/base/arkimeparse.js", "r") as f:
            ctx = execjs.compile(f.read())
            return ctx.call("parse_exp", expression)
    else:
        return None
