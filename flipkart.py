import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


gadget = str(input('Search gadget:'))
gadget = gadget.replace(' ', '+')
totle = 0
header = True
mode = 'w'


for i in range(1,42):
    url = requests.get(f'https://www.flipkart.com/search?q={gadget}&page={i}').text

    soup = BeautifulSoup(url, 'lxml')

    for div in soup.find_all('div', class_='bhgxx2 col-12-12'):

        c_name = None
        m = None
        color = None
        price = None
        disc = None
        ram = None
        rom = None
        display = None
        battery = None
        processor = None

        try:
            name = div.find('div', class_='_3wU53n').text
            price = div.find('div', class_='_1vC4OE _2rQ-NK').text
            price = price[1:]
            price = price.replace(',','')
            price = int(price)
            spec = div.find('div', class_='_3ULzGw')

            try:
                c_name = name.split(' ')
                c_name = c_name[0]
                #print(f'Company : {c_name} ')
            except:
                pass

            try:
                modelncolor = name.split('(')
                model = modelncolor[0]
                if c_name in model:
                    m = model.replace(c_name,'')
                m = m.strip()
                #print(f'Model : {m} ')
            except:
                pass

            try:
                modelncolor = name.split('(')
                color = modelncolor[1]
                color = color.split(',')
                color = color[0]
                #print(f'Color : {color} ')
            except:
                pass

            try:
                mrp = div.find('div', class_='_3auQ3N _2GcJzG').text
                mrp = mrp[1:]
                mrp = mrp.replace(',','')
                mrp = int(mrp)
                #print(f'Price: {price}')
                #print(f'MRP : {mrp}')
            except:
                #print(f'Price: {price}')
                #print(f'MRP : {price}')
                mrp = price

            try:
                rr = spec.find(text=re.compile('.RAM.'))
                rr = rr.split(' ')
                ram = rr[0] + rr[1]
                ram = int(ram)
                #print(f'RAM : {ram}')
            except:
                pass

            try:
                try:
                    rr = spec.find(text=re.compile('.ROM.*'))
                    rr = rr.split(' ')
                    rom = rr[4] + rr[5]
                    rom = int(rom)
                    #print(f'ROM : {rom}')                   
                except:
                    modelncolor = name.split('(')
                    rom = modelncolor[1]
                    rom = rom.split(',')
                    rom = rom[1]
                    rom = rom.strip(')')
                    #print(f'ROM : {rom}')                    
            except:
                pass

            try:
                display = spec.find(text=re.compile('.Display'))
                display = display.split('(')
                display = str(display[0])
                display = display.split(' ')
                display = float(display[0])
                #print(f'Display size : {display}')
            except:
                pass
            try:
                battery = spec.find(text=re.compile('.Battery'))
                battery = battery.split('Battery')
                battery = str(battery[0])
                battery = battery.split(' ')
                battery = int(battery[0])
                #print(f'Battery size : {battery}')
            except:
                pass

            try:
                try:
                    processor = spec.find(text=re.compile('.Processor'))
                    processor = processor.strip('Processor')
                    #print(f'Processor : {processor}')
                except:
                    processor = spec.find(text=re.compile('.processor.'))
                    processor = processor.split('processor')
                    processor = processor[0]
                    #print(f'Processor : {processor}')
            except:
                pass

        
            totle = totle + 1
            dict = { 'Company Name' : c_name, 'Model' : m, 'Color' : color, 'Price' : price, 'MRP' : mrp, 'RAM' : ram, 'ROM' : rom, 'Display size' : display, 'Battery size' : battery, 'Processor' : processor }
            df = pd.DataFrame(dict, index =[totle]) 
            df.to_csv('samsung.csv', encoding='utf-8', header=header, mode=mode) 
            header = False
            mode = 'a'
            print('          |')

        except:
            pass

        try:
            name = div.find('a', class_='_2cLu-l').text
            price = div.find('div', class_='_1vC4OE').text
            print(f'Name : {name} ')
            try:
                disc = div.find('div', class_='_3auQ3N').text
                print(f'Price: {price} for you, original price {disc}')
            except:
                print(f'Price: {price} There is no discount')

        except:
            pass

    print(f'-------   {i}   --------')

print(totle)



'''
div = soup
try:
    name = div.find('div', class_='_3wU53n').text
    price = div.find('div', class_='_1vC4OE _2rQ-NK').text
    print(f'Name : {name} ')
    try:
        disc = div.find('div', class_='_3auQ3N _2GcJzG').text
        print(f'Price: {price} for you, original price {disc}')
    except:
        print(f'Price: {price} There is no discount')


    try:
        spec = div.find('div', class_='_3ULzGw')
        try:
            rr = spec.find(text = re.compile('.RAM.'))
            rr = rr.split(' ')
            ram = rr[0]+' '+rr[1]
            rom = rr[4] +' '+rr[5]
            print(f'RAM : {ram}')
            print(f'ROM : {rom}')
        except:
            pass

        try:
            display = spec.find(text = re.compile('.Display'))
            display = display.split('(')
            display = display[0]
            print(f'Display size : {display}')
        except:
            pass

        try:
            battery = spec.find(text = re.compile('.Battery'))
            battery = battery.split('Battery')
            battery = battery[0]
            print(f'Battery size : {battery}')
        except:
            pass

        try:
            processor = spec.find(text = re.compile('.Processor'))
            processor = processor.split('Processor')
            processor = processor[0]
            print(f'Processor : {processor}')
        except:
            pass
        
        print('')
    except:
        pass
  
except:
    pass

try:
    name = div.find('a', class_='_2cLu-l').text
    price = div.find('div', class_='_1vC4OE').text
    print(f'Name : {name} ')
    try:
        disc = div.find('div', class_='_3auQ3N').text
        print(f'Price: {price} for you, original price {disc}')
    except:
        print(f'Price: {price} There is no discount')
        print('')


except:
    pass


'''