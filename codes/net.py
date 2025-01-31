"""
EE 5561 - Image Processing
Final Project
Deadline: December 17, 2023
coded by: Justine Serdoncillo start 12/6/23
"""

#### IMPORT LIBRARIES ####
import torch
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import torch.nn as nn
import numpy as np

#### Residual Block
def res_block(in_channels, out_channels, strides, first=False):
    layers = []
    if first:
        layers.append(nn.BatchNorm2d())
        layers.append(nn.ReLU())
    layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=strides[0]))
    layers.append(nn.BatchNorm2d())
    layers.append(nn.ReLU())
    layers.append(nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=strides[1]))
    
    return nn.Sequential(*layers)
        

class deepResUnet(nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.encoding1 = res_block(in_channels, 64, [1,1], first=True)
        self.encoding2 = res_block(64, 128, [2,1])
        self.encoding2 = res_block(128, 256, [2,1])
        self.bridge = res_block(256, 512, [2,1])
        self.decoding1 = res_block(512, 256, [1,1])
        self.decoding2 = res_block(256, 128, [1,1])
        self.decoding3 = res_block(128, 64, [1,1])
        self.upsamp = nn.Upsample()
        self.conv = nn.Conv2d(1,1)
        self.sigmoid = nn.Sigmoid()
           
    def forward(self, x):
        # encoding
        y1 = self.encoding1(x) + x
        y2 = self.encoding2(y1) + y1
        y3 = self.encoding3(y2) + y2
    
        # bridge
        y_bridge = self.bridge(y3) + y3

        # decoding
        Y1 = nn.cat(self.upsamp(y_bridge), y3)
        Y1 = self.decoding1(Y1) + Y1
        Y2 = nn.cat(self.upsamp(Y1), y2)
        Y2 = self.decoding1(Y2) + Y2
        Y3 = nn.cat(self.upsamp(Y2), y1)
        Y3 = self.decoding1(Y3) + Y3
        y = self.conv(Y3)
        y = self.sigmoid(y)
        
        return y

        

