# -*- coding: utf-8 -*-
"""Untitled

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14DP3pjTWBQodbPW91zHsbntYSSw6DIGu
"""

#Image Steganography

#Import all these necessary python libraries
import cv2 #library which focus on image processing, video capture and analysis
import numpy as np #Python lb used for working with arrays
import types # define name for some obj used by python interpreter 

# for image display
from google.colab.patches import cv2_imshow

#function to convert data to binary further used for encoding and decoding
def messageToBin(msg):
  if type(msg) == str:
    return ''.join([ format(ord(i), "08b") for i in msg ])
  elif type(msg) == bytes or type(msg) == np.ndarray:
    return [ format(i, "08b") for i in msg ]
  elif type(msg) == int or type(msg) == np.uint8:
    return format(msg, "08b")
  else:
    raise TypeError("Wrong Input type")

#Function to hide the secret data or msg into the image by modyfing the LSB (least significant bit )
def hideData(image, secret_message):

  # calculate the maximum bytes to encode 
  n_bytes = image.shape[0] * image.shape[1] * 3 // 8
  print("Max bytes to encode:", n_bytes)

  #Check if the number of bytes to encode is less than the maximum bytes in the image
  if len(secret_message) > n_bytes:
      raise ValueError("Insufficient image bytes!!")
  
  secret_message += ";;;;;" # you can use any string as the delimeter

  data_index = 0
  # convert input data to binary format using messageToBin() fucntion
  binary_secret_msg = messageToBin(secret_message)

  data_len = len(binary_secret_msg) #Find the length of data that needs to be hidden

  for values in image:
      for pixel in values:
        # converting red,green,blue(RGB values) to binary format
          r, g, b = messageToBin(pixel)
          
          if data_index < data_len:
              # hide the data into least significant bit of red, green and blue pixel
              pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1

          if data_index < data_len:
              pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1

          if data_index < data_len:
              pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          # If data is encoded successfully, break the loop
          if data_index >= data_len:
              break

  return image  

def showData(image):
  binary_data = ""
  for values in image:
      for pixel in values:
        # red green blue values to binary format
          r, g, b = messageToBin(pixel) 
          binary_data += r[-1] #extracting data from the least significant bit of red pixel
          binary_data += g[-1] #extracting data from the least significant bit of green pixel
          binary_data += b[-1] #extracting data from the least significant bit of blue pixel

 
  all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
  # convert from bits to characters
  decoded_data = ""
  for byte in all_bytes:
      decoded_data += chr(int(byte, 2))
      if decoded_data[-5:] == ";;;;;": #check if we have reached the delimeter which is ";;;;;"
          break
  # remove delimeter to show hidden secret msg
  return decoded_data[:-5] 

# Encode data into image 
def encode_text(): 
  image_name = input("Enter image name ") 

  # Read input image 
  image = cv2.imread(image_name)
   
  #info of the image
  # check shape of image for calculating  number of bits
  print("The shape of the image is: ",image.shape) 
  print("The original image is as shown below: ")
  resized_image = cv2.resize(image, (500, 500))
  cv2_imshow(resized_image) #display the image
  
      
  data = input("Enter your secret message  :") 
  if (len(data) == 0): 
    raise ValueError('Empty data')
  
  filename = input("Enter the name of new encoded image: ")

  #hide secret msg into the image 
  encoded_image = hideData(image, data) 
  cv2.imwrite(filename, encoded_image)


# decoding data from imagee
def decode_text():
  
  image_name = input("Enter the name of the image (i.e Steganographed) that you want to decode  :") 
  # read the image
  image = cv2.imread(image_name)  

  print("The Steganographed image is as shown below: ")
  resized_image = cv2.resize(image, (500, 500)) 
  cv2_imshow(resized_image) #display the Steganographed image
    
  text = showData(image)
  return text

def main(): 
    a = input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Choose here: ")
    userinput = int(a)
    if (userinput == 1):
      print("\nEncoding the secret....")
      encode_text() 
          
    elif (userinput == 2):
      print("\nDecoding the secret....") 
      print("Decoded message is " + decode_text()) 
    else: 
        raise Exception("Wrong input!! Enter correct one") 
          
main()