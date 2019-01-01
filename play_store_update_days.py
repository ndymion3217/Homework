# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import sys
import requests
import re
import datetime

def timestamp():  # 현재 시간을 [0000-00-00 00:00:00] 형식으로 리턴
    return '[' +datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']'

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
    ]  #

PAGE_REFRESH_TIME = sys.argv[2]  # 페이지 새로고침 변수를 세번쨰 시스템 변수로 할당
PORT_NUMBER = int(sys.argv[1])  # 포트 번호 변수를 두번째 시스템 변수로 할당
class PlayStoreHandler(BaseHTTPRequestHandler):
    def get_play_update_days_string(self, v):
        # en
        #response = requests.get('https://play.google.com/store/apps/details?id=' + sys.argv[1])
        # kr
        response = requests.get('https://play.google.com/store/apps/details?id=' + v[1] + '&hl=ko')  # 패키지 변수에 지정되어있던 두번째 원소(주소값)을 받아 응답객체를 만듦
        print(timestamp(), v[0], v[1], str(response.status_code))  # 시간과 페이지 이름, 주소, 객체의 상태를 출력함함
        # #print r.text

        # en
        #r = re.search(u'(January|Feburary|March|April|May|June|July|August|September|October|November|December)( +)([1-9]|[12][0-9]|3[01])(, +)(20[0-9][0-9])', response.text)
        # kr
        r = re.search(u'(20[0-9][0-9])년( +)([1-9]|1[0-2])월( +)([1-9]|[12][0-9]|3[01])일', response.text)

        if r is None:  # 설정한 시간이 발견되지 않으면
            print(timestamp(), v[0], 'invalid..')
            return v[0] + 'invalid..'  # 페이지 이름과 invalid를 반환

        print(timestamp(), r.group(0))  # 현재 시간과 ??를 출력
        year = r.group(1)  # r.search에서 검색한 1번쨰 그룹을 year변수에 할당
        month = r.group(3)  # 3번째 그룹을 month변수에 할당
        day =  r.group(5)  # 5번째 그룹을 day변수에 할당
        update = datetime.datetime(int(year), int(month), int(day), 0, 0, 0, 0)  # 실제 날짜가 적용된 datetime 객체를 update변수에 할당

        later = datetime.datetime.now() - update  # 마지막 업데이트로부터 지금까지 지난시간을 later변수에 할당 ??

        ret  = v[0] + ', '  'last update: ' + update.strftime('%Y-%m-%d') + ', ' + str(later.days) + ' days ago'
        #print timestamp(), ret
        return [later.days, ret]  # 마지막 업데이트를 반환

    #Handler for the GET requests
    def do_GET(self):
        if self.path == '/favicon.ico':
            return

        self.send_response(200)  # 응답을 보낼 시간 설정
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
    if len(sys.argv) != 3:  # 시스템변수가 3개가 아닐때
        print(timestamp(), 'invalid')  # 현재시간과 무효를 출력
        sys.exit()  # 프로그램 종료

    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), PlayStoreHandler)  # 서버를 생성해 변수에 할당
    print(timestamp(), 'Started httpserver on port ' , PORT_NUMBER)  # 현재시간과 ~포트에 서버가 시작됐다고 출력

    #Wait forever for incoming htto requests
    server.serve_forever()  # 끄지않는한 계속 서버 가동
except KeyboardInterrupt:  # 키보드가 눌리는 에러가 났을때
    print(timestamp(), '^C received, shutting down the web server')  # 현재시간과 ^C가 눌려서 웹서버를 종료 한다는 메세지 출력
    server.socket.close()  # 서버를 종료
