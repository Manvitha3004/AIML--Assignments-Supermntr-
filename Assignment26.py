"""
(06/04/2026)
Assignment 26: Image as Numbers

This beginner-friendly program shows how an image is represented as numbers.
It loads an image using OpenCV, prints image properties, extracts pixel values,
separates color channels, and explains key concepts.
"""

import os
import cv2


def load_image(image_path):
	"""Load image from path and handle missing file errors."""
	if not os.path.exists(image_path):
		print("\n[ERROR] Image file not found.")
		print(f"Path provided: {image_path}")
		print("Please check the path and try again.")
		return None

	image = cv2.imread(image_path)
	if image is None:
		print("\n[ERROR] File exists, but OpenCV could not read it as an image.")
		print("The file may be corrupted or in an unsupported format.")
		return None

	return image


def print_basic_info(image):
	"""Print shape, data type, and total number of pixels."""
	height, width, channels = image.shape
	total_pixels = height * width

	print("\n" + "=" * 72)
	print("IMAGE BASIC INFORMATION")
	print("=" * 72)
	print(f"Image Shape (H, W, C)     : {image.shape}")
	print(f"Data Type                 : {image.dtype}")
	print(f"Total Number of Pixels    : {total_pixels}")
	print(f"Total Numeric Values      : {image.size}")


def print_pixel_values(image):
	"""Print pixel values at (0,0) and center coordinate."""
	height, width, _ = image.shape

	top_left = image[0, 0]
	center_y, center_x = height // 2, width // 2
	center_pixel = image[center_y, center_x]

	print("\n" + "=" * 72)
	print("PIXEL VALUES AT SPECIFIC COORDINATES")
	print("=" * 72)
	print("Note: OpenCV stores color order as BGR (Blue, Green, Red).")
	print(f"Pixel at (0, 0)           : {top_left}  -> [B, G, R]")
	print(
		f"Pixel at center ({center_y}, {center_x}): {center_pixel}  -> [B, G, R]"
	)


def print_color_channels(image):
	"""Split and print details of Blue, Green, and Red channels."""
	blue_channel, green_channel, red_channel = cv2.split(image)

	print("\n" + "=" * 72)
	print("SEPARATE COLOR CHANNELS")
	print("=" * 72)
	print(f"Blue Channel Shape        : {blue_channel.shape}")
	print(f"Green Channel Shape       : {green_channel.shape}")
	print(f"Red Channel Shape         : {red_channel.shape}")

	# Show one sample value from each channel at top-left pixel.
	print("\nTop-left channel values at (0, 0):")
	print(f"Blue value                : {blue_channel[0, 0]}")
	print(f"Green value               : {green_channel[0, 0]}")
	print(f"Red value                 : {red_channel[0, 0]}")

	return blue_channel, green_channel, red_channel


def print_min_max_insights(image, blue_channel, green_channel, red_channel):
	"""Print min/max values and explain intensity range."""
	print("\n" + "=" * 72)
	print("PIXEL INTENSITY INSIGHTS")
	print("=" * 72)
	print(f"Overall Min Pixel Value   : {image.min()}")
	print(f"Overall Max Pixel Value   : {image.max()}")

	print("\nPer-channel min and max values:")
	print(f"Blue  Channel Min / Max   : {blue_channel.min()} / {blue_channel.max()}")
	print(f"Green Channel Min / Max   : {green_channel.min()} / {green_channel.max()}")
	print(f"Red   Channel Min / Max   : {red_channel.min()} / {red_channel.max()}")

	print("\nIntensity Range Explanation (0-255):")
	print("- 0 means no intensity (very dark for that channel).")
	print("- 255 means full intensity (very bright for that channel).")
	print("- Most standard color images use 8-bit values in this range.")


def print_concepts_and_summary():
	"""Print required explanation, applications, and summary."""
	print("\n" + "=" * 72)
	print("CONCEPT EXPLANATION")
	print("=" * 72)
	print("1. Shape (Height, Width, Channels):")
	print("   - Height: Number of rows of pixels.")
	print("   - Width: Number of columns of pixels.")
	print("   - Channels: Color components per pixel (usually 3 for color images).")

	print("\n2. Pixel Values and Intensity:")
	print("   - Every pixel is represented by numbers.")
	print("   - In color images, each pixel has values for Blue, Green, and Red.")
	print("   - Higher values mean stronger intensity for that color.")

	print("\n3. RGB Channels:")
	print("   - Red, Green, and Blue channels combine to form a full color image.")
	print("   - OpenCV loads images in BGR order by default.")

	print("\nApplications:")
	print("- Image Recognition: Detecting objects and faces.")
	print("- AI/Computer Vision: Training models for classification and detection.")
	print("- Medical Imaging: Analyzing X-rays, MRIs, and CT scans.")

	print("\nSummary:")
	print("This program demonstrates that images are numeric arrays.")
	print("By inspecting shape, data type, pixel values, and channels, we understand")
	print("how computers store and process visual data.")


def main():
	"""Main function to run the assignment program."""
	print("=" * 72)
	print("ASSIGNMENT 26: IMAGE AS NUMBERS")
	print("=" * 72)

	image_path = input("\nEnter image path (example: sample.jpg): ").strip()

	# Fallback to a default filename if user presses Enter.
	if not image_path:
		image_path = "sample.jpg"
		print("No path entered. Using default path: sample.jpg")

	image = load_image(image_path)
	if image is None:
		return

	print_basic_info(image)
	print_pixel_values(image)
	blue_channel, green_channel, red_channel = print_color_channels(image)
	print_min_max_insights(image, blue_channel, green_channel, red_channel)
	print_concepts_and_summary()


if __name__ == "__main__":
	main()
