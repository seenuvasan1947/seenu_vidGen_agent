import os

class ImageAgent:
    def get_image_folder(self):
        while True:
            folder = input("Enter the folder path containing your images: ")
            if os.path.isdir(folder):
                image_files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
                if image_files:
                    return [os.path.join(folder, f) for f in image_files]
                else:
                    print("No image files found in the specified folder. Please try again.")
            else:
                print("Invalid folder path. Please try again.")