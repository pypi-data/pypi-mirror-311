import os
import sys
import glob
import subprocess
import argparse

from pytvpaint import george
from pytvpaint.project import Project


def process_remaining_args(args):
    parser = argparse.ArgumentParser(
        description='TVPaint Project Template Arguments'
    )
    parser.add_argument('--ref-path', dest='ref_path')
    # parser.add_argument('--height', dest='height')
    # parser.add_argument('--width', dest='width')

    values, _ = parser.parse_known_args(args)

    return (
        values.ref_path #values.width,values.height
    )

ref_path = process_remaining_args(sys.argv)
# CAMERA_WIDTH = process_remaining_args(sys.argv)[1]
# CAMER_HEIGHT = process_remaining_args(sys.argv)[2]

# change project resolution

project = Project.current_project()
clip = project.current_clip
camera = clip.camera

# project_width = camera_width+300
# project_height = camera_height+170

project.resize(4240,2385,overwrite=True)
project.set_fps(25)
# project.resize(project_width,project_height,overwrite=True)


camera.get_point_data_at(0)
george.tv_camera_set_point(0,2120,1192,0,scale=1)
# george.tv_camera_set_point(0, project_width/2, project_height/2, 0, scale=1)

# -- import img sequence --

img_seq = clip.load_media(media_path=ref_path, with_name="[REF]", preload=True)

# -- change img seq layer position
img_seq.position = 1

project.save()
# project.close_all(True)
