import json
import shutil
import copy

from collections import defaultdict
from random import shuffle

# json 파일 읽기
with open("labels/train.json", "r") as f:
	raw_coco = json.load(f)

# 각 카테고리 별 어노테이션 개수 세기
# count_dict = defaultdict(int)

# for ann in raw_coco["annotations"]:
#     category_id = str(ann["category_id"])
#     count_dict[category_id] += 1
# print(count_dict)

# defaultdict(<class 'int'>, {'3': 2132, '5': 159, '2': 651, '1': 2344, '0': 180, '4': 101, '6': 148, '7': 586})

count_image_1 = list()
count_image_3 = list()
count_ann_1 = list()
count_ann_3 = list()

# category가 0~7까지 있음. '1'과 '3'을 600으로 맞춰야하는 코드를 작성해야함
for ann in raw_coco["annotations"]:
    if ann["category_id"] == 1:
        count_image_1.append(ann["image_id"])
        count_ann_1.append(ann["id"])
    elif ann["category_id"] == 3:
        count_image_3.append(ann["image_id"])
        count_ann_3.append(ann["id"])
    else:
        continue

# 랜덤하게 섞기
coco_shuffle = copy.deepcopy(raw_coco)
shuffle(coco_shuffle["annotations"])

# 1번 개수 : 2344 -> 600개?
# 3번 개수 : 2132 -> 600개

my_image_dict = dict()
for img in raw_coco["images"]:
    image_id = img["id"]
    file_name = img["file_name"]
    my_image_dict[image_id] = file_name


del_image_id = []
del_ann_id = []

for ann_1 in coco_shuffle["annotations"]:
    if len(count_ann_1) > 600:
        if ann_1["id"] in count_ann_1:
            # 1. 이미지 정보확인 2. 이미지 move 3. 리스트에 항목 제거
            image_id = ann_1["image_id"]
            file_name = my_image_dict[image_id] # 1.이미지 경로
            src = "/home/happyzion/yomce/train/" + file_name
            dst = "/home/happyzion/yomce/remove/" + file_name
            shutil.move(src, dst)   # 2. 이미지 move
            del_ann_id.append(ann_1["id"])
            del_image_id.append(ann_1["image_id"])
            count_ann_1.remove(ann_1["id"]) # 3. 리스트에 항목 제거
            
            
for ann_3 in coco_shuffle["annotations"]:
    if len(count_ann_3) > 600:
        if ann_3["id"] in count_ann_3:
            # 1. 이미지 정보확인 2. 이미지 move 3. 리스트에 항목 제거
            image_id = ann_3["image_id"]
            file_name = my_image_dict[image_id] # 1.이미지 경로
            src = "/home/happyzion/yomce/train/" + file_name
            dst = "/home/happyzion/yomce/remove/" + file_name
            shutil.move(src, dst)   # 2. 이미지 move
            del_ann_id.append(ann_3["id"])
            del_image_id.append(ann_3["image_id"])
            count_ann_3.remove(ann_3["id"]) # 3. 리스트에 항목 제거

new_images = []
new_annotations = []

del coco_shuffle["annotations"]
del coco_shuffle["images"]

for raw_ann in raw_coco["annotations"]:
    if raw_ann["id"] in del_ann_id:
        pass
    else:
        new_annotations.append(raw_ann)

for raw_img in raw_coco["images"]:
    if raw_ann["id"] in del_image_id:
        pass
    else:
        new_images.append(raw_img)
        
coco_shuffle["annotations"] = new_annotations
coco_shuffle["images"] = new_images

with open("/home/happyzion/yomce/result.json", 'w') as outfile:
    json.dump(coco_shuffle, outfile, indent=4)
