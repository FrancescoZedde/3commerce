from django.shortcuts import render
from openai_app.openai_forms import ChatGPTAsk, EmailMarketingForm, BlogArticleForm, BlogIdeasForm, BlogPlagiarismForm, FacebookAdsForm,FacebookPostForm, FacebookPostIdeasForm, InstagramPostForm, InstagramTagsForm, GoogleAdsTitleForm, GoogleAdsDescriptionForm, AmazonProductDescription
from openai_app.ws_gpt import ChatGPT
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings


from main_app.db_functions import updateUserWords
# Create your views here.


@login_required(login_url='/login')
def smartcopy_start(request):
    if request.method == 'GET':
        return render(request, 'openai_app/smartcopy_start.html')

@login_required(login_url='/login')
def smartcopy_play(request):
    if request.method == 'GET':
        return redirect(smartcopy_start)
    elif request.method == 'POST':
        service = request.POST.get('service')
        if service == 'blog-article':
            form = BlogArticleForm()
        elif service == 'blog-ideas':
            form = BlogIdeasForm()
        elif service == 'blog-plagiarism':
            form = BlogPlagiarismForm()
        elif service == 'facebook-ads':
            form = FacebookAdsForm()
        elif service == 'facebook-post':
            form = FacebookPostForm()
        elif service == 'facebook-post-ideas':
            form = FacebookPostIdeasForm()
        elif service == 'instagram-post':
            form = InstagramPostForm()
        elif service == 'instagram-tags':
            form = InstagramTagsForm()
        elif service == 'google-ads-title':
            form = GoogleAdsTitleForm()
        elif service == 'google-ads-description':
            form = GoogleAdsDescriptionForm()
        elif service == 'email-marketing':
            form = EmailMarketingForm()
        elif service == 'amazon-description':
            form = AmazonProductDescription()

        service_title = service.replace('-', ' ').title()
        context = { 'service_title':service_title,
                    'service': service,
                    'form':form, 
                    'GPT_KEY' : settings.CHAT_GPT_KEY}
        return render(request, 'openai_app/smartcopy_play.html', context)

