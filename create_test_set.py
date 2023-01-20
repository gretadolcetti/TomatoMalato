# For each calss in Dataset randomly select 10% of the images and move them to test set
# inside test dir 

import os
import random
import shutil

dataset_dir = 'Dataset/train'
test_dir = 'test'

# Create test dir
if not os.path.exists(test_dir):
    os.mkdir(test_dir)

# Create test set for each class
for class_dir in os.listdir(dataset_dir):
    if class_dir == '.DS_Store':
        continue
    # Create test class dir
    test_class_dir = os.path.join(test_dir, class_dir)
    if not os.path.exists(test_class_dir):
        os.mkdir(test_class_dir)

    # Get all images in class
    images = os.listdir(os.path.join(dataset_dir, class_dir))

    # Select 10% of images and move them to test set
    for image in random.sample(images, int(len(images) * 0.1)):
        shutil.move(os.path.join(dataset_dir, class_dir, image), test_class_dir)

