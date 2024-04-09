import pyodbc
import datetime
import requests
from bs4 import BeautifulSoup


def executesqlstatement(sqlstatement, array, comboxstate, errormsg):
    result = []
    resultnames = []
    databaseconnection = ' Not connected'

    try:
        cnxn = pyodbc.connect("DRIVER={SQL Server}; Server=localhost\SQLEXPRESS; Database=master; Trusted_Connection=True;")  # CONNECTION STRING.
        databaseconnection = ' master'
        connected = True
    except:
        errormsg = " Database did not respond."
        connected = False

    if not connected:
        pass
    else:
        cursor = cnxn.cursor()

        if comboxstate == "Search the database":
            cursor.execute(sqlstatement)  # SEARCH STATEMENT
            result = cursor.fetchall()
        elif comboxstate == "Insert data in the database":
            try:
                cursor.execute(sqlstatement)  # INSERT STATEMENT
                sqlstatement = "SELECT * FROM CollyersParking WHERE RegistrationNumber = '" + array[0] + "'"
                cursor.execute(sqlstatement)  # SEARCHES NEW RECORD
                result = cursor.fetchall()
            except:
                errormsg = " Invalid owner ID entered / registration number already in database"
        elif comboxstate == "Modify data in the database":
            try:
                cursor.execute(sqlstatement)  # MODIFY STATEMENT
                sqlstatement = "SELECT * FROM CollyersParking WHERE RegistrationNumber = '" + array[0] + "'"
                cursor.execute(sqlstatement)  # SEARCHES NEW RECORD
                result = cursor.fetchall()
            except:
                errormsg = " Invalid registration number entered."
        else:
            cursor.execute(sqlstatement)  # DELETE STATEMENT
            sqlstatement = "SELECT * FROM CollyersParking"
            cursor.execute(sqlstatement)
            result = cursor.fetchall()
            errormsg = " Record deleted."

        for i in range(len(result)):
            sqlstatement = "SELECT Fname, Lname FROM CollyersMembers WHERE MemberID = '" + result[i][5] + "'"
            cursor.execute(sqlstatement)
            names = cursor.fetchall()
            resultnames.append(names)

    cnxn.close()

    return result, resultnames, errormsg, databaseconnection


def dateformat(year, month, day):
    date = ''
    error = True
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        date = datetime.datetime(year, month, day)
        date = str(date)
        date = date[:10]
        error = False
    except:
        pass
    return date, error


def datecheck(year1, month1, day1, year2, month2, day2):
    startdate = ''
    enddate = ''
    errormsg = " No errors found!"
    datesvalid = False
    currentdate = datetime.datetime.now()
    currentdate = str(currentdate)
    currentdate = currentdate[:10]
    if year1 == '' or month1 == '' or day1 == '':
        errormsg = " Start date not entered."
    else:
        startdate, starterror = dateformat(year1, month1, day1)
        if starterror == True:
            errormsg = " Start date not valid"
            startdate = ''
        else:
            if year2 == '' or month2 == '' or day2 == '':
                errormsg = " End date not entered."
            else:
                enddate, enderror = dateformat(year2, month2, day2)
                if enderror == True:
                    errormsg = " End date not valid"
                    enddate = ''
                else:
                    if startdate > enddate:
                        errormsg = " End date can't be smaller than start date."
                    else:
                        if startdate < currentdate:
                            errormsg = " Start date can't be in the past."
                        else:
                            datesvalid = True

    return startdate, enddate, datesvalid, errormsg


def regcheck(registration):
    make = ''
    model = ''
    try:
        # USER AGENT USED TO PREVENT WEBSITE FROM THINKING A ROBOT IS RETRIEVING DATA
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0/Safari/537.36'})

        website = "https://www.carcheck.co.uk/volkswagen/"

        url = f"{website}{registration}"  # APPENDS REGISTRATION NUMBER TO WEBSITE LINK
        html = requests.get(url, headers=headers)
        file = BeautifulSoup(html.text, "lxml")
        makeandmodel = file.find_all('td')
        makeandmodel = makeandmodel[2:4]

        # FORMATTING OF MAKE
        make = makeandmodel[0]
        make = str(make)
        make = make[4:-5]

        # FORMATTING OF MODEL
        model = makeandmodel[1]
        model = str(model)
        model = model[4:-5]

        errorreg = False
    except:
        errorreg = True

    return make, model, errorreg


