"""
(08/04/2026)
Assignment 27: Image Filter Lab (OpenCV)

This program demonstrates basic image filtering operations:
1. Grayscale conversion
2. Gaussian Blur
3. Canny Edge Detection

It displays original and processed images side-by-side and allows the user
to control blur intensity and edge thresholds.
"""

import os
import cv2
import matplotlib.pyplot as plt


def load_image(image_path):
	"""Load an image from disk with error handling."""
	if not os.path.exists(image_path):
		print("\n[ERROR] Image file not found.")
		print(f"Given path: {image_path}")
		return None

	image = cv2.imread(image_path)
	if image is None:
		print("\n[ERROR] OpenCV could not read the image.")
		print("The file may be corrupted or unsupported.")
		return None

	return image


def get_user_parameters():
	"""Read blur kernel size and Canny thresholds from the user."""
	print("\nEnter filter settings (press Enter to use defaults).")

	blur_input = input("Gaussian blur kernel size (odd number, default 5): ").strip()
	t1_input = input("Canny threshold 1 (default 100): ").strip()
	t2_input = input("Canny threshold 2 (default 200): ").strip()

	# Defaults
	kernel_size = 5
	threshold1 = 100
	threshold2 = 200

	# Parse kernel size
	if blur_input:
		try:
			kernel_size = int(blur_input)
			if kernel_size < 1:
				kernel_size = 5
			# Gaussian kernel size should be odd. If even, make it odd.
			if kernel_size % 2 == 0:
				kernel_size += 1
		except ValueError:
			kernel_size = 5

	# Parse Canny threshold 1
	if t1_input:
		try:
			threshold1 = int(t1_input)
			if threshold1 < 0:
				threshold1 = 100
		except ValueError:
			threshold1 = 100

	# Parse Canny threshold 2
	if t2_input:
		try:
			threshold2 = int(t2_input)
			if threshold2 < 0:
				threshold2 = 200
		except ValueError:
			threshold2 = 200

	# Ensure threshold1 <= threshold2 for stable edge behavior.
	if threshold1 > threshold2:
		threshold1, threshold2 = threshold2, threshold1

	return kernel_size, threshold1, threshold2


def apply_filters(image, kernel_size, threshold1, threshold2):
	"""Apply grayscale, Gaussian blur, and Canny edge detection."""
	grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(grayscale, (kernel_size, kernel_size), 0)
	edges = cv2.Canny(blurred, threshold1, threshold2)

	return grayscale, blurred, edges


def print_shapes(original, grayscale, blurred, edges):
	"""Print shapes before and after processing."""
	print("\n" + "=" * 74)
	print("IMAGE SHAPES")
	print("=" * 74)
	print(f"Original image shape   : {original.shape} (Height, Width, Channels)")
	print(f"Grayscale shape        : {grayscale.shape} (Height, Width)")
	print(f"Blurred shape          : {blurred.shape} (Height, Width)")
	print(f"Edges shape            : {edges.shape} (Height, Width)")


def show_results(original, grayscale, blurred, edges, kernel_size, threshold1, threshold2):
	"""Display original and processed images side-by-side using matplotlib."""
	# Convert BGR to RGB for correct display in matplotlib.
	original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

	plt.figure(figsize=(16, 4))

	plt.subplot(1, 4, 1)
	plt.imshow(original_rgb)
	plt.title("Original")
	plt.axis("off")

	plt.subplot(1, 4, 2)
	plt.imshow(grayscale, cmap="gray")
	plt.title("Grayscale")
	plt.axis("off")

	plt.subplot(1, 4, 3)
	plt.imshow(blurred, cmap="gray")
	plt.title(f"Gaussian Blur\nKernel: {kernel_size}x{kernel_size}")
	plt.axis("off")

	plt.subplot(1, 4, 4)
	plt.imshow(edges, cmap="gray")
	plt.title(f"Canny Edges\nT1={threshold1}, T2={threshold2}")
	plt.axis("off")

	plt.tight_layout()
	plt.show()


def print_explanation(kernel_size, threshold1, threshold2):
	"""Print assignment explanation after running filters."""
	print("\n" + "=" * 74)
	print("EXPLANATION")
	print("=" * 74)

	print("\n1. Grayscale Conversion")
	print("- Converts color image into one intensity channel.")
	print("- Simplifies processing and is useful before edge detection.")

	print("\n2. Gaussian Blur")
	print(f"- Applied using kernel size {kernel_size}x{kernel_size}.")
	print("- A larger kernel gives stronger blur and removes more noise.")
	print("- Kernel size should be odd (3, 5, 7, ...).")

	print("\n3. Canny Edge Detection")
	print(f"- Used thresholds: threshold1={threshold1}, threshold2={threshold2}.")
	print("- Lower threshold finds weak edges; higher threshold keeps strong edges.")
	print("- Helps highlight object boundaries in images.")

	print("\nDifference Between Original and Processed Images")
	print("- Original: full color information.")
	print("- Grayscale: intensity-only version.")
	print("- Blurred: smoother image with reduced noise/details.")
	print("- Edges: only strong boundary lines are highlighted.")

	print("\nApplications of Image Filtering")
	print("- Image preprocessing for AI/computer vision tasks.")
	print("- Medical imaging to enhance structures and boundaries.")
	print("- Object detection, face detection, and robotic vision.")
	print("- Security and surveillance video analysis.")

	print("\nSummary")
	print("This lab shows how filters transform an image for analysis.")
	print("Grayscale reduces complexity, blur removes noise, and Canny extracts edges.")
	print("These steps are foundational in many real-world vision pipelines.")


def main():
	"""Main driver function."""
	print("=" * 74)
	print("ASSIGNMENT 27: IMAGE FILTER LAB")
	print("=" * 74)

	image_path = input("Enter image path (example: sample.jpg): ").strip()
	if not image_path:
		image_path = "sample.jpg"
		print("No path entered. Using default: sample.jpg")

	image = load_image(image_path)
	if image is None:
		return

	kernel_size, threshold1, threshold2 = get_user_parameters()

	grayscale, blurred, edges = apply_filters(
		image, kernel_size, threshold1, threshold2
	)

	print_shapes(image, grayscale, blurred, edges)
	show_results(image, grayscale, blurred, edges, kernel_size, threshold1, threshold2)
	print_explanation(kernel_size, threshold1, threshold2)


if __name__ == "__main__":
	main()
