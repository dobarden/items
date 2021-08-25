
from __future__ import print_function
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.search_items_resource import SearchItemsResource
from paapi5_python_sdk.partner_type import PartnerType
from paapi5_python_sdk.rest import ApiException
from paapi5_python_sdk.availability import Availability
from paapi5_python_sdk.get_items_request import GetItemsRequest
from paapi5_python_sdk.get_variations_request import GetVariationsRequest

# My addons
import time
from amzn_credentials import a_key, s_key, partner_id
import datetime



def search_items():

    """ Following are your credentials """
    """ Please add your access key here """

    access_key = a_key 

    """ Please add your secret key here """
    secret_key = s_key 

    """ Please add your partner tag (store/tracking id) here """
    partner_tag = partner_id 

    """ PAAPI Host and Region to which you want to send request """
    """ For more details refer: https://webservices.amazon.com/paapi5/documentation/common-request-parameters.html#host-and-region"""
    host = "webservices.amazon.com"
    region = "us-east-1"

    """ API declaration """
    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    
    items = []
    with open('items.txt') as file:
        for item in file.readlines():
            items.append(item.strip())
    numbers = list(range(0,len(items),10))
    err_list = []
    for number in numbers:
        divided_items = items[number:number+10]
        # print(divided_items)


        """ Forming request """
        try:
            
            search_items_request = GetItemsRequest(
                partner_tag=partner_tag,
                partner_type=PartnerType.ASSOCIATES,

                item_ids= divided_items, 
                resources=["Offers.Listings.Availability.Message", "ItemInfo.Title"],
                

                # resources=search_items_resource,
            )
        except ValueError as exception:
            print("Error in forming SearchItemsRequest: ", exception)
            return

        try:
            """ Sending request """
            response = default_api.get_items(search_items_request)

                       
            item_0 = response.items_result.items
            for i in range(len(response.items_result.items)):

                print("ASIN: ", item_0[i].asin)
                if item_0[i].offers is not None:
                    print("STATUS: ", item_0[i].offers.listings[0].availability.message)
                else:
                    print('STATUS: ERROR!!!')
                    err_list.append(item_0[i].asin)
                print("URL: ", item_0[i].detail_page_url)
                print('')

            
        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])

        except TypeError as exception:
            print("TypeError :", exception)

        except ValueError as exception:
            print("ValueError :", exception)

        except Exception as exception:
            print("Exception :", exception)
        if len(items) > number+10:
            print('Wait 2 seconds...')
            time.sleep(2)
        else:
            print(f'{len(items)} items checked')
            print(f'{len(err_list)} items with errors')
            if len(err_list) > 0:
                with open('err_items.txt', 'a') as errfile:
                    date = datetime.datetime.today()
                    errfile.write(f'Date: {date.strftime("%d-%m-%Y")} \n')
                    i = 1
                    for err_item in err_list:
                        errfile.write(f'{i}) {err_item} \n')
                        i += 1
            
search_items()