function getDeviceList(url, headers){
  for(attempts = 0; attempts < 4; attempts++) {
    // request to get list of devices
    try {
      var response = UrlFetchApp.fetch(url, headers);
      var data = JSON.parse(response.getContentText());
      Logger.log("Devices Obtained")
      return data["options"]; // reduce size of JSON
    } 
    catch(error) {
      Logger.log("ERROR OCCURED WHILE GETTING DEVICES, TRYING AGAIN, ATTEMPT "+attempts)
      if(attempts === 3){
        throw error;
      }
    }
  }
}
function getCarrier(url, phoneVal, headers){
  for(attempts = 0; attempts < 4; attempts++) {
    try {
      // request to get carrier
      var response = UrlFetchApp.fetch(url+phoneVal, headers);
      var carrierData = JSON.parse(response.getContentText());
      return carrierData["options"][0]["value"]
      } 
      catch(error) {
        Logger.log("ERROR OCCURED WHILE GETTING CARRIER, TRYING AGAIN, ATTEMPT "+attempts)
        if(attempts === 3){
          throw error;
        }
      }
  }
}
function getSize(url, phoneVal, carrier, headers){
  for(attempts = 0; attempts < 4; attempts++) {
  try {
    // request to get size
    var response = UrlFetchApp.fetch(url+phoneVal+"&carrier="+carrier, headers);
    var sizeData = JSON.parse(response.getContentText());
    return sizeData["options"][0]["value"]
    } 
    catch(error) {
      Logger.log("ERROR OCCURED WHILE GETTING SIZE, TRYING AGAIN, ATTEMPT "+attempts)
      if(attempts === 3){
        throw error;
      }
    }
  }
}
function getColor(url, phoneVal, carrier, size, headers){
  for(attempts = 0; attempts < 4; attempts++) {
    try {
      // request for colors based on phone, carrier, and sizes
      var response = UrlFetchApp.fetch(url+phoneVal+"&carrier="+carrier+"&size="+size, headers);
      var colorData = JSON.parse(response.getContentText());
      return colorData["options"][0]["value"].replace(/ /g,"%20")
      } 
      catch(error) {
        Logger.log("ERROR OCCURED WHILE GETTING COLOR, TRYING AGAIN, ATTEMPT "+attempts)
        if(attempts === 3){
          throw error;
        }
      }
  }
}
function getSku(url, phoneVal, carrier, size, color, headers){
    for(attempts = 0; attempts < 4; attempts++) {
      try {
        // request to get SKU
        var response = UrlFetchApp.fetch(url+phoneVal+"&carrier="+carrier+"&size="+size+"&color="+color, headers);
        var skuData = JSON.parse(response.getContentText());
        // shorten url to just sku
        skuData = skuData["redirectLink"]["uri"].replace(/.+sku=/, "")
        return skuData.toString();
      } 
      catch(error) {
        Logger.log("ERROR OCCURED WHILE GETTING SKU, TRYING AGAIN, ATTEMPT "+attempts)
        if(attempts === 3){
          throw error;
        }
      }
  } 
}
function getPrice(url, sku, screenCon, condition, headers){
  for(attempts = 0; attempts < 4; attempts++) {
  try {
    // request to get price based on conditions
    var response = UrlFetchApp.fetch(url+sku+"&crackedscreen-mob-1="+screenCon+"&cellphone-condition2="+condition, headers)
    var priceData = JSON.parse(response.getContentText());
    return priceData["appraisalValue"]
  } 
  catch(error) {
    Logger.log("ERROR OCCURED WHILE GETTING PRICE, TRYING AGAIN, ATTEMPT "+attempts)
    if(attempts === 3){
      throw error;
    }
  }
  } 
}