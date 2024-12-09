from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import requests
import random

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["chrome-extension://gibnnb÷pigmmjnphimmmbaiikljdbahcc"], 
    # Replace with your extension ID
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PriceRequest(BaseModel):
    product_name: str

# def get_list():
#     url = "https://free-proxy-list.net/"
#     soup = BeautifulSoup(requests.get(url).content, 'html.parser')
#     proxies = []
#     for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
#         tds = row.find_all("td")
#         try:
#             ip = tds[0].text.strip()
#             port = tds[1].text.strip()
#             proxies.append("http://" + str(ip) + ":" + str(port))
#         except IndexError:
#             continue
#     return proxies

def random_user_agent():
    # List of operating systems
    operating_systems = [
        "Windows NT 10.0",
        "Windows NT 6.3",
        "Windows NT 6.2",
        "Macintosh; Intel Mac OS X 10_15_7",
        "Macintosh; Intel Mac OS X 10_14_6",
        "Linux; Android 10; Pixel 3 XL",
        "Linux; Android 11; Samsung Galaxy S21",
        "Linux x86_64",
        "Windows NT 6.1; WOW64",
        "Macintosh; Intel Mac OS X 10_13_6"
    ]
    
    # List of browsers
    browsers = [
        "Chrome",
        "Firefox",
        "Safari",
        "Edge",
        "Opera"
    ]

    # Expanded version numbers for Chrome
    chrome_versions = [
        "90.0.4430.93",
        "91.0.4472.124",
        "92.0.4515.107",
        "93.0.4577.63",
        "94.0.4606.61",
        "95.0.4638.54",
        "96.0.4664.45",
        "97.0.4692.71",
        "98.0.4758.102",
        "99.0.4844.51",
        "100.0.4896.60"
    ]

    # Expanded version numbers for Firefox
    firefox_versions = [
        "88.0",
        "89.0",
        "90.0",
        "91.0",
        "92.0",
        "93.0",
        "94.0",
        "95.0",
        "96.0",
        "97.0",
        "98.0"
    ]

    # Expanded version numbers for Safari
    safari_versions = [
        "14.0.1",
        "14.1",
        "15.0",
        "15.1",
        "15.2",
        "15.3",
        "16.0",
        "16.1"
    ]

    # Expanded version numbers for Edge
    edge_versions = [
        "90.0.818.51",
        "91.0.864.41",
        "92.0.902.62",
        "93.0.961.38",
        "94.0.992.50",
        "95.0.1020.40",
        "96.0.1054.34",
        "97.0.1072.69",
        "98.0.1108.43",
        "99.0.1150.55",
        "100.0.1185.36"
    ]

    # Expanded version numbers for Opera
    opera_versions = [
        "76.0.4017.177",
        "77.0.4054.90",
        "78.0.4093.184",
        "79.0.4143.22",
        "80.0.4170.25",
        "81.0.4196.61",
        "82.0.4227.35",
        "83.0.4254.27",
        "84.0.4300.48",
        "85.0.4341.18",
        "86.0.4361.0"
    ]

    # Randomly choose an OS and browser
    os = random.choice(operating_systems)
    browser = random.choice(browsers)

    # Randomly choose a version based on the browser
    if browser == "Chrome":
        version = random.choice(chrome_versions)
        user_agent = f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
    elif browser == "Firefox":
        version = random.choice(firefox_versions)
        user_agent = f"Mozilla/5.0 ({os}; rv:{version}) Gecko/20100101 Firefox/{version}"
    elif browser == "Safari":
        version = random.choice(safari_versions)
        user_agent = f"Mozilla/5.0 ({os}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Safari/605.1.15"
    elif browser == "Edge":
        version = random.choice(edge_versions)
        user_agent = f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 Edg/{version}"
    elif browser == "Opera":
        version = random.choice(opera_versions)
        user_agent = f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 OPR/{version}"

    return user_agent


