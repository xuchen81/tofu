def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def int_to_base62(num):
    base62_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if num == 0:
        return base62_chars[0]

    base62 = []
    while num > 0:
        num, rem = divmod(num, 62)
        base62.append(base62_chars[rem])

    return ''.join(reversed(base62))


def get_personalize_text_template(template_text, company_info, target_info, text):
    personalized_text = template_text.replace("{{company_info}}", company_info)
    personalized_text = personalized_text.replace(
        "{{target_info}}", target_info)
    personalized_text = personalized_text.replace("{{text}}", text)
    return personalized_text
