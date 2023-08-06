import requests


def generate_usernames(user_name, OPENAI_API_KEY, username_for=None, min_length=None, max_length=None,
                       allowed_special_characters=None,
                       lucky_number=None, interests_hobbies=None, user_name_styles=None, interested_words=None,
                       gender=None, starts_with=None, ends_with=None):
    if user_name_styles == "all":
        user_name_styles = None

    prompt_parts = [
        f"I want you to help in creating 20 different usernames",
        f"for platform {username_for} " if username_for else "",
        f"for '{user_name}'.",
        f"Length between {min_length} to {max_length} characters." if min_length and max_length else "",
        f"We can use {allowed_special_characters} special characters." if allowed_special_characters else "",
        f"We can also have {lucky_number} number in it." if lucky_number else "",
        f"User hobbies and interests are {interests_hobbies}." if interests_hobbies else "",
        f"Try to create {user_name_styles} usernames." if user_name_styles else "",
        f"We can also use {interested_words}." if interested_words else "",
        f"It will be {gender} user." if gender else "",
        f"with prefix {starts_with}." if starts_with else "",
        f"Ends with {ends_with}." if ends_with else "",
    ]

    prompt = " ".join(prompt_parts)
    generated_usernames = generate_username(prompt.strip(), OPENAI_API_KEY)
    return generated_usernames


def generate_username(prompt, OPENAI_API_KEY):
    url = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        "model": 'text-davinci-003',
        "prompt": prompt,
        "temperature": 1,
        "max_tokens": 300
    }
    # print(url, headers, data)
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        generated_usernames_str = response_data['choices'][0]['text'].strip()
        generated_usernames = clean_response(generated_usernames_str)
        return generated_usernames
    else:
        return None


def clean_response(names_string: str) -> list:
    names = names_string.split("\n")
    result_names = []
    for name in names:
        s_names = name.strip().split(".")
        if len(s_names) > 1:
            result_names.append(s_names[1].strip())
    return result_names
