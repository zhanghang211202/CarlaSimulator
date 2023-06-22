import PIL.Image as Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

matplotlib.use('TkAgg')

label_dict={
    (157, 234, 50):(128, 64, 128),
    (145, 170, 100):(152,251,152),
    (100, 40, 40):(190,153,153),
    (55, 90, 80):(0, 0, 0),
    (45, 60, 150):(0, 0, 0),
    (81, 0, 81):(0,0,0),
    (150, 100, 100):(0,0,0),
    (230, 150, 140):(0,0,0),
    (180, 165, 180):(0,0,0),
    (110, 190, 160):(0,0,0),
    (170, 120, 50):(0,0,0),
}

label_to_id_dict={
    (128, 64, 128):0,
    (244, 35, 232):1,
    (70, 70, 70):2,
    (102,102,156):3,
    (190,153,153):4,
    (153,153,153):5,
    (250,170, 30):6,
    (220,220,  0):7,
    (107,142, 35):8,
    (152,251,152):9,
    ( 70,130,180):10,
    (220, 20, 60):11,
    (255,  0,  0):12,
    (  0,  0,142):13,
    (  0,  0, 70):14,
    (  0, 60,100):15,
    (  0, 80,100):16,
    (  0,  0,230):17,
    (119, 11, 32):18,
    (0,0,0):255
}

label_id_dict={
    0:(128, 64,128),
    1:(244, 35,232),
    2:(70, 70, 70),
    3:(102,102,156),
    4:(190,153,153),
    5:(153,153,153),
    6:(250,170, 30),
    7:(220,220,  0),
    8:(107,142, 35),
    9:(152,251,152),
    10:( 70,130,180),
    11:(220, 20, 60),
    12:(255,  0,  0),
    13:(  0,  0,142),
    14:(  0,  0, 70),
    15:(  0, 60,100),
    16:(  0, 80,100),
    17:(  0,  0,230),
    18:(119, 11, 32),
}
# change the key and value of the dictionary
label_id_reverse_dict = dict(zip(label_id_dict.values(), label_id_dict.keys()))

# read the label, change the label to the cityscapes format
def read_label(label_path):
    label = Image.open(label_path)
    label = np.array(label)
    # label = label[:,:,0:3]
    # label = label.astype(np.uint8)
    # label = label[:,:,::-1]
    # label = label.copy()
    for key in label_dict.keys():
        label[np.where((label == key).all(axis = 2))] = label_dict[key]
    return label

# read the mask_label, change it to id




def label_to_id(label_path):
    label = Image.open(label_path)
    label = np.array(label)
    for key in label_to_id_dict.keys():
        label[np.where((label == key).all(axis = 2))] = label_to_id_dict[key]
    return label

# read the label in carla_images_ft, change the label to the cityscapes format
# town_list = ['town01', 'town02', 'town07', 'town10']
# for town in town_list:
#     label_root_path = 'D:/WorkSpace/Carla1/carla_images_ft/labels/'+town+'/'
#     label_save_path = 'D:/WorkSpace/Carla1/carla_images_ft/labels/'+town+'_cs/'
#     for image_file in tqdm(os.listdir(label_root_path)):
#         label_path = label_root_path + image_file
#         label_after = read_label(label_path)
#         label_after = Image.fromarray(label_after)
#         label_after.save(label_save_path+image_file)

town_list = ['town01_cs', 'town02_cs', 'town07_cs', 'town10_cs']
for town in town_list:
    label_root_path = 'D:/WorkSpace/Carla1/carla_images_ft/labels/'+town+'/'
    label_save_path = 'D:/WorkSpace/Carla1/carla_images_ft/labels/'+town+'_id/'
    for image_file in tqdm(os.listdir(label_root_path)):
        label_path = label_root_path + image_file
        label_after = label_to_id(label_path)
        label_after = Image.fromarray(label_after)
        label_after.save(label_save_path+image_file)

