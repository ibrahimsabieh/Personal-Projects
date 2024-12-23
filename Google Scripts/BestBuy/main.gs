// This script pulls the trade in values of iPhones from Best Buy and lists them
// on a google sheet.
//
// Due to how Google App Script's run time enviorment works
// all scripts inside a project are apart of the same global enviorment
// and do not require any import/export statements
//
// Todo: 
// Expand script to cover other devices
// Add more ui menu items that may be necessary with any changes made


function main() {
    spreadSheet = createDataSheet("BestBuy Trade-in Values");

    const html = HtmlService.createHtmlOutputFromFile('initalDialog')
        .setWidth(450)
        .setHeight(300)
    var ui = SpreadsheetApp.getUi()
    ui.showModalDialog(html, "Running Script, Please be Patient")

    // call func to get list of phones
    var data = getDeviceList(phoneListURL, headers);
    var numPhones = data.length;
    var phoneInfo = []; // list of dict for individual phone info (name, value, price->screen condition->condition->price, sku)

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

function updateEntry() {

    var spreadSheet = SpreadsheetApp.getActiveSpreadsheet()
    var sheet = spreadSheet.getActiveSheet()

    var cell = sheet.getCurrentCell().getA1Notation()

    var skuCell = cell.replace(/^[A-Za-z]/, "E");
    var val = sheet.getRange(skuCell).getValue()

    Logger.log(val)


}


