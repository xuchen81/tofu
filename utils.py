def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def get_personalize_text_template(template_text, company_info, target_info, text):
    personalized_text = template_text.replace("{{company_info}}", company_info)
    personalized_text = personalized_text.replace(
        "{{target_info}}", target_info)
    personalized_text = personalized_text.replace("{{text}}", text)
    return personalized_text
