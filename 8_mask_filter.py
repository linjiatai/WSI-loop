import os
from PIL import Image
from skimage import morphology
import cv2
import numpy as np
Image.MAX_IMAGE_PIXELS = None
def mask_filter(mask):
    mask_np = np.asarray(mask)
    mask_np_cp = mask_np.copy()
    mask_np = np.array(mask_np).astype(np.uint8)

    ## del small noise in region
    for i in range(mask_np.max()):
        dst = morphology.remove_small_objects(mask_np!=i+1,min_size=224*224*2,connectivity=1)
        mask_np[dst==False]=i+1
    
    ## del small tumor region
    dst = morphology.remove_small_objects(mask_np==2,min_size=224*224*0.5,connectivity=1)
    mask_np[dst!=(mask_np==2)]=1

    ## Do not del BG, stroma and nomal region
    mask_np[mask_np_cp==3]=3
    mask_np[mask_np_cp==1]=1
    mask_np[mask_np_cp==0]=0
    
    ## del small tissue region of any type.
    dst = morphology.remove_small_objects(mask_np!=0,min_size=224*224*10,connectivity=1)
    mask_np[dst==False]=0
    
    return mask_np

maskpath = '/media/linjiatai/linjiatai-16TB/兵兵/Multi-step/SAVE/Original_dataset/seg_mask/'
maskpath_new = '/media/linjiatai/linjiatai-16TB/兵兵/Multi-step/SAVE/Original_dataset/seg_mask_filter/'
palette = [0]*100
palette[0:3] = [255,255,255]    # 白色 背景
palette[3:6] = [120,120,120]    # 灰色 正常
palette[6:9] = [255,0,0]        # 红色 肿瘤
palette[9:12] = [0,255,0]       # 绿色 间质
palette[12:15] = [0,255,255]    # 青色 粘液
palette[15:18] = [255,0,255]    # 紫色 坏死
palette[18:21] = [237,145,33]   # 土黄 肌肉
for root, _, files in os.walk(maskpath):
    for file in sorted(files):
        print(file)
        mask = Image.open(root+'/'+file)
        mask_np = mask_filter(mask)
        mask_new = Image.fromarray(np.uint8(mask_np), 'P')
        mask_new.putpalette(palette)
        mask_new.save(maskpath_new+file)