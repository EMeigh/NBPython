# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:09:00 2016

@author: Elijah Meigh

latest vertion of ASAS (python program for viewing and analysing SQL data)

NOTES:

1) i have commented the code, but i am dyslexic, please be forgiving when you find spelling mistakes :)
2) comments include my thoughts on areas of improvment in the future - this is somthing i do 
   so that i don't forget about bugs / potential issues / areas that could be improved
3) I did have some MongoDB functionality in an earlier version but it has since been removed.
   the functionality was very limited - it could connect to the database and pull out a document
   but did not include graphing or pretty display or anything (basically, what was in the lecture slides).
   If you want to see this i can send it to you.
4) I also had some writting to SQL functionality in a previous vertion. functionaility it was the same as detailed
   in 3) - basically just what was in the lecture slides. i can also send you this if you need / want it
"""

# Required imports
# tKinter throws warnings but it seems to work OK
from tkinter import *
import tkinter.messagebox
import matplotlib.pyplot as plt
import pymysql 
import numpy as np
import matplotlib.patches as mpatches



#ASAS Class - Contains SQL queeries and data analysis functions
class ASAS:
    #initialise the connection
    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', 'Pa$$W0rd', 'nbgardens')
    
    #function to close the db connection. required to prevent system slowdown
    def closeDBConnection(self, event):
        self.db.close()
    # so that the database can then be re-opned if required. maybe could just call __init__?
    # Investigate above in future
    def openDBConnection(self, event):
        self.db = pymysql.connect('localhost', 'root', 'Pa$$W0rd', 'nbgardens')   
        
    # function to grab and display customer data. 
    #in future i will try and turn this into a partial so that products / employees can also be checked
    def getCustData(self, event): #function for retrieving data
    
        #open cursor (allows DB to be 'searched')
        self.cursor = self.db.cursor()
        sql = "SELECT idCustomer, firstName, lastName FROM customer"
        #execute SQL command specified above
        self.cursor.execute(sql)
        #store results in 'results'
        results = self.cursor.fetchall()
        #close cursor - prevents clashes when another function is called
        self.cursor.close()
        #print(results)
        print("C ID|  F Name         | L Name")
        for column in results:
            idCustomer = column[0] 
            firstName = column[1]
            lastName = column[2]
            print(idCustomer, "  |", firstName, " \t|", lastName)
            
    def bestCustomer(self, event):
        #open cursor (allows DB to be 'searched')
        self.cursor = self.db.cursor()
        sql =  "select cust_idCustomer, firstName, lastName, round(sum((ol.quantity*p.salePrice)),2) as Value_Of_Total_Orders, count(distinct o.idpurchase) as 'number_of_orders' from Purchase as o join PurchaseLines as ol on ol.pur_idPurchase=o.idPurchase join product as p on p.idProduct=ol.pro_idProduct join customer as c on o.cust_idCustomer = c.idCustomer where o.purchaseStatus != 'Returned' AND  createDate BETWEEN '2014-01-01' AND '2016-12-30' group by c.firstName order by Value_Of_Total_Orders desc"
        #execute SQL command specified above
        self.cursor.execute(sql)
        #store results in 'results'
        results = self.cursor.fetchall() 
        #print(results)
        print(results)
        #close cursor - prevents clashes when another function is called
        self.cursor.close()
        #close any previous open plots. does nothing if no plots are active. saves an IF statement
        plt.clf()
        #declare arrays/lists that will be used for plotting
        idCustomer = []
        moneySpent = []
        #extract plotting data from results
        for column in results:
            idCustomer.append(column[0])
            moneySpent.append(column[3])
        #plot results, state axis size (in future this should be dynamic
        # to account for different data sets by looking at list for max/min values and using
        # for axis parameters), also decaling axis lables
        plt.bar(idCustomer, moneySpent, 1,  color="blue")       
        plt.axis([0, 10, 0, 20000])
        plt.ylabel('Total spend in £')
        plt.xlabel('Customer ID') 
        
    def bestSalespeople(self, event):
        #open cursor (allows DB to be 'searched')
        self.cursor = self.db.cursor()
        sql = "select e.idEmployee, e.FirstName, e.LastName, round(sum((ol.Quantity*p.salePrice)),2) as Value_Of_Total_Orders, count(distinct o.idPurchase) as 'Total Orders', createDate from purchase as o join purchaselines as ol on ol.pur_idPurchase=o.idPurchase join product as p on p.idProduct=ol.pro_idProduct join employee as e on o.emp_idEmployee=e.idEmployee where o.purchaseStatus != 'returned' group by idEmployee"
        #execute SQL command specified above
        self.cursor.execute(sql)
        #store results in 'results'
        results = self.cursor.fetchall() 
        #print(results)
        print(results)
        #close cursor - prevents clashes when another function is called
        self.cursor.close()
        #close any previous open plots. does nothing if no plots are active. saves an IF statement
        plt.clf()
        #declare arrays/lists that will be used for plotting
        idEmployee = []
        totalSales = []
        #extract plotting data from results
        for column in results:
            idEmployee.append(column[0])
            totalSales.append(column[3])
        #plot results, state axis size (in future this should be dynamic
        # to account for different data sets by looking at list for max/min values and using
        # for axis parameters), also decaling axis lables
        plt.bar(idEmployee, totalSales, 1,  color="blue")       
        plt.axis([0, 10, 0, 15000])
        plt.ylabel('Total Sales in £')
        plt.xlabel('Employee ID') 
        
    def getCustomRangeData(self, event):
        #open cursor (allows DB to be 'searched')
        self.cursor = self.db.cursor()
        sDate = entryField3.get()        
        eDate = entryField4.get()
        sql = "SELECT pro_idProduct, round(avg(rating),2) FROM formreview WHERE reviewDate BETWEEN '" + sDate + "' AND '" + eDate + "' GROUP BY pro_idProduct"
        #execute SQL command specified above
        self.cursor.execute(sql)
        #store results in 'results'
        results = self.cursor.fetchall()
        #close cursor - prevents clashes when another function is called
        self.cursor.close()
        #close any previous open plots. does nothing if no plots are active. saves an IF statement
        plt.clf()
        #print(results)
        print("P ID    | Average Rating")
        for column in results:
            idProduct = column[0] 
            avRating = column[1]
            print(idProduct, "\t|   ", avRating)
            plt.bar(idProduct, avRating, 1,  color="blue")  
        #plot results, state axis size (in future this should be dynamic
        # to account for different data sets by looking at list for max/min values and using
        # for axis parameters), also decaling axis lables
        plt.axis([0, 35, 0, 10])
        plt.ylabel('Average rating out of 10')
        plt.xlabel('product ID')   

    def get1YearData(self, event):
        #open cursor (allows DB to be 'searched')
        self.cursor = self.db.cursor()
        year = entryField.get()
        sql = "SELECT pro_idProduct, round(avg(rating),2) FROM formreview WHERE reviewDate BETWEEN '" + year + "-01-01' AND '" + year + "-12-30' GROUP BY pro_idProduct"
        #execute SQL command specified above
        self.cursor.execute(sql)
        #store results in 'results'
        results = self.cursor.fetchall()
        #close cursor - prevents clashes when another function is called
        self.cursor.close()
        #close any previous open plots. does nothing if no plots are active. saves an IF statement
        plt.clf()
        #print(results)
        print("P ID    | Average Rating")
        for column in results:
            idProduct = column[0] 
            avRating = column[1]
            print(idProduct, "\t|   ", avRating)
            plt.bar(idProduct, avRating, 1,  color="blue") 
        #plot results, state axis size (in future this should be dynamic
        # to account for different data sets by looking at list for max/min values and using
        # for axis parameters), also decaling axis lables
        plt.axis([0, 35, 0, 10])
        plt.ylabel('Average rating out of 10')
        plt.xlabel('product ID') 
        
    # function for calculating running avergae using numpty. sourced from stackexchange
    def runningMeanFast(self,x, N):
        return np.convolve(x, np.ones((N,))/N)[(N-1):]
        
    def oneProductManyYears(self, event):
        #open cursor (allows DB to be 'searched')
        self.cursor = self.db.cursor()
        idProduct = entryField2.get()
        sql = "SELECT pro_idProduct, rating, reviewDate FROM formreview  WHERE pro_idProduct ='" + idProduct + "'ORDER BY reviewDate asc"
        #execute SQL command specified above
        self.cursor.execute(sql)
        #store results in 'results'
        results = self.cursor.fetchall()
        #close cursor - prevents clashes when another function is called
        self.cursor.close()
        #close any previous open plots. does nothing if no plots are active. saves an IF statement
        plt.clf()
        #declare arrays/lists that will be used for plotting
        #also declaring variables for running avergae calculations
        # i = incrementing number of points
        # runningTotal = expanding total for avearge calculation
        i = 0;
        idProduct = []
        avRating = []
        date = []
        mAvRating = []
        runningTotal = 0
        #extract plotting data from results
        for column in results:
            i = i+1
            idProduct.append(column[0])
            avRating.append(column[1])  
            date.append(column[2])
            runningTotal = runningTotal + column[1]
            mAvRating.append(ASAS1.runningMeanFast(runningTotal, i))
        #plot results, state axis size (in future this should be dynamic
        # to account for different data sets by looking at list for max/min values and using
        # for axis parameters), also decaling axis lables
        plt.plot_date(date, avRating, 'b-*')
        plt.plot_date(date, mAvRating, 'r-*')
        plt.ylabel('Rating out of 10')
        plt.xlabel('Time') 
        blue_patch = mpatches.Patch(color='blue', label='Individual Rating')
        red_patch = mpatches.Patch(color='red', label='Running Average')
        plt.legend(handles=[blue_patch, red_patch])  
        plt.show()


#Class for GUI functions. currently only contains message functions.
#in future i need to expand to include formatting buttons, applying functionality
# and general layout stuff
class GUIFunctions:
    
    def AllProductDataMessage(self, event):
        tkinter.messagebox.showinfo('Multiple product data help', 'To use this function, please enter the year that you wish to view in the entry field and then press the blue "Get Anual Data" button')
        
    def SingleProductDataMessage(self, event):
        tkinter.messagebox.showinfo('Single product data help', 'To use this function, please enter the product ID that you wish to view in the entry field and then press the blue "Get Product Data" button')            

    def AllProductUserRangeDataMessage(self, event):
        tkinter.messagebox.showinfo('Multiple product, custome range data help', 'To use this function, please enter the start and end date of the period that you wish to view in the entry fields and then press the blue "Get Product Data" button. Please enter date information in the following format YYYY-MM-DD') 

    def getCustDataMessage(self, event):
        tkinter.messagebox.showinfo('Customer Data Help', 'Pressing the "Get Customer Data" button will retrieve customer details')


#initiate GUI
root = Tk()
#initiate ASAS funtions
ASAS1 = ASAS()
#initiate GUIfuntions
GUI1 = GUIFunctions()


###################################
#the following 'main' is very messy and long. i need to turn this code into functions
#and put them into the GUI class.
###################################


#GUI formatting
topFrame = Frame(root)
topFrame.pack(side = TOP)

#Welcome label
welcomeLabel = Label(topFrame, text = "Welcome to the ASAS application!!", bg = "yellow") 
welcomeLabel.pack(fill = X)
welcomeLabel2 = Label(topFrame, text = "Please select the functionthat you would like to perform from the buttons below", bg = "yellow")
welcomeLabel2.pack(fill = X)

#frames for formatting GUI
leftFrame = Frame(root)
rightFrame = Frame(root)
bottomFrame = Frame(root)
leftFrame.pack(side = LEFT)
rightFrame.pack(side = RIGHT)
bottomFrame.pack(side = BOTTOM)


#button creation. currently names are illogical. i need to come up with better names
button1 = Button(leftFrame, text = "Help", fg = "black")
button7 = Button(leftFrame, text = "Help", fg = "black")
button3 = Button(leftFrame, text = 'Help', fg = "black")
button9 = Button(leftFrame, text = 'Help', fg = "black")

button2 = Button(leftFrame, text = "Get Anual Data", fg = "blue")
button8 = Button(leftFrame, text = "Get Product Data", fg = "blue")
button4 = Button(leftFrame, text = "Get Range Data", fg = "blue")
button10 = Button(leftFrame, text = "Get Customer Data", fg = "purple")
button11 = Button(leftFrame, text = "Best Customers", fg = "purple")
button12 = Button(leftFrame, text = "Best Salespeople", fg = "purple")

button5 = Button(rightFrame, text = "open database connection", fg = "green")
button6 = Button(rightFrame, text = "close database connection", fg = "red")


#assigning button functionality
button1.bind("<Button-1>", GUI1.AllProductDataMessage)
button7.bind("<Button-1>", GUI1.SingleProductDataMessage)
button3.bind("<Button-1>", GUI1.AllProductUserRangeDataMessage)
button9.bind("<Button-1>", GUI1.getCustDataMessage)

button2.bind("<Button-1>", ASAS1.get1YearData)
button8.bind("<Button-1>", ASAS1.oneProductManyYears)
button4.bind("<Button-1>", ASAS1.getCustomRangeData)
button10.bind("<Button-1>", ASAS1.getCustData)
button11.bind("<Button-1>", ASAS1.bestCustomer)
button12.bind("<Button-1>", ASAS1.bestSalespeople)

button5.bind("<Button-1>", ASAS1.openDBConnection)
button6.bind("<Button-1>", ASAS1.closeDBConnection)

#placing buttons in GUI
button1.grid(row = 0, column = 0)
button3.grid(row = 1, column = 0)
button7.grid(row = 2, column = 0)
button9.grid(row = 3, column = 0)

button2.grid(row = 0, column = 1)
button4.grid(row = 1, column = 1)
button8.grid(row = 2, column = 1)
button10.grid(row = 3, column = 1)
button11.grid(row = 4, column = 1)
button12.grid(row = 5, column = 1)

button5.grid(row = 2, column = 3)
button6.grid(row = 3, column = 3)


#creating entry fields. same naming problem as buttons
entryField = Entry(leftFrame)
entryField3 = Entry(leftFrame)
entryField4 = Entry(leftFrame)
entryField2 = Entry(leftFrame)

#placing entry fields in GUI
entryField.grid(row = 0, column = 2)
entryField3.grid(row = 1, column = 2)
entryField4.grid(row = 1, column = 3)
entryField2.grid(row = 2, column = 2)

#make GUI a loop. Exit button will close loop.
#i need to find a way to close the database connection when 'the little red X' is clicked
root.mainloop()