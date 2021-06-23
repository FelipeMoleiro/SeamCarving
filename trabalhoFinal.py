import numpy as np
import cv2
import matplotlib.pyplot as plt
import imageio


#Sobel Img Edge Detection
def edgeImg(img):
    #gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
    #gy = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
    #mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelX = cv2.Sobel(gray,cv2.CV_64F,1,0)
    sobelY = cv2.Sobel(gray,cv2.CV_64F,0,1)


    newImg = np.sqrt(np.power(sobelX,2) + np.power(sobelY,2))

    return newImg

#use dynamic programming to find Min Energy Path
def calculateMinEnergyPath(energyImg):
    minEnergyPath = np.zeros(energyImg.shape)
    dir = np.zeros(energyImg.shape)
    n = energyImg.shape[0]
    m = energyImg.shape[1]

    #base case on the last row of the matrix
    for j in range(0,m):
        minEnergyPath[n-1][j] = energyImg[n-1][j]

    print(minEnergyPath)

    #builds matrix from bottom up
    for i in range(n-2,-1,-1):
        for j in range(0,m):
            #print(i,j)

            #just making sure we dont go out of bounds and finding the min
            minPos = j
            center = j
            min = minEnergyPath[i+1][center]

            if(center>0 and minEnergyPath[i+1][center-1] < min):
                min = minEnergyPath[i+1][center-1]
                minPos = center -1

            if(center<m-1 and minEnergyPath[i+1][center+1] < min):
                min = minEnergyPath[i+1][center+1]
                minPos = center+1
            

            minEnergyPath[i][j] = energyImg[i][j] + min
            #dir[i][j] = minPos - center # -1, 0 ou
    return minEnergyPath

def printMinSeam(img,minEnergyPath):
    n = minEnergyPath.shape[0]
    m = minEnergyPath.shape[1]
    
    minPos = 0
    minVal = minEnergyPath[0][0]

    #find Min Seam
    for i in range(1,m):
        if(minEnergyPath[0][i] < minVal):
            minPos = i
            minVal = minEnergyPath[0][i]

    printImg = np.array(img)
    printImg[0][minPos] = [255,255,255]
    for i in range(1,n):
        #find min from three down
        center = minPos
        min = minEnergyPath[i][center]

        if(center>0 and minEnergyPath[i][center-1] < min):
            min = minEnergyPath[i][center-1]
            minPos = center -1

        if(center<m-1 and minEnergyPath[i][center+1] < min):
            min = minEnergyPath[i][center+1]
            minPos = center+1


        printImg[i][minPos] = [255,255,255]
    
    plt.imshow(printImg)
    plt.show()
    return

#img = imageio.imread('imgs/Broadway_tower_edit.jpg')
img = imageio.imread('imgs/PersistenceOfMemory.jpg')

plt.imshow(img)
plt.show()

edge = edgeImg(img)

minEnergyPath = calculateMinEnergyPath(edge)

print(minEnergyPath)

plt.imshow(minEnergyPath,cmap="gray")
plt.show()

printMinSeam(img,minEnergyPath)

#print(edge.shape)