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

        data_str= input("Enter your data here: ")
    
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

def updateSalesWorksheet(data):
    print("updating worksheet... \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully \n")

data = getSalesData()
salesData = [int(num) for num in data]
updateSalesWorksheet(salesData)


