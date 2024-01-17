import time
import json
import datetime

with open("luckyzone.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 取得當前的UNIX時間戳
current_time = int(time.time())

part_dict = {
    "阿露亞倫戴關卡": "頭盔",
    "紅蓮宮街市": "上衣",
    "拉達梅斯": "上衣",
    "梅露卡之心": "下裝",
    "梅露卡港口": "下裝",
    "利伯偉特停泊處": "手套",
    "海勒瑪堤港口": "鞋子",
    "黑山山腳": "鞋子"
}

def getLuckyzone(data, time):
    for week_data in data:
        start_time = int(week_data['起始時間'])
        end_time = int(week_data['結束時間'])
        if start_time <= time <= end_time:
            result = []
            result.append(f"<t:{start_time}> ~ <t:{end_time}>")
            for part in ["頭盔", "上衣", "下裝", "手套", "鞋子"]:
                found_part = False
                for i in range(1, 4):
                    location = week_data[f"幸運關卡{i}_地區"]
                    if part_dict.get(location) == part:
                        result.append(f"{part}：{week_data[f'幸運關卡{i}_關卡']}")
                        found_part = True
                        break
                if not found_part:
                    result.append(f"{part}：--")
            return "\n".join(result)
    return "當前時間不在幸運關卡時間內"

def getLuckyzoneWeek(week):
    query_time = current_time + 604800 * week
    return getLuckyzone(data, query_time)

def getLuckyzoneAuto():
    return getLuckyzoneWeek(0)
  