# Dynamic Username Generator 🚀🔢

## Introduction 📚
Welcome to the Dynamic Username Generator! This unique Python package 🐍 generates personalized and creative usernames using the power of OpenAI 🤖. Ideal for both individuals and businesses, it's the perfect tool for creating meaningful online identities.

Whether you need a username for a new social media platform, or you're a platform owner who needs a quick solution for generating usernames for your users, Dynamic Username Generator is designed to assist you.

## Installation 💻

Before you begin, ensure you have met the following requirements:

- You have installed python 3.6+ 🐍
- You have a valid OpenAI API Key 🗝️

To install Dynamic Username Generator, follow these steps:

```shell
pip install dynamic_username_generator
```

## Usage 🚀

The usage of the Dynamic Username Generator is quite straightforward. Here is a basic example:

```python
from generate_usernames import generate_usernames

usernames = generate_usernames(user_name="JohnDoe", OPENAI_API_KEY="your_api_key")
print(usernames)
```

Remember, while `user_name` and `OPENAI_API_KEY` are mandatory, the function also accepts many other parameters to customize the username generation:

- `username_for`: The platform for which the username is for
- `min_length`: Minimum length of the username
- `max_length`: Maximum length of the username
- `allowed_special_characters`: Special characters that can be included
- `lucky_number`: A favorite number that can be included
- `interests_hobbies`: User's interests and hobbies for more personalized username
- `user_name_styles`: Styles preferred by the user
- `interested_words`: Words that user is interested to include
- `gender`: User's gender
- `starts_with`: Preferred starting characters
- `ends_with`: Preferred ending characters

## Support 🤝

For any queries or support, feel free to reach out to us through our website's [contact page](https://usernamegenerator.io/contact). We'd love to hear from you!

For more great username ideas and options, visit our website at [Username Generator](https://usernamegenerator.io/).

Enjoy creating unique and personalized usernames with Dynamic Username Generator! 🚀