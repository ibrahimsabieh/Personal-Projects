// This file simpily holds data like urls, headers, etc



var phoneListURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/Generation/options" // URL to get list of phones
var carrierListURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/Carrier/options?generation=" // List of networks, contingnt on phone
var sizeListURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/Size/options?generation=" // List of sizes, contingnt on phone and carrier
var colorListURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/Color/options?generation=" // List of colors, contingent on phone, carrier, and size
var skuSearchURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/search?generation=" // URL to get sku (sku must be extracted from a url value in response), based on all attributes
var conditionURL = "https://tradein.bestbuy.com/catalog/products/appraisal?sku=" // URL to get value based on sku, screen, and condition
var headers = {
  "headers" : {
    'accept': 'application/madness+json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tradein.bestbuy.com/client/',
    'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest' }
}