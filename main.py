import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def extract_palette(image_path, num_colors=5):
    # Load image with OpenCV
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Resize for faster processing
    img = cv2.resize(img, (200, 200))

    # Reshape image to a list of pixels
    pixels = img.reshape((-1, 3))

    # Run KMeans clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get dominant colors
    colors = np.round(kmeans.cluster_centers_).astype(int)

    return colors

def display_palette(colors):
    # Create a palette strip image
    palette = np.zeros((50, len(colors) * 100, 3), dtype=np.uint8)

    for i, color in enumerate(colors):
        palette[:, i*100:(i+1)*100, :] = color

    # Show using OpenCV
    cv2.imshow('Color Palette', cv2.cvtColor(palette, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Print HEX codes
    hex_codes = ['#%02x%02x%02x' % tuple(color) for color in colors]
    print("Palette HEX codes:", hex_codes)

# ==== Run ====
if __name__ == "__main__":
    image_path = "input.jpg"
    colors = extract_palette(image_path, num_colors=5)
    display_palette(colors)
