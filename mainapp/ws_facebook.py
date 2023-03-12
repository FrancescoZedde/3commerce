import requests
import json
from users.models import CustomUser


'''
POST /{ig-user-id}/media: carica contenuti multimediali e crea contenitori di oggetti multimediali.
POST /{ig-user-id}/media_publish: pubblica contenuti multimediali caricati utilizzando i relativi contenitori.
GET /{ig-container-id}?fields=status_code: verifica l'idoneità alla pubblicazione e lo stato dei contenitori di contenuti multimediali.
GET /{ig-user-id}/content_publishing_limit: verifica l'utilizzo del rate limiting di pubblicazione corrente dell'utente dell'app.

'''
# CREATE CONTAINER MEDIA
def instagram_create_container_media(user, url_image, caption, is_carousel):
    user_instance = CustomUser.objects.get(email=user.email)
    url = 'https://graph.facebook.com/v16.0/' + str(user_instance.instagram_user_id) +'/media'

    if is_carousel == True:
        print('carousel-media')
        data = {'access_token': user_instance.facebook_access_token,
                'image_url': url_image, 
                'caption': caption,
                'is_carousel_item': 'true', 
                }
    else:
        data = {'access_token': user_instance.facebook_access_token,
                'image_url': url_image, 
                'caption': caption
                }

    response = requests.post(url=url, data=data).json()
    print(response)
    return response['id']


# CHECK CONTAINER VALIDITY
'''
GET https://graph.facebook.com/{ig-container-id}
  ?fields={fields}
  &access_token={access-token}'''

def instagram_check_container_validity(user, container_id):
    user_instance = CustomUser.objects.get(email=user.email)
    url = 'https://graph.facebook.com/v16.0/' + str(container_id) + '?fields=status_code&access_token=' + str(user_instance.facebook_access_token)

    print(url)
    data = {'access_token': user_instance.facebook_access_token,
            }
    response = requests.get(url=url).json()
    print(response)
# CREATE CONTAINER CAROUSEL
'''
curl -i -X POST \

"https://graph.facebook.com/v16.0/str(user_instance.instagram_user_id)/media?
caption=Fruit%20candies&
media_type=CAROUSEL&
children=17899506308402767%2C18193870522147812%2C17853844403701904&
access_token=EAAOc..."
'''
def instagram_create_container_carousel(user, ids_array, caption):
    user_instance = CustomUser.objects.get(email=user.email)
    '''
    url = 'https://graph.facebook.com/v16.0/' + str(user_instance.instagram_user_id) +'/media'
    data = {'access_token': user_instance.facebook_access_token,
            'media_type': 'CAROUSEL',
            'children':ids_array,
            'caption': caption}'''
    url = 'https://graph.facebook.com/v16.0/' + str(user_instance.instagram_user_id) +'/media?caption=' + str(caption) + '&media_type=CAROUSEL&children=' + str(ids_array) + '&access_token=' + str(user_instance.facebook_access_token)
    print(url)
    #print(requests.post(url=url, data=data))
    #response = requests.post(url=url, data=data).json()
    response = requests.post(url=url).json()
    print(response)
    return response['id']

# PUBLISH CAROUSEL
'''
curl -i -X POST \

"https://graph.facebook.com/v16.0/90010177253934/media_publish?
creation_id=18000748627392977&
access_token=EAAOc..."
'''
def instagram_publish_carousel(user, carousel_id):
    user_instance = CustomUser.objects.get(email=user.email)
    url = 'https://graph.facebook.com/v16.0/' + str(user_instance.instagram_user_id) +'/media_publish'
    data = {'access_token': user_instance.facebook_access_token,
            'creation_id': carousel_id, 
            }

    response = requests.post(url=url, data=data).json()
    print(response)
