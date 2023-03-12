from django.conf import settings
import openai
import time

def create_keywords_string(keywords):
    keywords_string = ''
    for keyword in keywords:
        keywords_string = keywords_string + ' ' + keyword + ','
    return keywords_string

def clean_gpt_response(text):
    text = text[4:]
    return text

def string_title_validation(string):
    if string[0] == '"' and string[-1] == '"':
        clean_string = string[1:-1]
        return clean_string
    else:
        return string

class ChatGPT:
    def __init__(self):
        openai.api_key = settings.CHAT_GPT_KEY
    
    def write_product_description(self, model, product_title, product_description, keywords):
        prompt = 'write a product description using these keywords "'+ keywords +'" for a '+ product_title + 'with these features: ' + product_description
        print(prompt)
        response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=0.7,
                max_tokens=512,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
        )
        return response['choices'][0]['text'].strip()


    def write_product_title(self, product_title, category):
        prompt = 'Rewrite this headline' + product_title + 'in a SEO optimized way using keywords common in ' + category + ' product categories and avoid words: "Men", "men", "Woman", "woman"'
        response = openai.Completion.create(
                model='text-davinci-003',
                prompt=prompt,
                temperature=0.7,
                max_tokens=128,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
        )

        title = string_title_validation(response['choices'][0]['text'].strip())
        return title

    
    def gpt35_write_product_description(self, product_title, product_description, keywords, max_words, min_words):
        print(product_description)
        print('gpt product descrp')
        message_1 = "Write a professional product description for a " + product_title + " with these features: " + product_description
        message_2 = "A SEO optimized product description for keywords like: " + keywords
        message_3 = "The description must not contain the title of the product"
        message_4 = "max " + str(max_words) +" words, min " + str(min_words) + " words"
        message_5 = "Avoid introduction, just describe the product "
        
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages=[
                      {"role": "system", "content": "You are a product description writer"},
                      {"role": "user", "content": message_1},
                      {"role": "user", "content": message_2},
                      {"role": "user", "content": message_3},
                      {"role": "assistant", "content": 'Ok, how many words?'},
                      {"role": "user", "content":message_4},
                  ])
        print(response)
        time.sleep(5)
        return response['choices'][0]['message']['content']


    def gpt35_write_product_title(self, product_title, category):
        message_1 = "Write just one product headline for a " + product_title
        message_2 = "A SEO optimized product title for keywords commons in this category product: " + category
        message_3 = 'max 60, avoid words like "Men", "men", "Woman", "woman"'

        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages=[
                      {"role": "system", "content": "You are a product title writer"},
                      {"role": "user", "content": message_1},
                      {"role": "user", "content": message_2},
                      {"role": "assistant", "content": 'Ok, how many characters?'},
                      {"role": "user", "content":message_3},
                  ])
        print(response)
        return response['choices'][0]['message']['content']


    def answer_question(self, question):
        response = openai.Completion.create(
                model='text-davinci-003',
                prompt=question,
                temperature=0.7,
                max_tokens=128,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
        )

        answer = response['choices'][0]['text']
        return answer