import json
import shutil
from collections import defaultdict


with open("/home/happyzion/yomce/fish_coco_dataset/coco_2.json", "r") as f:
	raw_coco = json.load(f)
 
# 카테고리별로 5장정도만 샘플링해서 가져오겠읍니다.
sample_dict = defaultdict(list)
my_image_dict = dict()
my_cate_dict = dict()

for img in raw_coco["images"]:
    image_id = img["id"]
    file_name = img["file_name"]
    my_image_dict[image_id] = file_name
    
for cate in raw_coco["categories"]:
    cate_name = cate["name"]
    cate_id = cate["id"]
    my_cate_dict[cate_id] = cate_name
    

for category_num in range(0,8):
    limit = 5
    for ann in raw_coco["annotations"]:
        if limit == 0:
            break
        else:
            if ann["category_id"] == category_num:
                try:
                    file_name = my_image_dict[ann["image_id"]]
                    sample_dict[category_num].append(ann["image_id"])
                    # 이미지 옮기기 ^^
                    src = "/home/happyzion/yomce/fish_coco_dataset/images/" + file_name
                    dst = "/home/happyzion/yomce/fish_coco_dataset/sampling/" + my_cate_dict[category_num] + "_" + file_name
                    print(dst)
                    shutil.copy(src, dst)
                    limit -= 1
                except:
                    pass

    
