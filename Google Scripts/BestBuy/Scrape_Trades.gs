function menuCreateOnOpen() {
    var ui = SpreadsheetApp.getUi()
    ui.createMenu("Pricing Script Menu").addItem("Update...", "main").addToUi()
    // .addSubMenu().addItem("Apple Products")

}
function createDataSheet(sheetName) {
    var spreadSheet = SpreadsheetApp.getActiveSpreadsheet()
    try {
        spreadSheet.insertSheet(sheetName + " " + "Uniq", 1)
        return spreadSheet.setActiveSheet(spreadSheet.getSheets()[1])
    } catch (error) {
        Logger.log("Sheet Already Exists")
        Logger.log("Using Pre-existing Sheet")
        return spreadSheet.setActiveSheet(spreadSheet.getSheetByName(sheetName + " " + "Uniq"))
    }
}

function getDeviceList(url, headers) {
    for (attempts = 0; attempts < 4; attempts++) {
        // request to get list of devices
        try {
            var response = UrlFetchApp.fetch(url, headers);
            var data = JSON.parse(response.getContentText());
            Logger.log("Devices Obtained")
            return data["options"]; // reduce size of JSON
        }
        catch (error) {
            Logger.log("ERROR OCCURED WHILE GETTING DEVICES, TRYING AGAIN, ATTEMPT " + attempts)
            if (attempts === 3) {
                throw error;
            }
        }
    }
}
function getCarrier(url, phoneVal, headers) {
    for (attempts = 0; attempts < 4; attempts++) {
        try {
            // request to get carrier
            var response = UrlFetchApp.fetch(url + phoneVal, headers);
            var carrierData = JSON.parse(response.getContentText());
            return carrierData["options"][0]["value"]
        }
        catch (error) {
            Logger.log("ERROR OCCURED WHILE GETTING CARRIER, TRYING AGAIN, ATTEMPT " + attempts)
            if (attempts === 3) {
                throw error;
            }
        }
    }
}
function getSize(url, phoneVal, carrier, headers) {
    for (attempts = 0; attempts < 4; attempts++) {
        try {
            // request to get size
            var response = UrlFetchApp.fetch(url + phoneVal + "&carrier=" + carrier, headers);
            var sizeData = JSON.parse(response.getContentText());
            return sizeData["options"][0]["value"]
        }
        catch (error) {
            Logger.log("ERROR OCCURED WHILE GETTING SIZE, TRYING AGAIN, ATTEMPT " + attempts)
            if (attempts === 3) {
                throw error;
            }
        }
    }
}
function getColor(url, phoneVal, carrier, size, headers) {
    for (attempts = 0; attempts < 4; attempts++) {
        try {
            // request for colors based on phone, carrier, and sizes
            var response = UrlFetchApp.fetch(url + phoneVal + "&carrier=" + carrier + "&size=" + size, headers);
            var colorData = JSON.parse(response.getContentText());
            return colorData["options"][0]["value"].replace(/ /g, "%20")
        }
        catch (error) {
            Logger.log("ERROR OCCURED WHILE GETTING COLOR, TRYING AGAIN, ATTEMPT " + attempts)
            if (attempts === 3) {
                throw error;
            }
        }
    }
}
function getSku(url, phoneVal, carrier, size, color, headers) {
    for (attempts = 0; attempts < 4; attempts++) {
        try {
            // request to get SKU
            var response = UrlFetchApp.fetch(url + phoneVal + "&carrier=" + carrier + "&size=" + size + "&color=" + color, headers);
            var skuData = JSON.parse(response.getContentText());
            // shorten url to just sku
            skuData = skuData["redirectLink"]["uri"].replace(/.+sku=/, "")
            return skuData.toString();
        }
        catch (error) {
            Logger.log("ERROR OCCURED WHILE GETTING SKU, TRYING AGAIN, ATTEMPT " + attempts)
            if (attempts === 3) {
                throw error;
            }
        }
    }
}
function getPrice(url, sku, screenCon, condition, headers) {
    for (attempts = 0; attempts < 4; attempts++) {
        try {
            // request to get price based on conditions
            var response = UrlFetchApp.fetch(url + sku + "&crackedscreen-mob-1=" + screenCon + "&cellphone-condition2=" + condition, headers)
            var priceData = JSON.parse(response.getContentText());
            return priceData["appraisalValue"]
        }
        catch (error) {
            Logger.log("ERROR OCCURED WHILE GETTING PRICE, TRYING AGAIN, ATTEMPT " + attempts)
            if (attempts === 3) {
                throw error;
            }
        }
    }
}

