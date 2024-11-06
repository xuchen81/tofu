import os

from utils import read_file, get_personalize_text_template
from openai import OpenAI
import json
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=API_KEY)


def summarize_company_info():
    system_prompt = read_file('./prompts/system_company_summary.txt')
    company_info = read_file("./tests/company_info.json")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": company_info}
    ]

    print(messages)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
    )

    # print(json.dumps(response.to_dict(), indent=2))
    # print(response.choices[0].message.content)
    response_dict = json.loads(response.choices[0].message.content)
    print(response_dict)
    return response_dict


def personalize_text(user_input):
    system_prompt = read_file('./prompts/personalize_text.txt')
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
    )

    # print(json.dumps(response.to_dict(), indent=2))
    # print(response.choices[0].message.content)
    response_dict = json.loads(response.choices[0].message.content)
    print(response_dict)
    return response_dict


def test():
    company_info = summarize_company_info()
    personlize_prompt = read_file("./prompts/personalize_text.txt")

    target_info_text = read_file("./tests/target.json")

    # target info object
    target_info = json.loads(target_info_text)

    for key in target_info.keys():
        if key in ["Industries", "Personas"]:
            for subkey in target_info[key].keys():
                target_audience_info = {
                    "audience_name": subkey,
                    "audience_info": target_info[key][subkey]
                }
                print(target_audience_info)
                print("=" * 10)
                user_input = get_personalize_text_template(
                    read_file("./prompts/input.txt"), json.dumps(company_info), json.dumps(target_audience_info), "preparing for a recession toolkit")
                print(user_input)
                personalize_text(user_input)

    # print(target_info)

    # print(company_info)
    # print(personlize_prompt)
    # print(user_input)
    # target_info = read_file("./test_json/target.json")
    # print("-" * 10)
    # print(target_info)


# testAi()
# summarize_company_info()
test()
