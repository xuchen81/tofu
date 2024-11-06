import os

from utils import read_file, write_to_file, get_personalize_text_template
from openai import OpenAI
import json
from dotenv import load_dotenv
from html_minifier import clean_html


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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
    )

    # print(json.dumps(response.to_dict(), indent=2))
    # print(response.choices[0].message.content)
    response_dict = json.loads(response.choices[0].message.content)
    return response_dict


def personalize_text(user_input):
    system_prompt = read_file('./prompts/personalize_text_v2.txt')
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
    print("chat messages:")
    print(messages)
    print("\n")
    print("Results:")
    print("=======" * 20)
    print(response_dict)
    print("=======" * 20)
    return response_dict


def scrape_website():
    content = read_file("./scraper/page.html")
    cleaned, classNames = clean_html(content)
    write_to_file('./scraper/clean_page.html', cleaned)


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


def test_v2():
    to_personalize = {
        "company_slogo": "Preparing for a recession toolkit",
        "company_short_description": "A recession readiness toolkit to guide CFOs and finance leaders through recessions and periods of economic instability.",
        "book_slogo": "2022 CFO Recession Toolkit",
        "book_overview": "Managers are dealing with a number of economic issues, and some analysts believe that the US is headed toward a recession. To respond to the challenge, take action to address a possible recession now, so that you're ready to minimize the impact and outperform competitors who are not proactive."
    }
    company_info = summarize_company_info()
    personlize_prompt = read_file("./prompts/personalize_text_v2.txt")

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
                user_input = get_personalize_text_template(
                    read_file("./prompts/input.txt"), json.dumps(company_info), json.dumps(target_audience_info), json.dumps(to_personalize))
                personalize_text(user_input)


# testAi()
# summarize_company_info()
test_v2()
# scrape_website()
