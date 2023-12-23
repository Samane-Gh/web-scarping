from gettext import install
from turtle import title
from unicodedata import name
from colorama import Cursor
import requests
from bs4 import BeautifulSoup
import mysql.connector
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder

x = []
y = []

r = requests.get('https://bama.ir/car?body=van')
soup = BeautifulSoup(r.text,'html.parser')
cars = soup.find_all('div',{'class':'bama-ad__content-holder'})
for car in cars:    
    car_items = car.find('div',{'class':'bama-ad__top-section'})
    titles = car_items.find('div',{'class':'bama-ad__title-holder'})
    name = titles.find('div',{'class':'bama-ad__title'}).text
    
    
    detals = car.find('div', {'class':'bama-ad__detail-holder'})
    span = detals.find_all('span')
    year = span[0].text
    
    mile = span[2].text.split(' ')[0]
    if(mile == 'کارکرد'):
        mile = '0'
    footer = car.find('div',{'class':'bama-ad__footer'})
    price_holder = footer.find('div',{'class':'bama-ad__price-holder'})
    cost = price_holder.find('span',{'class':'bama-ad__price'})    
    mile = mile.replace(',','')    
    installments = price_holder.find('div',{'class':'bama-ad__installment-holder'})    
    if(cost is not None and cost.text.strip() != 'توافقی'):   
        x.append([name , float(year), float(mile)])        
        costValue = cost.text.replace(',','')
        y.append(float(costValue))
        
    cnx = mysql.connector.connect(user='root', password='Samane@3',
                               host='127.0.0.1',
                               database='cars',                                                            
                               auth_plugin='mysql_native_password')
    Cursor = cnx.cursor()
    quary = ("INSERT INTO car (name,year,mile,cost) VALUES (%s,%s,%s,%s)")
    if installments is not None:
        val = (name,year,mile,installments.text.split(' ')[1])
        Cursor.execute(quary,val)
        cnx.commit()
        cnx.close()            
        x.append([name , float(year), float(mile)])        
        costValue = installments.text.split(' ')[1].replace(',','')
        y.append(float(costValue))
        
    cnx = mysql.connector.connect(user='root', password='Samane@3',
                               host='127.0.0.1',
                               database='cars',                                                            
                               auth_plugin='mysql_native_password')
    Cursor = cnx.cursor()
    quary = ("INSERT INTO car (name,year,mile,cost) VALUES (%s,%s,%s,%s)")
    if installments is not None:
        val = (name,year,mile,installments.text.split(' ')[1])
        Cursor.execute(quary,val)
        cnx.commit()
        cnx.close()
        
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y)
print (" ***** Please enter your car information for predicting it's cost : ******")
print ("****   firts inter car name  , second car year  and the theird car mile  ******* ")
new_data = input().split(' ')
answer = clf.predict(new_data)
print(answer)