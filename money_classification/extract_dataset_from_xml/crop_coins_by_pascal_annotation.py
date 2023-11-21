import cv2
import os
import xml.etree.ElementTree as ET

def crop_coins_by_pascal_annotation(xml_path, image_path, output_path, image_ext='.jpeg'):
    """
    Crop coins from image by pascal annotation
    xml_path: path to xml file
    image_path: path to image file
    output_path: path to output folder
    """
    # Read image
    image = cv2.imread(image_path)
    # Read xml file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # Get image name
    image_name = root.find('filename').text
    # Get image size
    image_size = root.find('size')
    image_width = int(image_size.find('width').text)
    image_height = int(image_size.find('height').text)
    # Get objects
    counter = 0
    objects = root.findall('object')
    for obj in objects:
        
        # Get object name
        name = obj.find('name').text
        # Get bounding box
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        # Crop coin
        coin = image[ymin:ymax, xmin:xmax]
        # Save coin
        coin_name = image_name.replace(image_ext, f'_{counter}{image_ext}')
        counter += 1
        coin_path = os.path.join(output_path, coin_name)
        cv2.imwrite(coin_path, coin)
        print('Saved {}'.format(coin_name))

if __name__ == '__main__':
    # # Path to xml file
    # xml_path = './tf_data/labels/test (1).xml'
    # # Path to image file
    # image_path = './tf_data/images/test (1).jpeg'
    # # Path to output folder
    # output_path = './classification_data/images'
    xml_path = './tf_data/labels/'
    # Path to image file
    image_path = './tf_data/images/'
    # Path to output folder
    output_path = './classification_data/images'
    #image ext
    image_ext='.jpeg'

    for file in os.listdir(xml_path):
        if file.endswith('.xml'):
            # Get xml file path
            xml_file = os.path.join(xml_path, file)
            # Get image file path
            image_file = os.path.join(image_path, file.replace('.xml', image_ext))
            # Crop coins
            crop_coins_by_pascal_annotation(xml_file, image_file, output_path)
    # # Crop coins
    # crop_coins_by_pascal_annotation(xml_path, image_path, output_path)