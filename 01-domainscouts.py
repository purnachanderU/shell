import requests
import re
from collections import Counter

url = input("Enter the URL : ")
response = requests.get(url)
data = response.text

domains = re.findall(r'https?://?([a-zA-Z0-9.-]+\.(?:com|org|net))', data)

count = Counter(domains)
for domain, count_val, in count.items():
    print(domain, ":", count_val)


#prime_numbers = {x:x for x in ranage(100) if x%2 != 0 and x > 1}
