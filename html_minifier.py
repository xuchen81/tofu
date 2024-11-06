from bs4 import BeautifulSoup
from utils import int_to_base62


def clean_html(html: str) -> tuple:
    soup = BeautifulSoup(html, 'html.parser')

    body = soup.find('body')
    if body is None:
        return '', []

    for link in body.find_all('link'):
        if link.get('rel') == ['stylesheet']:
            link.decompose()

    for script in body.find_all('script'):
        script.decompose()

    for style in body.find_all('style'):
        style.decompose()

    id_and_class_names = []
    for tag in body.find_all(True):
        if 'class' in tag.attrs:
            id_and_class_names.extend(tag['class'])
        if 'id' in tag.attrs:
            id_and_class_names.append(tag['id'])

    if 'class' in body.attrs:
        id_and_class_names.extend(body['class'])
    if 'id' in body.attrs:
        id_and_class_names.append(body['id'])

    for tag in body.find_all(True):
        attrs = {key: tag[key] for key in tag.attrs if key in ['id', 'class']}

        if tag.name == 'a':
            attrs['href'] = tag.get('href')

        tag.attrs = attrs

    body.attrs = {key: body[key]
                  for key in body.attrs if key in ['id', 'class']}

    idClassSet = set(id_and_class_names)
    compress_mapping = {name: int_to_base62(
        index) for index, name in enumerate(idClassSet)}

    for tag in body.find_all(True):  # True means all tags
        if 'class' in tag.attrs:
            tag['class'] = [compress_mapping[class_name]
                            for class_name in tag['class']]
        if 'id' in tag.attrs:
            tag['id'] = compress_mapping[tag['id']]

    if 'class' in body.attrs:
        body['class'] = [compress_mapping[class_name]
                         for class_name in body['class']]
    if 'id' in body.attrs:
        body['id'] = compress_mapping[body['id']]

    for element in body.find_all(text=True):
        if element.parent.name not in ['script', 'style']:
            element.replace_with(element.strip())

    for tag in body.find_all(True):
        if not tag.get_text(strip=True):
            tag.decompose()

    minified_html = str(body).replace('\n', '').replace('> <', '><')

    return str(minified_html), compress_mapping
