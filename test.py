import requests
import datetime
import slacker
import time
import re
import sys

sys.path.append('C:/Users/SDM/iCloudDrive/iCloud~com~omz-software~Pythonista3/config')  # config 위치
import config

def timestamp():  # 현재 시간을 [0000-00-00 00:00:00] 형식으로 리턴
    return '[' +datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']'

def main():
    slack = slacker.Slacker(config.token)
    for i in config.packages:
        response = requests.get('https://play.google.com/store/apps/details?id=' + i[
            1] + '&hl=ko')  # 패키지 변수에 지정되어있던 두번째 원소(주소값)을 받아 응답객체를 만듦
        print(timestamp(), i[0], i[1], str(response.status_code))

        r = re.search(u'(20[0-9][0-9])년( +)([1-9]|1[0-2])월( +)([1-9]|[12][0-9]|3[01])일', response.text)

        if response.status_code == 404:
            slack.chat.post_message(config.channel, '( {} ) 앱이 구글스토어에 존재하지 않습니다.'.format(i[0]))
            return

        if r is None:  # 설정한 시간이 발견되지 않으면
            print(timestamp(), i[0], 'invalid..')
            return i[0] + 'invalid..'  # 페이지 이름과 invalid를 반환

        #print(timestamp(), r.group(0))  # 현재 시간과 ??를 출력
        year = r.group(1)  # r.search에서 검색한 1번쨰 그룹을 year변수에 할당
        month = r.group(3)  # 3번째 그룹을 month변수에 할당
        day = r.group(5)  # 5번째 그룹을 day변수에 할당
        update = datetime.datetime(int(year), int(month), int(day), 0, 0, 0, 0)  # 실제 날짜가 적용된 datetime 객체를 update변수에 할당

        later = datetime.datetime.now() - update  # 마지막 업데이트로부터 지금까지 지난시간을 later변수에 할당 ??

        ret = i[0] + ', '  'last update: ' + update.strftime('%Y-%m-%d') + ', ' + str(later.days) + ' days ago'
        # print timestamp(), ret
        if ret not in today and later.days == 0:
            today.append(ret)
            slack.chat.post_message(config.channel, '( {} ) 앱의 업데이트가 발견되었습니다.'.format(i[0]))

today = []
while True:
    main()
    time.sleep(config.page_refresh)