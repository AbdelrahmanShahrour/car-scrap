import numpy as np
import openpyxl
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
#795 page

'''
----------------------------------------------------------------------------------------
|<... 1. Colect data ...>                                                              |
|    1. Scraping. <scrap>. page1 = 1 , page2 = 200; return (<data1>)                   |
|<\... Colect data ...>                                                                |
|--------------------------------------------------------------------------------------|
|<... 2. fet eng ...>                                                                  |
|    2. data1> Split adds. return (<data2>)                                            |
|<\... fet eng ...>                                                                    |
|--------------------------------------------------------------------------------------|
|<... 3. Preprocessing ...>                                                            |
|    3. data2> removing NaN data. return (<data3>)                                     |
|  * 4. data3> true price. return (<data4>)                                            |
|<\... Preprocessing ...>                                                              |
|--------------------------------------------------------------------------------------| 
|<... 4. Save data ...>                                                                |
|    5. data4, data_all> append. return (<data5>) >> save data5 "opensooqcar.xlsx"     |
|<\... Save data ...>                                                                  |
---------------------------------------------------------------------------------------|
'''

def getinfo(tag, fet, name,intq=0):
    Cars = soup.find_all(tag, {fet:name})
    if len(Cars)==0:
        Cars = np.NaN
    else:
        x = str(Cars[intq].text.replace('  ','').replace('\n',''))
        s = int(x.find(':'))
        Cars = x[s+1:]
    return Cars

def find_date():
    datelist = soup.find_all('span', {"class":"postDate relative fRight"})
    if len(datelist)==0:
        return np.NaN
    else:
        x = datelist[0].text.replace('  ','').replace('\n','')
        if '-' in x:
            return x

        else: 
            return str(datetime.datetime.today())[:10]

def check():
    dateinline = soup.find_all('span', {"class":"postDate relative fRight"})[0].text.replace('  ','').replace('\n','')
    if ('أمس' in dateinline) or ('-' in dateinline):
        return False
    else:
        return True



def splitadds(data):
    uniquelist = ['فتحة',
    'مراياكهربائية',
    'شاشةلمس',
    'نظامملاحة',
    'مثبتسرعة',
    'مكيف',
    'كاميراخلفية',
    'حساساتاصطفاف',
    'كراسيجلد',
    'كراسيمدفأة',
    'أكياسهوائية',
    'أضويةLED',
    'مدخلAUX/USB',
    'بلوتوث',
    'ABS',
    'سنترلوك',
    'أضويةزينون',
    'دخولبدونمفتاح']

    listalladd = []

    for i in range(data.shape[0]):
        x = str(data['additions'].iloc[i]).replace('[','').replace(']','').replace(' ','').replace("'",'').split(',')
        listalladd.append(str(x))
        pass

    data['adds'] = listalladd
    def get_the_add(q, df):
        xx = []
        for i in range(df.shape[0]):
            if q in df['adds'].iloc[i]:
                xx.append('Yes')
            else:
                xx.append('No')
        return xx

    data['فتحة'] = get_the_add(uniquelist[0], data)
    data['مرايا كهربائية'] = get_the_add(uniquelist[1], data)
    data['شاشة لمس'] = get_the_add(uniquelist[2], data)
    data['نظام ملاحة'] = get_the_add(uniquelist[3], data)
    data['مثبت سرعة'] = get_the_add(uniquelist[4], data)
    data['مكيف'] = get_the_add(uniquelist[5], data)
    data['كاميرا خلفية'] = get_the_add(uniquelist[6], data)
    data['حساسات اصطفاف'] = get_the_add(uniquelist[7], data)
    data['كراسي جلد'] = get_the_add(uniquelist[8], data)
    data['كراسي مدفأة'] = get_the_add(uniquelist[9], data)
    data['أكياس هوائية'] = get_the_add(uniquelist[10], data)
    data['LED'] = get_the_add(uniquelist[11], data)
    data['مدخلAUX/USB'] = get_the_add(uniquelist[12], data)
    data['بلوتوث'] = get_the_add(uniquelist[13], data)
    data['ABS'] = get_the_add(uniquelist[14], data)
    data['سنترلوك'] = get_the_add(uniquelist[15], data)
    data['أضوية زينون'] = get_the_add(uniquelist[16], data)
    data['دخول بدون مفتاح'] = get_the_add(uniquelist[17], data)
    return data

