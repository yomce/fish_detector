# 그냥 뭐

# 어노테이션이 없다면 뭐
# 백그라운드 넣어 ㅇㅋ

import json
import copy
import shutil


# json 파일 읽기
with open("/home/happyzion/yomce/fish_coco_dataset/coco.json", "r") as f:
	raw_coco = json.load(f)

new_coco = copy.deepcopy(raw_coco)
new_images = []

avail_image_id = []

for ann in raw_coco["annotations"]:
    avail_image_id.append(ann["image_id"])
    


for img in raw_coco["images"]:
    if img["id"] in avail_image_id:
        file_name = img["file_name"]
        src = "/home/happyzion/yomce/fish_coco_dataset/train/" + file_name
        dst = "/home/happyzion/yomce/fish_coco_dataset/images/" + file_name
        shutil.move(src, dst)
        new_images.append(img)
        
        
del new_coco["images"]

new_coco["images"] = new_images

with open("/home/happyzion/yomce/result_2.json", 'w') as outfile:
    json.dump(new_coco, outfile, indent=4)
