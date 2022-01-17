from bs4 import BeautifulSoup
import requests
import csv
import extractData as eD

filename = r"C:\Users\KIIT\Desktop\MagicBricksDataFinal.csv"

cities = []

url = 'https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey' \
      '-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName='

wikiURL = 'https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population'
soupWIKI = BeautifulSoup(requests.get(wikiURL).text, 'lxml')

cols = ['city', 'name', 'developer', 'rera-id', 'price', 'water-availability', 'status-of-electricity', 'lift',
        'furnishing', 'bedrooms', 'bathrooms', 'status', 'configuration', 'tower-and-unit-details', 'recommended-for',
        'neighborhood', 'roads', 'safety', 'cleanliness', 'public-transport', 'parking', 'connectivity', 'traffic',
        'school', 'restaurants', 'hospital', 'market', 'locality-rating']

# Collects list of important cities from wikipedia
for city in soupWIKI.find_all('tr'):
    x = city.find_all('td')
    try:
        cities.append(x[1].a.text)
    except:
        IndexError


# Collects links of apartment listings from magicbricks
print("Stats:")
cityCTR = 0
hotelCTR = 0
with open(filename, 'w', newline="") as file:
    writer = csv.writer(file)
    writer.writerow(cols)
    for city in cities:
        ctr = 0
        soup = BeautifulSoup(requests.get(url + city).text, 'lxml')
        for hotel in soup.find_all('div', class_='SRCard'):
            try:
                link = hotel['data-code'].split('event')[1].split(',')[1].split('\'')[1]
                data = eD.make_data_row(link)
                writer.writerow([city] + data)
                hotelCTR += 1
                ctr += 1
                print(hotelCTR)
            except Exception as e:
                print(e, "in", city)

        cityCTR += 1
        print(f"For {city} : total-hotel = {ctr}")

print(f"\nTotal cities = {cityCTR}")
print(f"Total listings = {hotelCTR}")