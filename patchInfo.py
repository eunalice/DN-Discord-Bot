import aiohttp
import asyncio
from datetime import datetime
import pytz

def timeConvert(time_string):
    date = datetime.strptime(time_string, '%a, %d %b %Y %H:%M:%S %Z')
    utc_time = pytz.utc.localize(date)
    taipei_time = utc_time.astimezone(pytz.timezone('Asia/Taipei'))
    taipei_offset = taipei_time.strftime('%z')
    taipei_offset = f'UTC{taipei_offset[:3]}:{taipei_offset[3:]}'
    return taipei_time.strftime('%Y年%m月%d日 %H:%M:%S') 

def timeSince(time_string):
    date = datetime.strptime(time_string, '%a, %d %b %Y %H:%M:%S %Z')
    date_unix  = date.timestamp()
    now = datetime.utcnow()
    now_unix  = now.timestamp()
    delta = datetime.fromtimestamp(now_unix) - datetime.fromtimestamp(date_unix)
    if delta.days > 0:
        return f"{delta.days}天前"
    elif delta.seconds // 3600 > 0:
        return f"{delta.seconds // 3600}小時前"
    elif delta.seconds // 60 > 0:
        return f"{delta.seconds // 60}分鐘前"
    else:
        return "剛剛"

async def getVersion(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text(encoding='utf-8')
            version_line = content.split('\n')[0]
            version = version_line.split()[1]
            lastModified_Original = response.headers.get('Last-Modified')
            lastModified_Convert = timeConvert(lastModified_Original)
            lastModified_Since = timeSince(lastModified_Original);
            last_modified = lastModified_Convert + "," + lastModified_Since
            return version, last_modified
        else:
            return None, None

async def getVersions(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for name, url in urls:
            task = asyncio.create_task(getVersion(session, url))
            tasks.append((name, task))
        contents = {}
        for name, task in tasks:
            content = await task
            contents[name] = content
    return contents

def printVersions(contents):
    print("[各服版本號及最後修改時間]")
    for name, (content, last_modified) in contents.items():
        print(f"{name:4}：{content:>4} ({last_modified})")

async def getPatchInfo():
    urls = [
        ('KO', 'http://patchkr.dragonnest.com/Patch/PatchInfoServer.cfg'),
        ('CN', 'https://lzg.jijiagames.com/dn/patchinfo/Public/PatchInfoServer.cfg'), 
        ('TW', 'http://tw.cdnpatch.dragonnest.beanfun.com/dragonnest/PatchInfoServer.cfg'),
        ('JP', 'https://patchjp.dragonnest.com/Game/Patch/PatchInfoServer.cfg'),
        ('SEA', 'https://patchsea.dragonnest.com/Game/DragonNest/Patch/PatchInfoServer.cfg'),
        ('CN_L', 'https://lzg.jijiagames.com/dn/patchinfo/Legacy/PatchInfoServer.cfg')
    ]
    contents = await getVersions(urls)
    result = []
    for name, (content, last_modified) in contents.items():
        result.append(f"{name}: {content} ({last_modified})")
    return "\n".join(result)