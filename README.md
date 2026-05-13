# Image Matrix Processor

A lightweight, pure-Python command-line tool for performing geometric and color transformations on images by treating them as raw RGB matrices

## Features

Unlike standard libraries that handle everything behind the scenes, this project exposes the logic of image manipulation. You can:

* **Geometric Shifts**: Rotate, Scale, and Skew images with custom parameters.
* **Structural Changes**: Transpose matrices to flip orientations.
* **Filters**: Convert to Greyscale or apply Edge Detection to find high-contrast boundaries.
* **Persistent Session**: A robust **while loop interface** allows you to perform multiple transformations or process different images sequentially without restarting the script.
* **Matrix Re-rendering**: Converts modified pixel matrices back into standard image formats (e.g., `output.jpg`) using the Pillow library.

## Getting Started

### Prerequisites
You will need Python 3.x and the `Pillow` (PIL) library to handle the initial conversion from image files to matrices
