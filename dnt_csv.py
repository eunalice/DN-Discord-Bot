import os
import pandas as pd
from uistring import getCdata

csv_folder = 'dnt_csv/'
quality_mapping = {
    0: '一般',
    1: '高級',
    2: '稀有',
    3: '史詩',
    4: '珍奇',
    5: '傳奇',
    6: '神話',
    7: '上古'
}
storage_mapping = {1: '是', 0: '否'}

def search_item_by_id(csv_files, target_id):
    for csv_file_path in csv_files:
        file_path = os.path.join(csv_folder, csv_file_path)
        if not os.path.exists(file_path):
            continue
        df = pd.read_csv(file_path) 

        item_data = df[df['id'] == target_id]

        if not item_data.empty:
            return csv_file_path,item_data

    return None
    
def search_item(target_id):
    startswith = "itemtable"
    csv_files = [file for file in os.listdir(csv_folder) if file.startswith(startswith) and file.endswith(".csv")]  
    result = search_item_by_id(csv_files, target_id)
    if result is not None:
        file_name, item_data = result

        file_name = os.path.splitext(file_name)[0]

        name_id = item_data['NameID'].values[0]
        item_id = item_data['id'].values[0]
        rank = item_data['Rank'].values[0]
        description_id = item_data['DescriptionID'].values[0]
        able_storage = item_data['AbleStorage'].values[0]
        able_w_storage = item_data['AbleWStorage'].values[0]
        
        name_id_description = getCdata(name_id)
        description_id_description = getCdata(description_id)
        rank_description = quality_mapping.get(rank, 'Unknown Quality')
        able_storage_description = storage_mapping.get(able_storage, 'Unknown')
        able_w_storage_description = storage_mapping.get(able_w_storage, 'Unknown')

        item_info_string = (
            f"{name_id_description}　　物品ID：{item_id}\n"
            f"品質：{rank_description}　　倉轉：{able_w_storage_description}\n"
            f"物品描述：{description_id_description}\n"
            f"\n數據表：{file_name}\n"
        )

        return item_info_string