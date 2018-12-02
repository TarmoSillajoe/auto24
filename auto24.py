
# coding: utf-8

# In[372]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup


# **Scrape results list excluding detailviews**

# In[373]:


def get_car_features(element, mylist):
    
    """Returns the car's features as nested list"""

    car_instance = element.findChild('td',attrs={"class":"make_and_model"})
    
    #Find ad's id
    ad_link = car_instance.findChild('a')
    mylist[0].append(str(ad_link.attrs).split('/')[2].strip("}").strip("'"))
    
    #Find car description
    mylist[1].append(ad_link.get_text())
    
    #Production year
    year_td = car_instance.find_next_sibling('td',attrs={'class':'year'})
    mylist[2].append(year_td.get_text())
    
    #Fuel
    mylist[3].append(car_instance.find_next_sibling('td',attrs={'class':'fuel'}).get_text())
    
    #Transmission
    mylist[4].append(car_instance.find_next_sibling('td',attrs={'class':'transmission'}).get_text())
    
    #Price
    mylist[5].append(car_instance.find_next_sibling('td',attrs={'class':'price'}).get_text())


# In[374]:


def scrape_page(url):
    
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')

    mylist=[[], # id
        [], # car description
        [], # production year
        [], # fuel
        [], # transmission
        [], # Price
       ] 
    mytable = soup.find('table',attrs={'id':'usedVehiclesSearchResult'})
    result_rows = mytable.findChildren('tr',attrs={'class':re.compile(fr"result-row item-.")})
    for row in result_rows:
        get_car_features(row,mylist)   
    df = pd.DataFrame(mylist)
    transposed = df.transpose()
    return transposed


# In[375]:


def click_next(driver):   
    try:
        myelement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "next-page"))                                
        )
        myelement.click()
    except:
        print('Did not find the element.')


# In[376]:


import time
timeout = time.time() + 60*1 
dataframes=[]

url = "https://www.auto24.ee/kasutatud/nimekiri.php?bn=2&a=101&aj=&f1=2018&g2=12000&k1=60&ae=2&af=50&ag=0&ag=1&otsi=otsi"
# driver = webdriver.Firefox()
# driver.get(url)

#nextlink = soup.find('a',attrs={'class':"input-link item","rel":"next"})
#url = "https://www.auto24.ee/" + nextlink.attrs.get('href')

has_nextpage=True
while(has_nextpage):
    dataframes.append(scrape_page(url))
    
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    
    nextlink = soup.find('a',attrs={'class':"input-link item","rel":"next"})
    has_nextpage = bool(nextlink)
    if has_nextpage:
        url = "https://www.auto24.ee/" + nextlink.attrs.get('href')


# while True:
#     dataframes.append(scrape_page(soup)
#     if bool(not soup.find('div',attrs={'class':'next-page'})) or time.time() > timeout:
#         break
    
#     click_next(driver)


# In[377]:


df_all = pd.concat(dataframes,ignore_index=True)
df_all.columns = ['id', 'description', 'year','fuel','gearbox','price']
df_all['id'] = pd.to_numeric(df_all['id'])
df_all.dtypes


# In[378]:


type(df_all.iloc[0,0])


# In[379]:


def scrape_detailview(id_string, list_in):
    url = 'https://www.auto24.ee/used/' + id_string
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    
    list_in[0].append(str(id_string))
    body_type = np.nan
    manuf_date = np.nan
    km = np.nan

    main_data = soup.find('table',attrs={"class":"section main-data"})
    
    if main_data:
        tr_body = main_data.findChild('tr',attrs={'class':'field-keretyyp'})
        tr_date = main_data.findChild('tr',attrs={'class':'field-month_and_year'})
        tr_km = main_data.findChild('tr',attrs={'class':'field-labisoit'})
        
    body_type = tr_body.findChild('span',attrs={'class':'value'}).get_text() if tr_body else body_type
    manuf_date = tr_date.findChild('span',attrs={'class':'value'}).get_text() if tr_date else manuf_date
    km = tr_km.findChild('span',attrs={'class':'value'}).get_text() if tr_km else km
        
    list_in[1].append(body_type)
    list_in[2].append(manuf_date)
    list_in[3].append(km)


# In[380]:


adslist = [[], #0 id
          [], #1 body_type
          [], #2 manufacturing date
          []  #3 kilometers driven
         ]

for adid in list(df_all['id']):
    scrape_detailview(str(adid), adslist)


# In[381]:


pd.options.display.max_rows = 999
df_ads = pd.DataFrame(adslist).transpose()
df_ads.columns = ['id','body','man_date','km']
df_ads['id'] = pd.to_numeric(df_ads['id'])
df_ads.head()


# In[382]:



df_all.head()
# df_all.drop_duplicates(subset=['id'],inplace=True)
# df_ads.drop_duplicates(subset=['id'],inplace=True)


# In[383]:


df = df_ads.merge(df_all,how='left',on=['id'])


# In[384]:


df.head()


# In[385]:


df['model'] = df['description'].apply(lambda x: x.split(' ')[1])
df['manufacturer'] = df['description'].apply(lambda x: x.split()[0])

df.head(3)


# In[390]:


mypattern = re.compile('(^\d{2,3} ?\d*)')


# In[391]:


matchobject = mypattern.findall('19 000 sis. KM')[0]
entries = re.search('(^\d{2,3} ?\d{3})','11 900 sis. KM')
#entries.group(0)
(matchobject)


# In[392]:


import unicodedata
#new_str = unicodedata.normalize("NFKD", unicode_str)
df['km'].fillna("0", inplace=True)
df['km']= df['km'].apply(lambda x: unicodedata.normalize("NFKD",str(x)))
df['km']= df['km'].apply(lambda x: str(x).strip(' km').replace(' ',''))
df['km'] = pd.to_numeric(df['km'])


# In[401]:


mypattern = re.compile('(^\d{2,3} ?\d*)')
df['price']= df['price'].apply(lambda x: unicodedata.normalize("NFKD",str(x)))
df['price'] = df['price'].apply(lambda x: mypattern.findall(x)[0].replace(" ",""))
df['price']=pd.to_numeric(df['price'])
df['price'].unique()


# In[ ]:


df['year'] = pd.to_numeric(df['year'])
df.dtypes


# In[ ]:


df.sort_values('description', inplace=True)
df.head()


# In[ ]:


df[df['manufacturer']=='Volkswagen']


# In[ ]:


df[df['year']==2011].groupby(['manufacturer','model']).count()


# In[ ]:


df[(df['year']==2009) 
   & (df['manufacturer']=='Ford')]['km'].plot.hist(bins=20)


# In[ ]:


df[['manufacturer','model']].value_counts()

