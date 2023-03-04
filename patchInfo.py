import requests
from datetime import datetime
import pytz

def timeConvert(time_string):
    dt = datetime.strptime(time_string, '%a, %d %b %Y %H:%M:%S %Z')
    utc_time = pytz.utc.localize(dt)
    taipei_time = utc_time.astimezone(pytz.timezone('Asia/Taipei'))
    taipei_offset = taipei_time.strftime('%z')
    taipei_offset = f'UTC{taipei_offset[:3]}:{taipei_offset[3:]}'
    return taipei_time.strftime('%Y年%m月%d日 %H:%M:%S') 

def timeSince(date_str):
    date = datetime.strptime(date_str, "%Y年%m月%d日 %H:%M:%S")
    now = datetime.now()
    delta = now - date
    if delta.days > 0:
        return f"{delta.days}天前"
    elif delta.seconds // 3600 > 0:
        return f"{delta.seconds // 3600}小時前"
    elif delta.seconds // 60 > 0:
        return f"{delta.seconds // 60}分鐘前"
    else:
        return "剛剛"

def getVersion(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        version_line = content.split('\n')[0]
        version = version_line.split()[1]
        lastModified_Convert = timeConvert(response.headers.get('Last-Modified'))
        lastModified_Since = timeSince(lastModified_Convert);
        last_modified = lastModified_Convert + "," + lastModified_Since         
        return version, last_modified
    else:
        return None, None

def getVersions(urls):
    contents = {name: getVersion(url) for name, url in urls}
    return contents

def printVersions(contents):
    print("[各服版本號及最後修改時間]")
    for name, (content, last_modified) in contents.items():
        print(f"{name:4}：{content:>4} ({last_modified})")

def getPatchInfo():
    urls = [
        ('KO', 'http://patchkr.dragonnest.com/Patch/PatchInfoServer.cfg'),
        ('CN', 'https://lzg.jijiagames.com/dn/patchinfo/Public/PatchInfoServer.cfg'), 
        ('TW', 'http://tw.cdnpatch.dragonnest.beanfun.com/dragonnest/PatchInfoServer.cfg'),
        ('JP', 'https://patchjp.dragonnest.com/Game/Patch/PatchInfoServer.cfg'),
        ('SEA', 'https://patchsea.dragonnest.com/Game/DragonNest/Patch/PatchInfoServer.cfg'),
        ('CN_L', 'https://lzg.jijiagames.com/dn/patchinfo/Legacy/PatchInfoServer.cfg')
    ]
    contents = getVersions(urls)
    result = []
    for name, (content, last_modified) in contents.items():
        result.append(f"{name}: {content} ({last_modified})")
    return "\n".join(result)