def searchengine(array, comboxstate):
    databaseconnection = " Not connected"

    # CHECKING VALIDITY OF ENTERED DATES

    if array[3] != '' or array[4] != '' or array[5] != '':
        startdate, errorstart = dateformat(array[3], array[4], array[5])
    else:
        startdate = ''
        errorstart = False

    if array[6] != '' or array[7] != '' or array[8] != '':
        enddate, errorend = dateformat(array[6], array[7], array[8])
    else:
        enddate = ''
        errorend = False

    if errorstart == True:
        errormsg = " Invalid start date entered. Records shown may not adhere to criterias entered."
    else:
        errormsg = " No errors found!"

    if errorend == True:
        errormsg = " Invalid start date entered. Records shown may not adhere to criterias entered."
    else:
        errormsg = " No errors found!"

    array = ['RegistrationNumber', array[0], 'Make', array[1], 'Model', array[2], 'PermitStartDate', startdate,
             'PermitEndDate', enddate, 'MemberID', array[9]]
    sqlstatement = "SELECT * FROM CollyersParking WHERE "

    counter = 0

    for i in range(0, 6):
        if array[i * 2 + 1] != '':
            sqlstatementparts = array[i * 2] + " = '" + array[i * 2 + 1] + "' AND "
            sqlstatement = sqlstatement + sqlstatementparts
            counter = counter + 1
        else:
            pass

    if counter == 0:
        sqlstatement = "SELECT * FROM CollyersParking"
    else:
        sqlstatement = sqlstatement[:-5]

    result, resultnames, errormsg, databaseconnection = executesqlstatement(sqlstatement, array, comboxstate, errormsg)

    return result, resultnames, errormsg, databaseconnection


def insert(array, comboxstate):
    result = []
    resultnames = []
    errormsg = " No errors found!"
    databaseconnection = " Not connected"

    if array[0] == '':
        errormsg = " No registration number entered."
    else:
        sqlstatement = "INSERT INTO CollyersParking VALUES ("
        make, model, errorreg = regcheck(array[0])

        if errorreg == True:
            errormsg = " Invalid registration number entered."
        else:
            startdate, enddate, datesvalid, errormsg = datecheck(array[3], array[4], array[5], array[6], array[7],
                                                                 array[8])

            if not datesvalid:
                pass
            else:
                if array[9] == '':
                    errormsg = " No owner ID entered."
                else:
                    sqlstatement = sqlstatement + "'" + array[
                        0] + "', '" + make + "', '" + model + "', '" + startdate + "', '" + enddate + "', '" + array[
                                       9] + "')"
                    result, resultnames, errormsg, databaseconnection = executesqlstatement(sqlstatement, array,
                                                                                            comboxstate, errormsg)

    return result, resultnames, errormsg, databaseconnection


def modify(array, comboxstate):
    result = []
    resultnames = []
    errormsg = " No errors found!"
    databaseconnection = " Not Connected"

    if array[0] == '':
        errormsg = " No registration number entered."
    else:
        sqlstatement = "UPDATE CollyersParking SET "
        startdate, enddate, datesvalid, errormsg = datecheck(array[3], array[4], array[5], array[6], array[7], array[8])
        if datesvalid == False:
            pass
        else:
            sqlstatement = sqlstatement + "PermitStartDate = '" + startdate + "', PermitEndDate = '" + enddate + "' WHERE RegistrationNumber = '" + \
                           array[0] + "'"
            result, resultnames, errormsg, databaseconnection = executesqlstatement(sqlstatement, array, comboxstate,
                                                                                    errormsg)

    return result, resultnames, errormsg, databaseconnection


def delete(array, comboxstate):
    databaseconnection = " Not connected"
    errormsg = " No errors found!"
    sqlstatement = "DELETE FROM CollyersParking WHERE RegistrationNumber = '" + array[0] + "'"
    result, resultnames, errormsg, databaseconnection = executesqlstatement(sqlstatement, array, comboxstate, errormsg)

    return result, resultnames, errormsg, databaseconnection

