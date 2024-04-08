import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS =Credentials.from_service_account_file('creds.json')

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def getSalesData():
    """
    Get sales input data from the user
    """
    while True:
        print("Please enter sales data")
        print("Data should be six numbers, seperated by comma's")
        print("Eg 3,4,5,6,7,8\n")

        data_str= input("Enter your data here: \n")
    
        salesData = data_str.split(",")

        if validateData(salesData):
            print("Valid data")
            break
    
    return salesData

def validateData(values):
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e} Please try again \n")
        return False
    
    return True

def updateWorksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculateSurplusData(sales_row):
    print("Calculating surplus stock")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def getLastFiveEntrySales():
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculateStockData(data):
    print("calculating stock data...")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column ]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    data = getSalesData()
    salesData = [int(num) for num in data]
    updateWorksheet(salesData, "sales")
    newSurplusData = calculateSurplusData(salesData)
    updateWorksheet(newSurplusData, "surplus")
    salesColumns = getLastFiveEntrySales()
    stockData = calculateStockData(salesColumns)
    updateWorksheet(stockData, "stock")
    

main()


