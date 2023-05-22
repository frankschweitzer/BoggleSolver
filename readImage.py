import cv2
import numpy as np
import pytesseract

# Load the image
image = cv2.imread("boggle_board.jpg", cv2.IMREAD_GRAYSCALE)

# Threshold the image to convert it to binary
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# Define the dimensions of the Boggle board
rows = 4
cols = 4

# Calculate the width and height of each cell in the image
cell_width = image.shape[1] // cols
cell_height = image.shape[0] // rows

# Initialize an empty 2D list for the grid
grid = [['' for _ in range(cols)] for _ in range(rows)]

# Iterate over each cell in the grid
for i in range(rows):
    for j in range(cols):
        # Extract the cell region from the binary image
        cell_image = binary_image[i*cell_height:(i+1)*cell_height, j*cell_width:(j+1)*cell_width]

        # Perform OCR using pytesseract to recognize the character in the cell
        character = pytesseract.image_to_string(cell_image, config='--psm 10')

        # Assign the character to the corresponding position in the grid
        grid[i][j] = character

# Now you have the Boggle board grid as a 2D list
print(grid)
