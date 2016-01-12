# Quick introduction to OpenCV with Python

## CamShift

A simple object tracking example using the **CamShift** algorithm to track motion.

- This example track an object based on its color histogram, in 1 dimension (using Hue only)
- The example also includes the detection based on 2 dimensions (using Hue and Saturation)

It is a basic demonstration of object tracking, which you may find has a few caveats, since it is based only on color:
It does not work well on black objects or objects with many colors, or if there are similarly colored features in the background.
To build a more robust object tracking system, look into keypoint detection and object descriptors like
Moments, HuMoments etc... and compute homographies between frames to match the keypoints.

## Face detection

A basic face detection example using the Haar Cascades model.

This example makes used of a pre-trained classifier named Haar Cascades. 
There are several pre-trained models available in the OpenCV distribution to detect:
- faces
- profiles
- eyes 
- eyeglasses
- left or right eye
- smile, 
- full body
- licence plates
...

Check the different files available in you OpenCV folder.

The example includes detection of faces, then within the face, detection of eyes.
Face profile is also included (commented out): the model works for left facign profiles, so in order to detect right facing profiles the image needs to be flipped.

## Credits

- These examples are from the OpenCV documentation at [http://docs.opencv.org/](http://docs.opencv.org/)
and inspired by the blog by Adrian at [PyImageSearch.com](https://PyImageSearch.com)

- I highly recommend you check out his blog, register for his free course on OpenCV which is both fun and educational, and maybe even buy his book.

## Tips and tricks

- The OpenCV library is a C++ library. While all the functions are available in Python through the bindings, the documentation is not nearly as good as the C++ documentation. 
Most of the example are in C++, but they should easily translate into Python. 

- Make sure to check the documentation for your version of OpenCV: there are many breaking changes between v2.4 and v3.1

- If all fails, check the function signature in your favorite editor.