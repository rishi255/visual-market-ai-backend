
import os
from google.cloud import vision
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()
KEYDIR_PATH = os.getenv('KEYDIR_PATH')
credentials = service_account.Credentials.from_service_account_file(KEYDIR_PATH)
client = vision.ImageAnnotatorClient(credentials=credentials)

def detect_objects(image_path: str):
    """
    Detects object entities by choosing the object with greatest confidence of being true.

    Args:
        image_path (str): Path to image file.
    
    Returns:
        objects: Annotated image object of image given by path.
    """
    image_file = open(file=image_path, mode='rb')
    content = image_file.read()
    image = vision.Image(content=content)
    objects = client.object_localization(image=image).localized_object_annotations

    print(type(objects))
    print(f'Number of objects found: {len(objects)}')
    for object_ in objects:
        print(f'\n{object_.name} (confidence: {object_.score})')
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(f' - ({vertex.x}, {vertex.y})')

    return objects

def detect_logos(image_path: str):
    """
    Detect logos from images.

    Args:
        image_path (str): Path to image file.

    Returns:
        object: 
    """

    image_file = open(file=image_path, mode='rb')
    content = image_file.read()
    image = vision.Image(content=content)
    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    
    print(type(response))
    print('Logos:')
    for logo in logos:
        print(logo.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return logos

if __name__ == '__main__':
    print('-' * 100)
    image_path = './data/fruits.png'
    objects = detect_objects(image_path=image_path)

    print('-' * 100)
    image_path = './data/logo-collage.png'
    logos = detect_logos(image_path=image_path)
