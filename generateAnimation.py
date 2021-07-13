#Declaração das funções para rodar o algoritmo
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imageio
from numba import jit
import os


imgNum = 0 # global img counter


#Sobel Img Edge Detection
def edgeImg(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelX = cv2.Sobel(gray,cv2.CV_64F,1,0)
    sobelY = cv2.Sobel(gray,cv2.CV_64F,0,1)

    return np.sqrt(np.power(sobelX,2) + np.power(sobelY,2))

#use dynamic programming to find Min Energy Path
@jit
def calculateMinEnergyPath(energyImg):
    minEnergyPath = np.zeros(energyImg.shape)
    n = energyImg.shape[0]
    m = energyImg.shape[1]

    #base case on the last row of the matrix
    for j in range(0,m):
        minEnergyPath[n-1][j] = energyImg[n-1][j]

    #builds matrix from bottom up
    for i in range(n-2,-1,-1):
        for j in range(0,m):
            #just making sure we dont go out of bounds and finding the min
            left = max(0,j-1)
            right = min(m-1,j+1)
            

            minEnergyPath[i][j] = energyImg[i][j] + min(minEnergyPath[i+1][left:right+1])

    return minEnergyPath

@jit
def removeSeam(img,minEnergyPath):
    n = minEnergyPath.shape[0]
    m = minEnergyPath.shape[1]
    
    minPos = 0
    minVal = minEnergyPath[0][0]

    #find Min Seam
    for i in range(1,m):
        if(minEnergyPath[0][i] < minVal):
            minPos = i
            minVal = minEnergyPath[0][i]

    newImg = np.zeros((img.shape[0],img.shape[1]-1,img.shape[2]),dtype=np.uint8)

    newImg[0] = np.concatenate((img[0][0:minPos],img[0][minPos+1:img.shape[1]]))
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

        newImg[i] = np.concatenate((img[i][0:minPos],img[i][minPos+1:img.shape[1]]))
    
    return newImg

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
    printImg[0][minPos] = [255,0,0]
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


        printImg[i][minPos] = [255,0,0]

    return printImg




def archiveName(i):
    str1 = "tmpFrames/"
    str2 = "%03d" % i
    return str1 + str2 + ".png"

def removeNSeams(img,seamNumber):
    frame = np.zeros(img.shape,dtype=np.uint8)
    newImg = img

    frame *= 0 
    frame[:newImg.shape[0],:newImg.shape[1],:] = newImg
    imageio.imsave(archiveName(imgNum),frame)
    imgNum += 1

    for i in range(0,seamNumber):
        print ('removing seam ',i+1, ' of ', seamNumber, end="\r")
        newEP = calculateMinEnergyPath(edgeImg(newImg))

        imgRemoved = printMinSeam(newImg,newEP)
        frame *= 0 
        frame[:imgRemoved.shape[0],:imgRemoved.shape[1],:] = imgRemoved
        imageio.imsave(archiveName(imgNum),frame)
        imgNum += 1

        newImg = removeSeam(newImg,newEP)

    frame *= 0 
    frame[:newImg.shape[0],:newImg.shape[1],:] = newImg
    imageio.imsave(archiveName(imgNum),frame)
    imgNum += 1

    return newImg

@jit
def findInsertSeam(img,duplicatePixels,minEnergyPath,numSeam,seamMatrix):
    
    n = img.shape[0]
    m = img.shape[1]
        
    #find path
    minPos = 0
    minVal = minEnergyPath[0][0]
    for i in range(1,m):
        if(minEnergyPath[0][i] < minVal):
            minPos = i
            minVal = minEnergyPath[0][i]

    if(np.isinf(duplicatePixels[0][minPos])): return 1 #error, no more space for insertion

    duplicatePixels[0][minPos] = np.inf
    seamMatrix[0][minPos] = numSeam

    for i in range(1,n):
        #find min from three down
        center = minPos
        minThree = minEnergyPath[i][center]

        if(center>0 and minEnergyPath[i][center-1] < minThree):
            minThree = minEnergyPath[i][center-1]
            minPos = center -1

        if(center<m-1 and minEnergyPath[i][center+1] < minThree):
            miminThree = minEnergyPath[i][center+1]
            minPos = center+1

        duplicatePixels[i][minPos] = np.inf
        seamMatrix[i][minPos] = numSeam

    return 0

@jit
def expandImage(img,duplicatePixels):
    #count number of lines to add
    numLine = 0
    for i in range(duplicatePixels.shape[1]):
        if(np.isinf(duplicatePixels[0][i])): numLine += 1
        
    newImg = np.zeros((img.shape[0],img.shape[1]+numLine,img.shape[2]),dtype=np.uint8)
    
    for i in range(img.shape[0]):
        indiceColumNewImage = 0
        for j in range(img.shape[1]):
            newImg[i][indiceColumNewImage] = img[i][j]
            indiceColumNewImage += 1
            if(np.isinf(duplicatePixels[i][j])): #add again if its repeated
                newImg[i][indiceColumNewImage] = img[i][j]
                indiceColumNewImage += 1

    return newImg

def expandImageSaving(img,seamMatrix,seamNum,N):
    global imgNum
    frame = np.zeros((img.shape[0],img.shape[1]+N,img.shape[2]),dtype=np.uint8)


    for i in range(1,seamNum):
        #count number of lines to add
        minPos = 0
        for j in range(seamMatrix.shape[1]):
            if(seamMatrix[0][j] == i):
                minPos = j
                break

        #print(minPos)
            
        newImg = np.zeros((img.shape[0],img.shape[1]+1,img.shape[2]),dtype=np.uint8)
        newSeamMatrix= np.zeros((img.shape[0],img.shape[1]+1),dtype=np.uint8)

        #expand img line
        line = np.zeros((img.shape[1]+1,3),dtype=np.uint8)
        line[0:minPos] = img[0][0:minPos]
        line[minPos] = img[0][minPos]
        line[minPos+1] = img[0][minPos]
        line[minPos+2:img.shape[1]+1] = img[0][minPos+1:img.shape[1]]
        newImg[0] = line

        line = np.zeros(seamMatrix.shape[1]+1)
        line[0:minPos] = seamMatrix[0][0:minPos]
        line[minPos] = seamMatrix[0][minPos]
        line[minPos+1] = seamMatrix[0][minPos]
        line[minPos+2:seamMatrix.shape[1]+1] = seamMatrix[0][minPos+1:seamMatrix.shape[1]]
        newSeamMatrix[0] = line

        n = img.shape[0]

        for j in range(1,n):
            #find min from three down
            if(minPos-1 >= 0 and seamMatrix[j][minPos-1] == i):
                minPos = minPos-1
            elif(minPos+1 <= seamMatrix.shape[1]-1 and seamMatrix[j][minPos+1] == i):
                minPos = minPos+1

            line = np.zeros((img.shape[1]+1,3),dtype=np.uint8)
            line[0:minPos] = img[j][0:minPos]
            line[minPos] = img[j][minPos]
            line[minPos+1] = img[j][minPos]
            line[minPos+2:img.shape[1]+1] = img[j][minPos+1:img.shape[1]]
            newImg[j] = line

            line = np.zeros(seamMatrix.shape[1]+1)
            line[0:minPos] = seamMatrix[j][0:minPos]
            line[minPos] = seamMatrix[j][minPos]
            line[minPos+1] = seamMatrix[j][minPos]
            line[minPos+2:seamMatrix.shape[1]+1] = seamMatrix[j][minPos+1:seamMatrix.shape[1]]
            newSeamMatrix[j] = line

        #save image
        frame *= 0 

        img = np.copy(newImg)

        newImg[np.where(newSeamMatrix > i)] = (0,0,255)
        frame[:newImg.shape[0],:newImg.shape[1],:] = newImg
        imageio.imsave(archiveName(imgNum),frame)
        imgNum += 1

        seamMatrix = newSeamMatrix

    return newImg

def insertNseams(img,N):
    global imgNum
    frame = np.zeros((img.shape[0],img.shape[1]+N,img.shape[2]),dtype=np.uint8)

    #saves initial image
    frame[:img.shape[0],:img.shape[1],:] = img
    imageio.imsave(archiveName(imgNum),frame)
    imgNum += 1

    duplicatePixels = np.zeros((img.shape[0],img.shape[1])) # saves pixels that will be duplicated
    seamMatrix = np.zeros((img.shape[0],img.shape[1]))
    seamNum = 1

    numSeamsInserted = 0
    
    while(numSeamsInserted < N):
        print ('inserting seam ',numSeamsInserted+1, ' of ', N, end="\r")
        minEnergyPath = calculateMinEnergyPath(edgeImg(img)+duplicatePixels)
        if(findInsertSeam(img,duplicatePixels,minEnergyPath,seamNum,seamMatrix) == 1):
            img = expandImageSaving(img,seamMatrix,seamNum,N)
            seamNum = 1
            duplicatePixels = np.zeros((img.shape[0],img.shape[1]))
            seamMatrix = np.zeros((img.shape[0],img.shape[1])) 
            continue
        else:
            #saves image
            frame *= 0 
            newImg = np.copy(img)
            newImg[np.where(np.isinf(duplicatePixels))] = (0,0,255)
            frame[:newImg.shape[0],:newImg.shape[1],:] = newImg
            imageio.imsave(archiveName(imgNum),frame)
            imgNum += 1

            seamNum += 1
            numSeamsInserted += 1

    newImg = expandImageSaving(img,seamMatrix,seamNum,N)
    seamNum = 1
    return newImg

os.system("mkdir tmpFrames")

'''
#removal
img = imageio.imread('imgs/paris.jpg')

numRemoval = 200
newImg = removeNSeams(img,numRemoval)
'''
img = imageio.imread('imgs/lake.jpg')


newImg = insertNseams(img,50)



os.system("ffmpeg -framerate 12 -i tmpFrames/%03d.png output.mp4")
#os.system("ffmpeg -r 1 -i tmpFrames/%03d.png -vcodec mpeg4 -y movie.mp4")

#os.system("rm -r tmpFrames")