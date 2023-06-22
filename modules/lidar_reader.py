#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:14:56 2022

@author: wicky
"""

import numpy as np
import open3d as o3d
import queue
from matplotlib import cm



VIRIDIS = np.array(cm.get_cmap('plasma').colors)
VID_RANGE = np.linspace(0.0, 1.0, VIRIDIS.shape[0])
# queue = queue.Queue()
# queue.put(1,2)
# print(queue.get())
pcd = o3d.io.read_point_cloud('../KITTI_Dataset_CARLA_v0.9.13/Carla/Maps/Town10HD_Opt/generated/frames/frame_0000.ply')

# data = np.copy(np.frombuffer(pcd.raw_data, dtype=np.dtype('f4')))
# data = np.reshape(data, (int(data.shape[0] / 4), 4))
# # Isolate the intensity and compute a color for it
# intensity = data[:, -1]
# intensity_col = 1.0 - np.log(intensity) / np.log(np.exp(-0.004 * 100))
# int_color = np.c_[
#     np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 0]),
#     np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 1]),
#     np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 2])]
#
# # Isolate the 3D data
# points = data[:, :-1]
# # We're negating the y to correclty visualize a world that matches
# # what we see in Unreal since Open3D uses a right-handed coordinate system
# points[:, :1] = -points[:, :1]
# point_list = o3d.geometry.PointCloud()
# point_list.points = o3d.utility.Vector3dVector(points)
# point_list.colors = o3d.utility.Vector3dVector(int_color)
vis = o3d.visualization.Visualizer()
vis.create_window(
    window_name='Carla Lidar',
    width=960,
    height=540,
    left=480,
    top=270)
vis.add_geometry(pcd)
vis.get_render_option().background_color = [0.05, 0.05, 0.05]
vis.get_render_option().point_size = 1
vis.get_render_option().show_coordinate_frame = True
# vis.get_render_option(). = 1
vis.run()
vis.destroy_window()