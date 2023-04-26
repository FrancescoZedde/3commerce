from serpapi import GoogleSearch
from django.conf import settings



class SerpApi:
    def __init__(self):

        self.api_key = settings.SERPAPI_KEY
    
    def serp_reverse_image(self, image_url):
        params = {
          "engine": "google_reverse_image",
          "image_url": image_url,
          "api_key": self.api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        inline_images = results["inline_images"]
        #print(inline_images)

        return inline_images

    def serp_search_by_query(self, query, location, language):
        params = {
                    "engine": "google_shopping",
                    "q": query,
                    "location": "Austin, Texas, United States",
                    "hl": language,
                    "gl": location,
                    "api_key": self.api_key,
                    }

        search = GoogleSearch(params)
        results = search.get_dict()
    
        shopping_results = results["shopping_results"]
        print(shopping_results)
        return shopping_results

    def serp_search_sellers_by_product_id(self, product_id,location, language):

        params = {
          "engine": "google_product",
          "product_id": product_id,
          "offers": "1",
          "hl": language,
          "gl": location,
          "api_key": self.api_key,
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        print(results)
        sellers_results = results["sellers_results"]
        return sellers_results

    
    def serp_ebay_search_by_query(self, query):

        params = {
        "engine": "ebay",
        "_nkw": query,
        "api_key": self.api_key,
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        print('FULL JSON')
        print(results)
        organic_results = results["organic_results"]

        return organic_results