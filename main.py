import requests
import selectorlib
import smtplib, ssl
import os
import  time
import sqlite3

Connection=sqlite3.connect("data2.db")




URL="http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    response=requests.get(url,headers=HEADERS)
    source=response.text
    return source

def extract(source):
    extractor=selectorlib.Extractor.from_yaml_file("extract.yaml")
    value=extractor.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = ""
    password = ""


    receiver = ""
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent")


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor=Connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)",row)
    Connection.commit()

def read(extracted):
    row=extracted.split(",")
    row=[item.strip() for item in row]
    band,city,date=row
    cursor = Connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",(band,city,date))
    rows=cursor.fetchall()
    print(rows)
    return rows

if __name__=="__main__":
    while True:
       scraped=scrape(URL)
       extracted=extract(scraped)

       print(extracted)


       if extracted != "No upcoming tours":
           row=read(extracted)
           if not row:
                store(extracted)
                send_email(message="Hey new event found")
        time.sleep(2)