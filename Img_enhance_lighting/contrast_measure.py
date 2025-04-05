import numpy as np
import cv2
import glob

filelist = glob.glob('C:\\Users\\badri\\OneDrive\\Desktop\\IIT Tirupati Academic Documents\\SigmaFluxDataset\\*.jpg')
for i in filelist:
    img = cv2.imread(i)
    print(i[-7:-1],'has the contrast value:',np.std(img))