@login_required(login_url='/login')
def smartcopy_write(request):
    if request.method == 'GET':
        return redirect(smartcopy_start)
    elif request.method == 'POST':
        print(request.POST)
        class_instance = ChatGPT()

        service = request.POST.get('service')
        if service == 'blog-article':
            '''
            if int(request.user.words) <= 0:
                return JsonResponse('no tokens')
            else:'''
            topic = request.POST.get('topic')
            target_audience = request.POST.get('target_audience')
            keywords = request.POST.get('keywords')
            tone = request.POST.get('tone')
            word_count = request.POST.get('word_count')
            language = request.POST.get('language')
            results = ChatGPT.smartcopy_write_blog_article(class_instance,topic, target_audience, keywords, tone, word_count, language)
            updateUserWords(request.user, results['usage']['completion_tokens'])    
            return JsonResponse(results)

        elif service == 'blog-ideas':
            topic = request.POST.get('topic')
            target_audience = request.POST.get('target_audience')
            keywords = request.POST.get('keywords')
            language = request.POST.get('language')
            results = ChatGPT.smartcopy_blog_ideas(class_instance, topic, target_audience, keywords, language)
            updateUserWords(request.user, results['usage']['completion_tokens'])   
            return JsonResponse(results)

        elif service == 'blog-plagiarism':
            text = request.POST.get('text')
            results = ChatGPT.smartcopy_check_plagiarism(class_instance,text)
            updateUserWords(request.user, results['usage']['completion_tokens'])   
            return JsonResponse(results)

        elif service == 'facebook-ads':
            topic = request.POST.get('topic')
            target_audience = request.POST.get('target_audience')
            keywords = request.POST.get('keywords')
            tone = request.POST.get('tone')
            word_count = request.POST.get('word_count')
            language = request.POST.get('language')
            emoji = request.POST.get('emoji')
            bullet_list = request.POST.get('bullet_list')
            n_copies = request.POST.get('n_copies')
            results = ChatGPT.smartcopy_write_facebook_ads(class_instance, topic, target_audience, keywords, tone, word_count, n_copies, emoji, bullet_list, language)
            updateUserWords(request.user, results['usage']['completion_tokens'])
            return JsonResponse(results)

        elif service == 'facebook-post':
            topic = request.POST.get('topic')
            target_audience = request.POST.get('target_audience')
            keywords = request.POST.get('keywords')
            tone = request.POST.get('tone')
            word_count = request.POST.get('word_count')
            language = request.POST.get('language')
            emoji = request.POST.get('emoji')
            bullet_list = request.POST.get('bullet_list')
            n_copies = request.POST.get('n_copies')
            results = ChatGPT.smartcopy_write_facebook_ads(class_instance, topic, target_audience, keywords, tone, word_count, n_copies, emoji, bullet_list, language)
            updateUserWords(request.user, results['usage']['completion_tokens'])   
            return JsonResponse(results)

        elif service == 'facebook-post-ideas':
            topic = request.POST.get('topic')
            target_audience = request.POST.get('target_audience')
            keywords = request.POST.get('keywords')
            language = request.POST.get('language')
            results = ChatGPT.smartcopy_facebook_post_ideas(class_instance, topic, target_audience, keywords, language)
            updateUserWords(request.user, results['usage']['completion_tokens'])   
            return JsonResponse(results)

        elif service == 'instagram-post':
            topic = request.POST.get('topic')
            target_audience = request.POST.get('target_audience')
            keywords = request.POST.get('keywords')
            tone = request.POST.get('tone')
            word_count = request.POST.get('word_count')
            language = request.POST.get('language')
            emoji = request.POST.get('emoji')
            bullet_list = request.POST.get('bullet_list')
            n_copies = request.POST.get('n_copies')
            results = ChatGPT.smartcopy_write_instagram_post(class_instance, topic, target_audience, keywords, tone, word_count, n_copies, emoji, bullet_list, language)
            updateUserWords(request.user, results['usage']['completion_tokens'])   
            return JsonResponse(results)

        elif service == 'instagram-tags':
            topic = request.POST.get('topic')
            target_audience = request.POST.get('target_audience')
            keywords = request.POST.get('keywords')
            language = request.POST.get('language')
            results = ChatGPT.smartcopy_write_instagram_tags(class_instance,topic, target_audience, keywords, language)
            updateUserWords(request.user, results['usage']['completion_tokens'])   
            return JsonResponse(results)

        elif service == 'google-ads-title':
            form = GoogleAdsTitleForm()
        elif service == 'google-ads-description':
            form = GoogleAdsDescriptionForm()
        elif service == 'email-marketing':
            form = EmailMarketingForm()
        elif service == 'amazon-description':
            form = AmazonProductDescription()




@login_required(login_url='/login')
def generate_img_page(request):
    if request.method=='GET':
        assistant_chat_form = ChatGPTAsk()
        context = {
            'assistant_chat_form':assistant_chat_form,
        }
        return render(request, 'openai_app/generate_img_page.html', context)
    if request.method =='POST':
        question = request.POST.get('question', None)
        if question != None:
            assistant_chat_form = ChatGPTAsk()
            class_instance = ChatGPT()
            answer = ChatGPT.answer_question(class_instance, question, max_tokens)
            print(answer)
            context = {
                'question': question,
                'answer': answer,
                'assistant_chat_form': assistant_chat_form,
            }
            return render(request, 'openai_app/generate_img_page.html', context)

@login_required(login_url='/login')
def generate_img(request):
    question = request.POST.get('question')
    n_copies = request.POST.get('n_copies')
    class_instance = ChatGPT()
    response =ChatGPT.generate_image_from_prompt(class_instance,question, n_copies )
    #response =ChatGPT.generate_image_variation(class_instance)
    print(response)
    return HttpResponse(response)