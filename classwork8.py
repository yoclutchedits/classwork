import cv2
import matplotlib.pyplot as plt
image=cv2.imread('example.jpg')
image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.title('rgb image')
plt.show()
gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
plt.imshow(gray_image,cmap='gray')
plt.title('gray image')
plt.show()
crop_image=image[50:200,100:300]
crop_rgb=cv2.cvtColor(crop_image,cv2.COLOR_BGR2RGB)
plt.imshow(crop_rgb)
plt.title('cropped image')
plt.show()