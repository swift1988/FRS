import torch.nn as nn
import torch.nn.functional as F

from ..builder import NECKS

@NECKS.register_module()
class ADAP(nn.Module):

    def __init__(self,
                 in_channels,
                 out_channels,
                 num = 5,
                 kernel = 3,
                 with_relu = False):
        super(ADAP, self).__init__()
        self.num = num
        self.conv = nn.ModuleList()
        self.with_relu = with_relu
        for _ in range(num):
            if kernel == 3:
                self.conv.append(nn.Conv2d(in_channels, out_channels, 3, padding=(1, 1)))
            elif kernel == 1:
                self.conv.append(nn.Conv2d(in_channels, out_channels, 1))
            else:
                raise ValueError("other kernel size not completed")
        if with_relu:
            print("The adap conv is with relu")
        else:
            print("The adap conv is without relu")
        #self.const = nn.ConstantPad2d((0,1,0,1), 0.)

    def forward(self, inputs):
        out = []
        for i in range(self.num):
            if self.with_relu:
                out.append(F.relu(self.conv[i](inputs[i])))
            else:
                out.append(self.conv[i](inputs[i]))
            # out.append(F.relu(self.conv[i](inputs[i])))
        return out

@NECKS.register_module()
class ADAP_SINGLE(nn.Module):

    def __init__(self,
                 in_channels,
                 out_channels,
                 num = 5,
                 kernel = 3,
                 with_relu = False):
        super(ADAP_SINGLE, self).__init__()
        self.num = num
        self.with_relu = with_relu
        if kernel == 3:
            self.conv = nn.Conv2d(in_channels, out_channels, 3, padding=(1, 1))
        elif kernel == 1:
            self.conv = nn.Conv2d(in_channels, out_channels, 1)
        else:
            raise ValueError("other kernel size not completed")
        if with_relu:
            print("The adap conv is with relu")
        else:
            print("The adap conv is without relu")
        #self.const = nn.ConstantPad2d((0,1,0,1), 0.)

    def forward(self, inputs):
        out = []
        for i in range(self.num):
            if self.with_relu:
                out.append(F.relu(self.conv(inputs[i])))
            else:
                out.append(self.conv(inputs[i]))
        return out

@NECKS.register_module()
class ADAP_C(nn.Module):

    def __init__(self,
                 in_channels,
                 out_channels,
                 with_relu=False):
        super(ADAP_C, self).__init__()
        self.conv = nn.ModuleList()
        self.with_relu = with_relu
        if len(in_channels) != len(out_channels):
            raise ValueError("the in_channels is {}, but the out_channels is {}".format(len(in_channels), len(out_channels)))
        for i in range(len(in_channels)):
            self.conv.append(nn.Conv2d(in_channels[i], out_channels[i], 3, padding=(1, 1)))

    def forward(self, inputs):
        out = []
        for i in range(len(inputs)):
            if self.with_relu:
                out.append(F.relu(self.conv[i](inputs[i])))
            else:
                out.append(self.conv[i](inputs[i]))
        return out

@NECKS.register_module()
class ADAP_Residule(nn.Module):

    def __init__(self,
                 in_channels,
                 out_channels, residule_conv=False):
        super(ADAP_Residule, self).__init__()
        self.residule_conv = residule_conv
        self.conv1_1 = nn.ModuleList()
        self.conv3 = nn.ModuleList()
        self.conv1_2 = nn.ModuleList()
        self.residule = nn.ModuleList()
        if len(in_channels) != len(out_channels):
            raise ValueError("the in_channels is {}, but the out_channels is {}".format(len(in_channels), len(out_channels)))
        for i in range(len(in_channels)):
            self.conv1_1.append(nn.Conv2d(in_channels[i], in_channels[i], 1))
            self.conv3.append(nn.Conv2d(in_channels[i], in_channels[i], 3, padding=(1, 1)))
            self.conv1_2.append(nn.Conv2d(in_channels[i], out_channels[i], 1))
            if self.residule_conv:
                self.residule.append(nn.Conv2d(in_channels[i], out_channels[i], 1))

    def forward(self, inputs):
        out = []
        for i in range(len(inputs)):
            out_ = F.relu(self.conv1_1[i](inputs[i]))
            out_ = F.relu(self.conv3[i](out_))
            out_ = self.conv1_2[i](out_)
            if self.residule_conv:
                out_ = F.relu(out_ + self.residule[i](inputs[i]))
            else:
                out_ = F.relu(out_ + inputs[i])
            out.append(out_)
        return out