async def fetch_amazon_price(product_name: str):
    search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    headers = {
        "User-Agent": random_user_agent()
    }
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    # proxies = get_list()  # Fetch the proxy list
    # proxy = random.choice(proxies)  # Select a random proxy
    # print(f"amazon proxy: {proxy}")
    
    # async with httpx.AsyncClient(proxies={"http": proxy, "https": proxy}) as client:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(search_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all("a", href=True)
            productlist = []

            for link in product_links:
                if len(productlist) >= 5:
                    break

                if "dp/" in link['href'] and all(word.lower() in link['href'].lower() for word in product_name.split()):
                    product_url = link['href']
                    if not product_url.startswith('http'):
                        product_url = "https://www.amazon.in" + product_url

                    product_response = await client.get(product_url, headers=headers)
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.text, 'html.parser')

                    title_tag = product_soup.find("span", id="productTitle")
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)
                    if productlist and productlist[-1]["title"] == title:
                        continue
                    
                    price_tag = product_soup.find("span", class_="a-price-whole")
                    price = price_tag.get_text(strip=True)

                    productlist.append({
                        "title": title,
                        "price": price
                    })
              
            return productlist 
        except httpx.RequestError as e:
            print(f"An error occurred while requesting: {e}")
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url}")
    
    return None


async def fetch_flipkart_price(product_name: str):
    search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
    headers = {
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "User-Agent": random_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    # proxies = get_list()  # Fetch the proxy list
    # proxy = random.choice(proxies)  # Select a random proxy
    # print(f"flipkart proxy: {proxy}")

    # async with httpx.AsyncClient(proxies={"http": proxy, "https": proxy}) as client:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try :
            response = await client.get(search_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all("a", href=True)
            productlist = []

            for link in product_links:
                if len(productlist) >= 5:
                    break

                if all(word.lower() in link['href'].lower() for word in product_name.split()):
                    product_url = link['href']
                    if not product_url.startswith('http'):
                        product_url = "https://www.flipkart.com" + product_url

                    product_response = await client.get(product_url, headers=headers)
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.text, 'html.parser')

                    title_tag = product_soup.find("h1")
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)
                    if productlist and productlist[-1]["title"] == title:
                        continue

                    price_tag = product_soup.find("div", string=lambda text: '₹' in text if text else False)
                    price = price_tag.get_text(strip=True)

                    productlist.append({
                        "title": title,
                        "price": price
                    })

            return productlist
                
        except httpx.RequestError as e:
            print(f"An error occurred while requesting: {e}")
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url}")

    return None

async def fetch_myntra_price(product_name: str):
    search_url = f"https://www.myntra.com/{product_name.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    # proxies = get_list()  # Fetch the proxy list
    # proxy = random.choice(proxies)  # Select a random proxy
    # print(f"myntra proxy: {proxy}")

    # async with httpx.AsyncClient(proxies={"http": proxy, "https": proxy}) as client:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try :
            response = await client.get(search_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            # <a data-refreshpage="true" target="_blank" href="charger/cmf+by+nothing/cmf-by-nothing-65w-gan-charger/27744208/buy" style="display: block;">
            product_link = soup.find("a", {"class": "product-base"})

            if product_link:
                product_url = product_link['href']
                product_response = await client.get(product_url, headers=headers)
                product_response.raise_for_status()

                product_soup = BeautifulSoup(product_response.text, 'html.parser')
                price_tag = product_soup.find("span", {"class": "product-discountedPrice"})

                if price_tag:
                    return price_tag.get_text(strip=True)
                else:
                    print("pricetag not found")
            else :
                print("no product link found")
                
        except httpx.RequestError as e:
            print(f"An error occurred while requesting: {e}")
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url}")       
        
    return None

@app.post("/fetch-prices")
async def fetch_prices(request: PriceRequest):
    
    product_name = request.product_name
    amazon_price = await fetch_amazon_price(product_name)
    flipkart_price = await fetch_flipkart_price(product_name)
    myntra_price = await fetch_myntra_price(product_name)

    prices = {
        "amazon": amazon_price,
        "flipkart": flipkart_price,
        "myntra": myntra_price
    }


    if not any(prices.values()):
        raise HTTPException(status_code=404, detail="Prices not found")

    return prices

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
