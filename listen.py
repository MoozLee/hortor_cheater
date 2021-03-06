import re
import json
from mitmproxy import ctx
from urllib.parse import quote
import string
import requests

def response(flow):
    path = flow.request.path
    if path == '/question/bat/findQuiz':
        content = flow.response.content
        data = json.loads(content)
        question = data['data']['quiz']
        options = data['data']['options']
        ctx.log.info('question : %s, options : %s'%(question, options))
        options = ask(question, options)
        data['data']['options'] = options
        flow.response.text = json.dumps(data)


def ask(question, options):
    url = quote('http://www.baidu.com/s?wd=' + question, safe = string.printable)
    content = requests.get(url).text
    answer = []
    for option in options:
        count = content.count(option)
        ctx.log.info('option : %s, count : %s'%(option, count))
        answer.append(option + ' [' + str(count) + ']')
    return answer

