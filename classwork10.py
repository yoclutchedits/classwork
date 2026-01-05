import cv2 
import matplotlib.pyplot as plt
import numpy as np
def display_image(title, image):
    plt.figure(figsize=(12,8))
    if len(image.shape)==2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()
def interactive_edge_detection(image_path):
    image=cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return
    gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    display_image('original gray image', gray_image)
    print("select an option:")
    print("1. Canny Edge Detection")
    print("2. Sobel Edge Detection")
    print("3. Laplacian Edge Detection")
    print("4. gaussian smoothing")
    print("5. median filtering")
    print("6. exit")
    while True:
        choice=input("enter your choice (1-6): ")
        if choice=="1":
            print("adjust Canny parameters:")
            lower_threshold=int(input("enter lower threshold (0-255): "))
            upper_threshold=int(input("enter upper threshold (0-255): "))
            Edges=cv2.Canny(gray_image,lower_threshold,upper_threshold)
            display_image("canny edge detection", Edges)
        elif choice=="2":
            Sobel_x=cv2.Sobel(gray_image,cv2.CV_64F,1,0,ksize=5)
            Sobel_y=cv2.Sobel(gray_image,cv2.CV_64F,0,1,ksize=5)
            combined_sobel=cv2.bitwise_or(Sobel_x.astype(np.uint8),Sobel_y.astype(np.uint8))
            display_image("sobel edge detection", combined_sobel)
        elif choice=="3":
            Laplacian=cv2.Laplacian(gray_image,cv2.CV_64F)
            display_image("laplacian edge detection",np.abs(Laplacian).astype(np.uint8))
        elif choice=="4":
            print("adjust kernal size for gaussian smoothing(must be odd):")
            ksize=int(input("enter kernel size: "))
            blured_image=cv2.GaussianBlur(image,(ksize,ksize),0)
            display_image("gaussian smoothing", blured_image)
        elif choice=="5":
            print("adjust kernal size for gaussian smoothing(must be odd):")
            ksize=int(input("enter kernel size: "))
            median_filtered=cv2.medianBlur(image,ksize)
            display_image("median filtering", median_filtered)
        elif choice=="6":
            print("exiting...")
            break
        else:
            print("invalid choice, please try again.")
interactive_edge_detection('example.jpg')
