class YOLOV1(nn.Module):
    def __init__(self):
       super(YOLOV1,self).__init__()
       vgg = VGG()
       self.extractor = vgg.extractor
       self.avgpool = nn.AdaptiveAvgPool2d((7,7))
       # 决策层：检测层
       self.detector = nn.Sequential(
          nn.Linear(512*7*7,4096),
          nn.ReLU(True),
          nn.Dropout(),
          #nn.Linear(4096,1470),
          nn.Linear(4096,245),
          #nn.Linear(4096,5),
       )
       for m in self.modules():
           if isinstance(m,nn.Conv2d):
               nn.init.kaiming_normal_(m.weight,mode='fan_out',nonlinearity='relu')
               if m.bias is not None: 
                   nn.init.constant_(m.bias,0)
           elif isinstance(m,nn.BatchNorm2d):
               nn.init.constant_(m.weight,1)
               nn.init.constant_(m.bias,1)
           elif isinstance(m,nn.Linear):
               nn.init.normal_(m.weight,0,0.01)
               nn.init.constant_(m.bias,0)
    def forward(self,x):
        x = self.extractor(x)
        x = self.avgpool(x)
        x = x.view(x.size(0),-1)
        x = self.detector(x)
        b,_ = x.shape
        x = x.view(b,7,7,30)
        
        return x