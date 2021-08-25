# amazon_items.py
# The script makes a request through the Amazon API to Amazon.com and checks the availability of items.
# You need to create a file "amzn_credentials.py" with your API key. And the items.txt file with items ASINs (one  ASIN = one line).
# After checking, the script will create a file "err_items.txt" in which the ASINs of items that are out of stock will be listed.