function hasMainProcessStarted() {
    var value = PropertiesService.getScriptProperties().getProperty('mainProcessStarted');
    return value === 'true'
}

function hasMainProcessEnded() {
    var value = PropertiesService.getScriptProperties().getProperty('mainProcessEnded');
    return value === 'true'
}

function updateProgress(i, total) {
    PropertiesService.getScriptProperties().setProperty('currentProgress', i.toString());
    PropertiesService.getScriptProperties().setProperty('totalPhones', total.toString());
}

// Called by the progress dialog html to get current progress
function getProgress() {
    var props = PropertiesService.getScriptProperties();
    // get string value and convert to base 10 int
    var current = parseInt(props.getProperty('currentProgress'), 10) || 0;
    var total = parseInt(props.getProperty('totalPhones'), 10) || 0;
    return { current: current, total: total };
}

// This function is called from the client once the initial dialog closes
function showProgressDialog() {
    var html = HtmlService.createHtmlOutputFromFile('progressDialog')
        .setWidth(450)
        .setHeight(300);
    SpreadsheetApp.getUi().showModalDialog(html, "Progress");
}

function main() {
    spreadSheet = createDataSheet("BestBuy Trade-in Values");

    var phoneListURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/Generation/options" // URL to get list of phones
    var carrierListURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/Carrier/options?generation=" // List of networks, contingnt on phone
    var sizeListURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/Size/options?generation=" // List of sizes, contingnt on phone and carrier
    var colorListURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/Color/options?generation=" // List of colors, contingent on phone, carrier, and size
    var skuSearchURL = "https://tradein.bestbuy.com/catalog/product-families/iphones/search?generation=" // URL to get sku (sku must be extracted from a url value in response), based on all attributes
    var conditionURL = "https://tradein.bestbuy.com/catalog/products/appraisal?sku=" // URL to get value based on sku, screen, and condition
    var headers = {
        "headers": {
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
            'x-requested-with': 'XMLHttpRequest'
        }
    }

    // call func to get list of phones
    var data = getDeviceList(phoneListURL, headers);
    var numPhones = data.length;
    var phoneInfo = []; // list of dict for individual phone info (name, value, price->screen condition->condition->price, sku)


    const html = HtmlService.createHtmlOutputFromFile('initalDialog')
        .setWidth(450)
        .setHeight(300)
    var ui = SpreadsheetApp.getUi()
    ui.showModalDialog(html, "Running Script, Please be Patient")

    for (i = 0; i < numPhones; i++) {
        // Value key is for how info in calls are formated, name key is info formated for display
        var tempPhoneVal = data[i]["value"];
        var tempPhoneName = data[i]["name"];
        phoneInfo.push({ "value": tempPhoneVal, "name": tempPhoneName, "price": { "Yes": {}, "No": {} }, "sku": "" });
    }

    // Changes ui to progress ui from initial ui
    PropertiesService.getScriptProperties().setProperty('mainProcessStarted', 'true');
    // request to get list of carriers based on phone
    for (var i = 0; i < numPhones; i++) {
        Logger.log(i)
        Logger.log(phoneInfo[i])

        // Update Progress Every Iteration
        updateProgress(i, numPhones);

        var tempPhoneVal = phoneInfo[i]["value"]
        // request to get carrier
        var tempCarrVal = getCarrier(carrierListURL, tempPhoneVal, headers);

        // request for sizes based on phone and carrier
        var tempSizeVal = getSize(sizeListURL, tempPhoneVal, tempCarrVal, headers);

        // request for colors based on phone, carrier, and sizes
        var tempColorVal = getColor(colorListURL, tempPhoneVal, tempCarrVal, tempSizeVal, headers);

        // request to get SKU based on phone attributes
        var skuData = getSku(skuSearchURL, tempPhoneVal, tempCarrVal, tempSizeVal, tempColorVal, headers);
        phoneInfo[i]["sku"] = skuData;

        var tempScreen = "No"
        var condition = ["Good", "Fair"]
        var zeroVal = false;
        for (var j = 1; j <= 2; j++) {
            // request to get price for conditions if screen no crack
            var tempCondition = condition[j - 1]
            var priceData = getPrice(conditionURL, skuData, tempScreen, tempCondition, headers)
            if (priceData === 0) {
                phoneInfo.splice(i, 1)
                zeroVal = true
                break
            }
            phoneInfo[i]["price"]["No"][tempCondition] = priceData
        }
        if (zeroVal) {
            i--
            numPhones--
            continue
        }
        var tempScreen = "Yes"
        for (var j = 1; j <= 2; j++) {
            // request to get price for conditions if screen yes crack
            var tempCondition = condition[j - 1]
            var priceData = getPrice(conditionURL, skuData, tempScreen, tempCondition, headers)
            phoneInfo[i]["price"]["Yes"][tempCondition] = priceData
        }
        Logger.log(JSON.stringify(phoneInfo[i]))
    }
    updateProgress(i, numPhones);

    // var spreadSheet = SpreadsheetApp.getActiveSpreadsheet()
    // var cell = spreadSheet.getActiveCell();

    // Name, Screen Damage, Condititon, SKU (for quick update), Value, Date data last updated

    // Fill Column Headers
    spreadSheet.getRange("A1").setValue("Phone")
    spreadSheet.getRange("B1").setValue("Cracked")
    spreadSheet.getRange("C1").setValue("Condition")
    spreadSheet.getRange("D1").setValue("Value")
    spreadSheet.getRange("E1").setValue("SKU")
    spreadSheet.getRange("F1").setValue("Date Updated")

    var row = 2
    var numPhones = phoneInfo.length;
    var date = new Date()
    for (var i = 0; i < numPhones; i++) {
        // If phone has no value, skip
        if (phoneInfo[i]["price"]["No"]["Good"] === 0) {
            continue
        }
        for (var j = i; j < (i + 4); j++) {
            spreadSheet.getRange("A" + (row)).setValue(phoneInfo[i]["name"])
            if (j < (i + 2)) {
                spreadSheet.getRange("B" + (row)).setValue("No")
                if (j < (i + 1)) {
                    spreadSheet.getRange("C" + (row)).setValue("Good")
                    spreadSheet.getRange("E" + (row)).setValue(phoneInfo[i]["sku"])
                    spreadSheet.getRange("D" + (row)).setValue(phoneInfo[i]["price"]["No"]["Good"])
                    spreadSheet.getRange("F" + (row)).setValue(date)
                }
                else {
                    spreadSheet.getRange("C" + (row)).setValue("Fair")
                    spreadSheet.getRange("E" + (row)).setValue(phoneInfo[i]["sku"])
                    spreadSheet.getRange("D" + (row)).setValue(phoneInfo[i]["price"]["No"]["Fair"])
                    spreadSheet.getRange("F" + (row)).setValue(date)
                }
            }
            else {
                spreadSheet.getRange("B" + (row)).setValue("Yes")
                if (j < (i + 3)) {
                    spreadSheet.getRange("C" + (row)).setValue("Good")
                    spreadSheet.getRange("E" + (row)).setValue(phoneInfo[i]["sku"])
                    spreadSheet.getRange("D" + (row)).setValue(phoneInfo[i]["price"]["Yes"]["Good"])
                    spreadSheet.getRange("F" + (row)).setValue(date)
                }
                else {
                    spreadSheet.getRange("C" + (row)).setValue("Fair")
                    spreadSheet.getRange("E" + (row)).setValue(phoneInfo[i]["sku"])
                    spreadSheet.getRange("D" + (row)).setValue(phoneInfo[i]["price"]["Yes"]["Fair"])
                    spreadSheet.getRange("F" + (row)).setValue(date)
                }
            }
            row++
        }
    }
}


