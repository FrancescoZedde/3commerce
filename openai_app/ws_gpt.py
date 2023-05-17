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
        return response['choices'][0]['message']['content'], response['usage']['completion_tokens']


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
        return response['choices'][0]['message']['content'], response['usage']['completion_tokens']


    def answer_question(self, question, max_tokens):
        response = openai.Completion.create(
                model='text-davinci-003',
                prompt=question,
                temperature=0.7,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
        )

        answer = response['choices'][0]['text']
        return answer

    def generate_image_from_prompt(self, prompt, n_copies):
        response = openai.Image.create(
                prompt=prompt,
                n=int(n_copies),
                size="1024x1024"
        )
        print(response)
        return response['data']
    
    def generate_image_variation(self):
        response = openai.Image.create_variation(
                #prompt="add a model"
                image=open("main_app/static/images/blackdress.png", "rb"),
                n=2,
                size="1024x1024"
        )
        print(response)

    def smartcopy_write_blog_article(self, topic, target_audience, keywords, tone, word_count, language):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages = [
                {"role": "system", "content": "You are a blog article writer"},
                {"role": "user", "content": f"Write a {tone} blog article"},
                {"role": "user", "content": f"Topic: {topic}. Target Audience: {target_audience}. Keywords: {keywords}. Word Count: {str(word_count)}. Language: {language}"},
            ],
            temperature =0.7,
            max_tokens = 2000,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            
            )
        print(response)

        if len(response['choices']) >= 1:
            return response
        else:
            print(f"Error")
    
    def smartcopy_blog_ideas(self, topic, target_audience, keywords, language):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages = [
                      {"role": "system", "content": "You are a blog writer"},
                      {"role": "user", "content": "Make a list of 15 blog article ideas" },
                      {"role": "user", "content": "Topic: " + topic + ". Target Audience: " + target_audience + ". Keywords: " + keywords  + ". Language: " + language},
                    ],
            temperature =0.7,
            max_tokens = 2000,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            
            )
        print(response)

        if len(response['choices']) >= 1:
            return response
        else:
            print(f"Error")

    def smartcopy_check_plagiarism(self, text):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages = [
                      {"role": "system", "content": "You are a plagiarism checker"},
                      {"role": "user", "content": "check plagiarism in this text and highlight parts that are plagiarized:" },
                      {"role": "user", "content": text },
                    ],
            temperature =0.7,
            max_tokens = 2000,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            
            )
        print(response)

        if len(response['choices']) >= 1:
            return response
        else:
            print(f"Error")

    
    def smartcopy_write_facebook_ads(self, topic, target_audience, keywords, tone, word_count, n_copies, emoji, bullet_list, language):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages = [
                      {"role": "system", "content": "You are a facebook ads writer"},
                      {"role": "user", "content": "Write a " + tone + " facebook ads"},
                      {"role": "user", "content": "Topic: " + topic + ". Target Audience: " + target_audience + ". Keywords: " + keywords + "Word Count: " + str(word_count)  + ". Language: " + language + ".  Style: " + emoji + bullet_list},
                    ],
            temperature =0.7,
            max_tokens = 2000,
            top_p = 1,
            n = int(n_copies),
            frequency_penalty = 0,
            presence_penalty = 0,
            
            )
        print(response)

        if len(response['choices']) >= 1:
            return response
        else:
            print(f"Error")
    
    def smartcopy_facebook_post(self, topic, target_audience, keywords, tone, word_count, n_copies, emoji, bullet_list, language):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages = [
                      {"role": "system", "content": "You are a social media manager"},
                      {"role": "user", "content": "Write a " + tone + " facebook post"},
                      {"role": "user", "content": "Topic: " + topic + ". Target Audience: " + target_audience + ". Keywords: " + keywords + "Word Count: " + str(word_count)  + ". Language: " + language + ".  Style: " + emoji + bullet_list},
                    ],
            temperature =0.7,
            max_tokens = 2000,
            top_p = 1,
            n = int(n_copies),
            frequency_penalty = 0,
            presence_penalty = 0,
            
            )
        print(response)

        if len(response['choices']) >= 1:
            return response
        else:
            print(f"Error")
    
    def smartcopy_facebook_post_ideas(self, topic, target_audience, keywords, language):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages = [
                      {"role": "system", "content": "You are a social media manager"},
                      {"role": "user", "content": "Make a list of 10 topics for a facebook post ideas" },
                      {"role": "user", "content": "Topic: " + topic + ". Target Audience: " + target_audience + ". Keywords: " + keywords  + ". Language: " + language},
                    ],
            temperature =0.7,
            max_tokens = 500,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            
            )
        print(response)

        if len(response['choices']) >= 1:
            return response
        else:
            print(f"Error")

    
    
    def smartcopy_write_instagram_post(self, topic, target_audience, keywords, tone, word_count, n_copies, emoji, bullet_list, language):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages = [
                      {"role": "system", "content": "You are a instagram post writer"},
                      {"role": "user", "content": "Write a " + tone + " instagram post"},
                      {"role": "user", "content": "Topic: " + topic + ". Target Audience: " + target_audience + ". Keywords: " + keywords + "Word Count: " + str(word_count)  + ". Language: " + language + ".  Style: " + emoji + bullet_list},
                    ],
            temperature =0.7,
            max_tokens = 1000,
            top_p = 1,
            n = int(n_copies),
            frequency_penalty = 0,
            presence_penalty = 0,
            
            )
        print(response)

        if len(response['choices']) >= 1:
            return response
        else:
            print(f"Error")
    

    def smartcopy_write_instagram_tags(self,topic, target_audience, keywords, language):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                
                messages = [
                      {"role": "system", "content": "You are an expert social media manager"},
                      {"role": "user", "content": "Write 20 instagram tags in a single line"},
                      {"role": "user", "content": "Topic: " + topic + ". Target Audience: " + target_audience + ". Keywords: " + keywords + ". Language: " + language },
                    ],
            temperature =0.7,
            max_tokens = 1000,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            
            )
        print(response)

        if len(response['choices']) >= 1:
            return response
        else:
            print(f"Error")