// Creates menu
function menuCreateOnOpen() {
  var ui = SpreadsheetApp.getUi()
  ui.createMenu("Pricing Script Menu")
  .addSubMenu(ui.createMenu("Update...").addItem("All", "main").addSubMenu(ui.createMenu("Apple Products").addItem("All", "main").addItem("iPhones", "updateEntry")))
  .addToUi()
  // .addSubMenu().addItem("Apple Products")
  
}

// Creates new sheet if not exists
function createDataSheet(sheetName){
  var spreadSheet = SpreadsheetApp.getActiveSpreadsheet()
  try {
    spreadSheet.insertSheet(sheetName+" "+"Uniq", 1)
    return spreadSheet.setActiveSheet(spreadSheet.getSheets()[1])
  } catch (error) {
    Logger.log("Sheet Already Exists")
    Logger.log("Using Pre-existing Sheet")
    return spreadSheet.setActiveSheet(spreadSheet.getSheetByName(sheetName+" "+"Uniq"))
  }
}




// Called by inital dialog html to know when process is started
function hasMainProcessStarted() {
  var value = PropertiesService.getScriptProperties().getProperty('mainProcessStarted');
  return value === 'true'
}

// updates progress values
function updateProgress(i, total) {
  PropertiesService.getScriptProperties().setProperty('currentProgress', i.toString());
  PropertiesService.getScriptProperties().setProperty('totalPhones', total.toString());
}

// Called by progress dialog html to get current progress
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






