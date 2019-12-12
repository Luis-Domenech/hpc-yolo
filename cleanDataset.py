import os
import random
import cv2
import pickle
from shutil import copyfile
import xml.etree.ElementTree as ET


def cleanDataset(image_dir):
    
    print("Cleaning Dataset :)")

    xmls = []

    for root, dirs, filenames in os.walk(image_dir):
                

        for f in os.listdir(image_dir):
            # if(f.split(".")[1].lower() in ["png", "jpeg", "jpg"]):
            if(f.split(".")[1].lower() in ["xml"]):
                
                try:
                    tree = ET.parse(image_dir + "/" + f)
                    root = tree.getroot()

                    x = root.findall(".//filename")[0].text
                    x = root.findall(".//width")[0].text
                    x = root.findall(".//height")[0].text
                    x = root.findall(".//name")[0].text
                    x = root.findall(".//xmin")[0].text
                    x = root.findall(".//ymin")[0].text
                    x = root.findall(".//xmax")[0].text
                    x = root.findall(".//ymax")[0].text

                    xmls.append(f.split(".")[0])
                except:
                    print("Omitting: " + f)

        for f in os.listdir(image_dir):
            if(f.split(".")[1].lower() in ["png", "jpeg", "jpg"]):

                if f.split(".")[0] not in xmls:
                    print("Removing: " + f)
                    os.remove(image_dir + "/" + f)
                

                
cleanDataset("test_rgb")
cleanDataset("train_rgb")
cleanDataset("test_hsv")
cleanDataset("train_hsv")
cleanDataset("test_lab")
cleanDataset("train_lab")
cleanDataset("test_xyz")
cleanDataset("train_xyz")
cleanDataset("test_ycb")
cleanDataset("train_ycb")

