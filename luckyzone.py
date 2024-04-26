import time
import json
import datetime

with open("luckyzone_stage.json", "r", encoding="utf-8") as f:
    data_stage = json.load(f)
    
with open("luckyzone_nest.json", "r", encoding="utf-8") as f:
    data_nest = json.load(f)    

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

nest_drop_dict = {
    "獅蠍　　": "神聖、堅韌",
    "賽派特拉": "皎潔、漆黑",
    "火山　　": "燃燒、順風",
    "守護者　": "燃燒、堅韌",
    "迷霧　　": "皎潔、順風",
    "教授Ｋ　": "神聖、漆黑",
    "大主教　": "神聖、燃燒",
    "巨人族　": "神聖、皎潔",
    "錫蘭　　": "皎潔、燃燒",
    "颱風金　": "漆黑、堅韌",
    "克拉努　": "漆黑、順風",
    "岱達羅斯": "順風、堅韌"
}

def getLuckyzone_stage(data_stage, time):
    for week_data in data_stage:
        start_time = int(week_data['起始時間'])
        end_time = int(week_data['結束時間'])
        if start_time <= time <= end_time:
            result = []
            result.append(f"幸運關卡第{week_data['週次']}週")
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

def getLuckyzone_nest(data_nest, time):
    for week_data in data_nest:
        start_time = int(week_data['起始時間'])
        end_time = int(week_data['結束時間'])
        if start_time <= time <= end_time:
            result = []
            result.append(f"幸運巢穴第{week_data['週次']}週")
            result.append(f"<t:{start_time}> ~ <t:{end_time}>")
            nest1 = week_data['幸運巢穴1_巢穴']
            nest2 = week_data['幸運巢穴2_巢穴']
            nest1_values = nest_drop_dict.get(nest1, "")
            nest2_values = nest_drop_dict.get(nest2, "")
            result.append(f"{nest1}:{nest1_values}")
            result.append(f"{nest2}:{nest2_values}")       
            return "\n".join(result)
    return "當前時間不在幸運巢穴時間內"

def getLuckyzoneWeek(week):
    current_time = int(time.time())
    query_time = current_time + 604800 * week
    result = []
    stage = getLuckyzone_stage(data_stage, query_time)
    nest = getLuckyzone_nest(data_nest, query_time)
    result.append(stage)
    result.append(nest) 
    return "\n".join(result)

def getLuckyzoneAuto():
    return getLuckyzoneWeek(0)
  