def preprocessing(data):
    data3 = data.dropna()
    # data4 = data3[data3['price']>1500 & data3['price']<200000]
    return data3


def saving(datascrap, main_data):
    final_data = datascrap.append(main_data,ignore_index=True)
    final_data.to_excel('true_data.xlsx',index=False)


if __name__ == "__main__":
    main_data = pd.read_excel('true_data.xlsx')
    linkscar, city, n, Brand, Brand_child, Car_Year, regional_specs, Tramsmission_Cars, Fuel_Cars, Car_Color, ConditionUsed, Kilometers_Cars, paint, body_condition, CarCustoms, CarLicense, CarInsurance, Payment_Method, additions, date, price = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for page in range(1,200):
        link = f"https://jo.opensooq.com/ar/%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D9%88%D9%85%D8%B1%D9%83%D8%A8%D8%A7%D8%AA/%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D9%84%D9%84%D8%A8%D9%8A%D8%B9?page={page}"
        result = requests.get(link)
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        a = soup.find_all('a', {"class":"block postLink notEg postSpanTitle noEmojiText"},href=True)
        
        for i in a:
            x = 'https://jo.opensooq.com'+i['href']
            result = requests.get(x)
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            ###########
            if check():
                price1 = soup.find_all('strong', {"class":"priceCurrencyMiddle"})
                date.append(find_date())
                city.append(getinfo('li', "class", "inline vTop relative mb15"))
                linkscar.append(x)
                n.append(getinfo('li', "class", "inline vTop relative mb15",1))
                Brand.append(getinfo('li', "data-icon", "PostDynamicAttribute[Brand]"))
                Brand_child.append(getinfo('li', "data-icon", "PostDynamicAttribute[Brand_child]"))
                Car_Year.append(getinfo('li', "data-icon", "PostDynamicAttribute[Car_Year]"))
                regional_specs.append(getinfo('li', "data-icon", "PostDynamicAttribute[regional_specs]"))
                Tramsmission_Cars.append(getinfo('li', "data-icon", "PostDynamicAttribute[Tramsmission_Cars]"))
                Fuel_Cars.append(getinfo('li', "data-icon", "PostDynamicAttribute[Fuel_Cars]"))
                Car_Color.append(getinfo('li', "data-icon", "PostDynamicAttribute[Car_Color]"))
                ConditionUsed.append(getinfo('li', "data-icon", "PostDynamicAttribute[ConditionUsed]"))
                Kilometers_Cars.append(getinfo('li', "data-icon", "PostDynamicAttribute[Kilometers_Cars]"))
                paint.append(getinfo('li', "data-icon", "PostDynamicAttribute[paint]"))
                body_condition.append(getinfo('li', "data-icon", "PostDynamicAttribute[body_condition]"))
                CarCustoms.append(getinfo('li', "data-icon", "PostDynamicAttribute[CarCustoms]"))
                CarLicense.append(getinfo('li', "data-icon", "PostDynamicAttribute[CarLicense]"))
                CarInsurance.append(getinfo('li', "data-icon", "PostDynamicAttribute[CarInsurance]"))
                Payment_Method.append(getinfo('li', "data-icon", "PostDynamicAttribute[Payment_Method]"))
                if len(price1)==0 or price1=='0.00':
                    price.append(np.NaN)
                else:
                    price.append(float(price1[0].text.replace(',','')))
                additions.append(list([i.text for i in soup.find_all('li', {"class":["fRight mb15", 'fRight mb15 latestParam']})]))
            else:
                break
        print(f'============================= {page} =============================')
    data = {'linkscar':linkscar, 'city': city, 'place':n, 'Brand':Brand, 'Brand_child':Brand_child, 'Car_Year':Car_Year, 'regional_specs':regional_specs, 'Tramsmission_Cars':Tramsmission_Cars, 'Fuel_Cars':Fuel_Cars, 'Car_Color':Car_Color, 'ConditionUsed':ConditionUsed, 'Kilometers_Cars':Kilometers_Cars, 'paint':paint, 'body_condition':body_condition, 'CarCustoms':CarCustoms, 'CarLicense':CarLicense, 'CarInsurance':CarInsurance, 'Payment_Method':Payment_Method, 'additions':additions, 'Date':date, 'price':price}
    data1 = pd.DataFrame(data)
    data2 = splitadds(data1)
    data3 = preprocessing(data2)
    saving(data3, main_data)