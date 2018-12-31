# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import sys
import requests
import re
import datetime

def timestamp():
    return '[' +datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']'  # 현재 시간을 0000-00-00 00:00:00 형식으로 리턴

packages = \
    [
        ['유비페이', 'com.harex.android.ubpay'],
        ['이지스페이', 'com.harex.android.alltheGate'],

        ['유비포스', 'com.harex.android.apppos'],
        ['우체국포스', 'com.harex.android.postpos'],

        ['투유금융', 'com.knb.mbr'],
        ['투유뱅크 개인', 'com.knb.psb'],
        ['포스트페이', 'com.epost.psf.ss'],
        ['썸뱅크', 'kr.co.bsbank.mobilebank'],
        ['J뱅크', 'com.jejubank.jbank.android'],

        ['포항성모병원', 'kr.spacesoft.mmc.phsmh'],

        ['미납OK', 'com.deepple.hpvm'],

        ['컬쳐랜드', 'com.cultureland.ver2'],
        ['공영홈쇼핑', 'com.pub.fm']
    ]

PAGE_REFRESH_TIME = sys.argv[2]
PORT_NUMBER = int(sys.argv[1])
class PlayStoreHandler(BaseHTTPRequestHandler):
    def get_play_update_days_string(self, v):
        # en
        #response = requests.get('https://play.google.com/store/apps/details?id=' + sys.argv[1])
        # kr
        response = requests.get('https://play.google.com/store/apps/details?id=' + v[1] + '&hl=ko')
        print(timestamp(), v[0], v[1], str(response.status_code))
        #print r.text

        # en
        #r = re.search(u'(January|Feburary|March|April|May|June|July|August|September|October|November|December)( +)([1-9]|[12][0-9]|3[01])(, +)(20[0-9][0-9])', response.text)
        # kr
        r = re.search(u'(20[0-9][0-9])년( +)([1-9]|1[0-2])월( +)([1-9]|[12][0-9]|3[01])일', response.text)

        if r is None:
            print(timestamp(), v[0], 'invalid..')
            return v[0] + 'invalid..'

        print(timestamp(), r.group(0))
        year = r.group(1)
        month = r.group(3)
        day =  r.group(5)
        update = datetime.datetime(int(year), int(month), int(day), 0, 0, 0, 0)

        later = datetime.datetime.now() - update

        ret  = v[0] + ', '  'last update: ' + update.strftime('%Y-%m-%d') + ', ' + str(later.days) + ' days ago'
        #print timestamp(), ret
        return [later.days, ret]

    #Handler for the GET requests
    def do_GET(self):
        if self.path == '/favicon.ico':
            return

        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        # Send the html message
        #self.wfile.write("Hello World !")
        play_ret_list = list()
        for v in packages:
            play_ret_list.append(self.get_play_update_days_string(v))

        play_ret_list.sort()

        output = '<head>'
        output += '<script language="javascript" type="text/javascript">'
        output += 'setTimeout(function () {location.reload();},'
        output += PAGE_REFRESH_TIME + '000'
        output += ');'
        output += '</script>'
        output += '</head>'
        
        output += '<body>'
        for l in play_ret_list:
            color = ''
            if l[0] == 0:
                color = 'red'
            elif l[0] <= 1:
                color = 'red'
            elif l[0] <= 7:
                color = 'blue'
            else:
                color = 'black'

            output += '<font color=' + color + '>'
            output += l[1]
            output += '</font>'
            output += '</br>'
        output += '</br>last check: ' + timestamp()
        output += '</body>'

        self.wfile.write(output)
        print(timestamp(), output)
        return

try:
    if len(sys.argv) != 3:
        print(timestamp(), 'invalid')
        sys.exit()

    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), PlayStoreHandler)
    print(timestamp(), 'Started httpserver on port ' , PORT_NUMBER)

    #Wait forever for incoming htto requests
    server.serve_forever()
except KeyboardInterrupt:
    print(timestamp(), '^C received, shutting down the web server')
    server.socket.close()
