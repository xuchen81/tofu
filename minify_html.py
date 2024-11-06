from bs4 import BeautifulSoup
from utils import int_to_base62


def clean_html(html: str) -> tuple:
    soup = BeautifulSoup(html, 'html.parser')

    # Keep only the body content
    body = soup.find('body')
    if body is None:
        return '', []

    # Remove all <link> tags for CSS
    for link in body.find_all('link'):
        if link.get('rel') == ['stylesheet']:
            link.decompose()

    # Remove all <script> tags
    for script in body.find_all('script'):
        script.decompose()

    # Remove all <style> tags
    for style in body.find_all('style'):
        style.decompose()

    # Get all class names and id values in the page
    id_and_class_names = []
    for tag in body.find_all(True):
        if 'class' in tag.attrs:
            id_and_class_names.extend(tag['class'])
        if 'id' in tag.attrs:
            id_and_class_names.append(tag['id'])

    # Include body tag class names and id values
    if 'class' in body.attrs:
        id_and_class_names.extend(body['class'])
    if 'id' in body.attrs:
        id_and_class_names.append(body['id'])

    # Loop through all nodes and keep only the required attributes
    for tag in body.find_all(True):
        # Keep only id and class attributes
        attrs = {key: tag[key] for key in tag.attrs if key in ['id', 'class']}

        # For <a> tags, keep href as well
        if tag.name == 'a':
            attrs['href'] = tag.get('href')

        # Set the new attributes
        tag.attrs = attrs

    # Keep only id and class attributes for body tag
    body.attrs = {key: body[key]
                  for key in body.attrs if key in ['id', 'class']}

    idClassSet = set(id_and_class_names)
    compress_mapping = {name: int_to_base62(
        index) for index, name in enumerate(idClassSet)}

    # Replace class names and id values with compressed values
    for tag in body.find_all(True):  # True means all tags
        if 'class' in tag.attrs:
            tag['class'] = [compress_mapping[class_name]
                            for class_name in tag['class']]
        if 'id' in tag.attrs:
            tag['id'] = compress_mapping[tag['id']]

    # Replace class names and id values for body tag
    if 'class' in body.attrs:
        body['class'] = [compress_mapping[class_name]
                         for class_name in body['class']]
    if 'id' in body.attrs:
        body['id'] = compress_mapping[body['id']]

    # Trim spaces at the beginning and end of text in leaf nodes
    for element in body.find_all(text=True):
        if element.parent.name not in ['script', 'style']:
            element.replace_with(element.strip())

    # Remove all nodes that have no text in them
    for tag in body.find_all(True):
        if not tag.get_text(strip=True):
            tag.decompose()

    # Remove all spaces and new lines between tags
    minified_html = str(body).replace('\n', '').replace('> <', '><')

    return str(minified_html), compress_mapping
