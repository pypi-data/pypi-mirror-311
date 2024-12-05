import re

import execjs

from xbase_util.xbase_constant import parse_path


def parse_expression(expression):
    if expression:
        with open(parse_path, "r") as f:
            ctx = execjs.compile(f.read())
            return ctx.call("parse_exp", expression)
    else:
        return None


# def geo_reader():
#     return geoip2.database.Reader(geo_path)


def split_samples(sample, per_subsection):
    num_subsections = len(sample) // per_subsection
    remainder = len(sample) % per_subsection
    subsection_sizes = [per_subsection] * num_subsections
    if remainder > 0:
        subsection_sizes.append(remainder)
        num_subsections += 1
    return num_subsections, subsection_sizes


def split_process(subsection, process_count):
    subsection_per_process = len(subsection) // process_count
    remainder = len(subsection) % process_count
    lengths = []
    start = 0
    for i in range(process_count):
        end = start + subsection_per_process + (1 if i < remainder else 0)
        lengths.append(end - start)
        start = end
    return lengths


def build_es_expression(size, start_time, end_time, arkime_expression):
    expression = {"query": {"bool": {"filter": []}}}
    try:
        if size:
            expression['size'] = size
        if start_time:
            expression['query']['bool']['filter'].append(
                {"range": {"firstPacket": {"gte": round(start_time.timestamp() * 1000)}}})
        if end_time:
            expression['query']['bool']['filter'].append(
                {"range": {"lastPacket": {"lte": round(end_time.timestamp() * 1000)}}})
        arkime_2_es = parse_expression(arkime_expression)
        if arkime_2_es:
            expression['query']['bool']['filter'].append(arkime_2_es)
        return expression
    except Exception as e:
        print(f"请安装nodejs{e}")
        print(arkime_expression)
        exit(1)


def get_uri_depth(url):
    match = re.match(r'^[^?]*', url)
    if match:
        path = match.group(0)
        # 去除协议和域名部分
        path = re.sub(r'^https?://[^/]+', '', path)
        segments = [segment for segment in path.split('/') if segment]
        return len(segments)
    return 0


def firstOrZero(param):
    if type(param).__name__ == 'list':
        if (len(param)) != 0:
            return param[0]
        else:
            return 0
    else:
        return 0
