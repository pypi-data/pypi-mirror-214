# Image Converter GUI APP for Arduino oled display ssd1306 128x64
## About Project
Application has been created in order to easy convert images into your <strong>Arduino</strong> project with <strong>oled displays</strong>
### How does it work:
While you open .png and .jpg (others extensions in the future) image in app, the algorithm convert it to hexdeicmal array. Then it             returns full     code, ready to copy and put into the Arduino IDE. You can also preview how image will you like on your dislplay
## Demo
 <p align="center">
<img src="https://user-images.githubusercontent.com/123249470/232137289-ff2707a7-a4bf-4e55-88a5-a469f54c3c3d.gif" width="350" height="560">
</p>

## Getting Started
### Prerequisites
Download python, pip and check version
```
$ pip3 --version 
$ python --version
```
### Installation
#### Windows/Linux/Mac OS:
```
$ pip3 install image-to-arduino
```
### Run
#### Windows/Linux/Mac OS:
```
$ image-to-arduino
```
### How to upgrade version
#### Windows/Linux/Mac OS:
```
$ pip3 install --upgrade image-to-arduino
```
## How to connect display to Arduino

<p align="center">
      <img src="https://user-images.githubusercontent.com/123249470/233432819-97b593ab-d380-4945-85ab-543dbb49921b.png" width="620" height="480">
</p>

<strong>IMPORTANT:</strong> If you have Arduino board with inputs SCK and SDA, use them instead of A4 and A5 inputs

## How to Contribute
1. Fork the Project
2. Clone repo with your GitHub username instead of ```YOUR-USERNAME```:<br>
```
$ git clone https://github.com/YOUR-USERNAME/Image_Converter_App 
```
3. Create new branch:<br>
```
$ git branch BRANCH-NAME 
$ git checkout BRANCH-NAME
```
4. Make changes and test<br>
5. Submit Pull Request with comprehensive description of change

## Task list
* add more than one display size<br>
* make icon of the app<br>
* make app as .exe <br>
* fix issue with generating dark png images with trancparency
* resize window (width)
* optimize gif extension option (or remove it)
* test software
* <del> reverse color of image </del><br>
* <del> create function which generate full arduino code(not only arduino array) and connect it to switch button</del>
* <del> show preview of an image </del> <br>
* <del> upgrade graphics and style </del><br>
* <del> add more functions </del><br>
## What I have learned
*	tkinter library skills 
*	basics of UX and GUI
*	image processing 
## Used libraries
* tkinter 
* customtkinter
* openCV
* numpy
## License 
[MIT license](LICENSE)
