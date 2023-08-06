from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ]

def get_date():
    from datetime import date
    today = date.today()
    d = today.strftime("%m/%d/%Y")
    return d

def get_month():
    month_index = datetime.now().month - 1
    return [month_index, months[month_index]]
    
def get_year():
    return int(datetime.now().year)