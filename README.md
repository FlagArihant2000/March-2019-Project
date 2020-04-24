1. CircleRecognizer.py - The program takes a photo as an input and identifies the circle that is present in the image.

2. PreRecordedASL.py - The program basically identifies the ASL (American Sign Language) digits in a pre-recorded video.

3. Live.py - The program identifies the ASL digits when appropriate gestures are made towards the webcam.

This whole repository was made during the months of February and March, 2019. The main task was detection of the digits in American Sign Language. 

This was a project done for selection to Technoseason 1 Image Processing Task for IvLabs. Basically, we had to make a program that is able to take the input hand gestures as our input and give its equivalent meaning in terms of American Sign Language Digits. There are various approaches to tackle this problem, however I went through a more traditional route. The image was taken, converted to HSV in order to perform color thresholding of the skin. The contour was obtained and convex hull was performed in order to find the defects in the contour. Those defects were filtered using different equations and constraints. In order to make the corners more sharp, the hand was eroded in order to find the distinct points. The code was written in python3. This solution made our team stand second in the Technoseason Recruitment Drive.


