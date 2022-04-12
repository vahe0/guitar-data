import requests
import json
import csv


headers = {"Content-Type": "application/hal+json; charset=utf-8", "Accept-Version": str(3.0)}


#Type may also be "acoustic-guitars" or any other type that is found on Reverb.com
type = 'electric-guitars'

#Electric guitars in particular are categorized in these four ways on Reverb. We will use a for loop to get listings for all of them. 
#The "left-handed" category may be problematic because some people list guitars under "solid-body" but they are also left-handed.  
categories = ['solid-body', 'semi-hollow', 'hollow-body', 'left-handed']

#This constant specifies how many pages to look through via a for loop as well. More pages may result in listings that were posted a long time ago.
NUMBER_OF_PAGES = 10
    
data ={}
ls =[]

print('In progress...')

for category in categories:

    for page in range(NUMBER_OF_PAGES):
        
        #At the end of the url, we can pass "&year_max=1980" to only get guitars manufactured prior to 1980. The year can be changed.
        response = requests.get(f'https://api.reverb.com/api/listings/all?category={category}&product_type={type}&page={page}&per_page=50',headers=headers)
        listings = response.json()['listings']  
        text = json.dumps(listings, sort_keys=True, indent=4)
       
        
        for listing in listings:
            data = {
                'price': listing['price']['amount'], 
                'category':  category ,
                'type': type,
                'make' : listing['make'] ,
                'model': listing['model'] ,
                'year': listing['year'],
                'finish': listing['finish'],
                'condition': listing['condition']['display_name'],
                'auction': listing['auction'],                                                             #Boolean that indicates if listing is an auction or not.                                                      
                'shipping_cost' : listing['shipping']['initial_offer_rate']['rate']['display']['amount'],  #It is worth investigating what exactly this shipping cost implies. The prices should vary depending on location.
                'accepts_offers': listing['offers_enabled'],                                               #Boolean indicating if the seller accepts offers for the guitar.
                'date' : listing['published_at'],                                                          #Date listing was published
            }
        
            ls.append(data)
    
    keys = ls[0].keys()

with open('guitar_data.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(ls)
print('Completed')