'''
Function:
    Implementation of ASPPHead
Author:
    Zhenchao Jin
'''
import torch
import torch.nn as nn
from ..encoders import BuildActivation, BuildNormalization, actname2torchactname


'''ASPPHead'''
class ASPPHead(nn.Module):
    def __init__(self, in_channels, out_channels, dilations, norm_cfg=None, act_cfg=None):
        super(ASPPHead, self).__init__()
        # set attributes
        self.in_channels = in_channels
        self.out_channels = out_channels
        # parallel convolutions
        self.parallel_convs = nn.ModuleList()
        for idx, dilation in enumerate(dilations):
            if dilation == 1:
                conv_cfg = {
                    'in_channels': in_channels, 'out_channels': out_channels, 'kernel_size': 1, 
                    'stride': 1, 'padding': 0, 'dilation': dilation, 'bias': False
                }
            else:
                conv_cfg = {
                    'in_channels': in_channels, 'out_channels': out_channels, 'kernel_size': 3, 
                    'stride': 1, 'padding': dilation, 'dilation': dilation, 'bias': False
                }
            conv = nn.Conv2d(**conv_cfg)
            self.parallel_convs.append(conv)
        self.parallel_bn = nn.Sequential(
            BuildNormalization(placeholder=out_channels * len(dilations), norm_cfg=norm_cfg),
            BuildActivation(act_cfg=act_cfg),
        )
        # global branch
        self.global_branch = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False),
            BuildNormalization(placeholder=out_channels, norm_cfg=norm_cfg),
            BuildActivation(act_cfg=act_cfg),
            nn.Conv2d(out_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False),
        )
        # output project
        self.bottleneck_conv = nn.Conv2d(out_channels * len(dilations), out_channels, kernel_size=1, stride=1, padding=0, bias=False)
        self.bottleneck_bn = nn.Sequential(
            BuildNormalization(placeholder=out_channels, norm_cfg=norm_cfg),
            BuildActivation(act_cfg=act_cfg),
        )
        # initialize parameters'''
        if hasattr(self.bottleneck_bn[0], 'activation'):
            self.initparams(self.bottleneck_bn[0].activation, self.bottleneck_bn[0].activation_param)
        else:
            self.initparams(actname2torchactname(act_cfg['type']), act_cfg.get('negative_slope'))
    '''initialize parameters'''
    def initparams(self, nonlinearity, param=None):
        gain = nn.init.calculate_gain(nonlinearity, param)
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.xavier_normal_(module.weight.data, gain)
                if hasattr(module, 'bias') and module.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(module, nn.BatchNorm2d):
                if hasattr(module, 'weight') and module.weight is not None:
                    nn.init.constant_(m.weight, 1)
                if hasattr(module, 'bias') and module.bias is not None:
                    nn.init.constant_(m.bias, 0)
    '''forward'''
    def forward(self, x):
        input_size = x.shape
        # feed to parallel convolutions
        outputs = torch.cat([conv(x) for conv in self.parallel_convs], dim=1)
        outputs = self.parallel_bn(outputs)
        outputs = self.bottleneck_conv(outputs)
        # feed to global branch
        global_feats = self.global_branch(x)
        global_feats = global_feats.repeat(1, 1, x.size(2), x.size(3))
        # shortcut
        outputs = outputs + global_feats
        outputs = self.bottleneck_bn(outputs)
        # return
        return outputs