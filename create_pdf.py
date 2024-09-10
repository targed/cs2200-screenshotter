from PIL import Image
import os

def images_to_pdf(image_folder, output_pdf):
    # Get all image files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    image_files.sort()  # Sort the files to maintain order

    # Open the images and convert them to RGB
    images = [Image.open(os.path.join(image_folder, file)).convert('RGB') for file in image_files]

    # Save the images as a single PDF
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF created successfully: {output_pdf}")
    else:
        print("No images found in the folder.")

if __name__ == "__main__":
    image_folder = 'screenshots'  # Folder containing the images
    output_pdf = 'output.pdf'     # Output PDF file name

    images_to_pdf(image_folder, output_pdf)