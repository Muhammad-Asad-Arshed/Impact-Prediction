# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 21:28:48 2019

@author: Maharvi
"""
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from time import sleep
import pandas as pd
import pandas as pdf
import pandas as pdr
import re
from textblob import TextBlob
import preprocessor as p
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from pywsd.utils import lemmatize, lemmatize_sentence
from langdetect import detect
import pytz
from datetime import datetime,timedelta
#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
df = pd.DataFrame(columns=['Text','GMTTweetDate','Sentiment','PreDayRate','CurrentDayRate','Status'])
twu = ['@Jhagra','@ZainHQ','@HashimJBakht','@Asad_Umar','@Hammad_Azhar','@ImranKhanPTI','@SMQureshiPTI','@ShehryarAfridi1','@SaleemMandvi','@MiftahIsmail','@ArifAlvi','@CMShehbaz','@1sakhtar','@pid_gov','@FinMinistryPak','@StateBank_Pak']
for tu in twu:     # by item
 k=str(tu)
 for status in tweepy.Cursor(api.user_timeline, screen_name=k, tweet_mode="extended").items():
# Convert tweet pakistan time to GMT time zone
   print(status.user)
   m=datetime.strptime(str(status.created_at), '%Y-%m-%d %H:%M:%S')
   mytimezone=pytz.timezone("Asia/Karachi") #my current timezone
   dtobj4=mytimezone.localize(m)        #localize function
   gm=dtobj4.astimezone(pytz.timezone("GMT")) #astimezone method 
   gm=str(gm).replace("+00:00",'')
   gmt=datetime.strptime(str(gm), '%Y-%m-%d %H:%M:%S')
   if(str(gmt).find("2018")>=0 or str(gmt).find("2017")>=0 or str(gmt).find("2016")>=0 or str(gmt).find("2015")>=0 or str(gmt).find("2014")>=0 or str(gmt).find("2013")>=0):
    #Preprocess Tweets
     p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.MENTION,p.OPT.HASHTAG,p.OPT.RESERVED,p.OPT.EMOJI,p.OPT.SMILEY)
     prep=p.clean(str(status.full_text))
     prep = re.sub(r"&amp;", "and", prep)
     #check preprocess tweet is in english or not
     try:
        k=detect(prep)
     except:
        k="Not"
     if(k=='en'):
     #Removing Stop words
      stop_words = set(stopwords.words('english')) 
      word_tokens = word_tokenize(prep) 
      filtered_sentence = [w for w in word_tokens if not w in stop_words] 
      filtered_sentence = [] 
      for w in word_tokens: 
        if w not in stop_words: 
         filtered_sentence.append(w) 
      prep=" ".join(str(p) for p in filtered_sentence)
      synonyms=[]
      prep=lemmatize_sentence(prep)
      prep =" ".join(str(e) for e in prep)    
      #word that has more than 1 length 
      prep = ' '.join([w for w in prep.split() if len(w)>1])           
      a=0
      dff = pdf.read_excel("finance_keywords.xlsx")
      for x in dff['financewords']:
        lw=lemmatize_sentence(x)
        lws=" ".join(str(p) for p in lw)
        if(prep.find(lws)!=-1):
             a=1; 
        else:       
          for syn in wordnet.synsets(lws): 
            for l in syn.lemmas(): 
              synonyms.append(l.name()) 
          for w1 in prep:
            for xn1 in synonyms:
              if(w1==xn1):
                 a=1;
      synonyms = []    
      if(a==1):
     #Procedure for finding sentiment
       ex = TextBlob(prep)
       analysis = ex
       s=2;
       if(analysis.sentiment[0]>0):
          s=1
       elif (analysis.sentiment[0]<0):
          s=-1
       else:
          s=0
   #Tweets pre and current rate
       prcr=(gmt-timedelta(days=1)).date().strftime('%A %d %B %Y')
       #Rates
       dfr = pdr.read_excel("Rates.xlsx")
       df2=dfr.loc[dfr['Date']==prcr]
       if(df2.empty):
           prerate='0.0000 PKR'
       else:
           prerate=df2["Rate"].values[0]  
         #Current Rate
       df4=dfr.loc[dfr['Date']==gmt.date().strftime('%A %d %B %Y')]
       if(df4['Date'].empty):
            c='0.0000 PKR'
       else:
            c=df4["Rate"].values[0]
    #finding status
       c=c.replace("PKR",'')
       pr=prerate.replace("PKR",'')
       cur=float(c)
       pre=float(pr)
      
       if((cur-pre)>0):
           stat="Increase"
       elif((cur-pre)<0):
           stat="Decrease"
       else:
           stat="No Change"
    
#Conert datetime to date and format like that Monday 31 December 2018
       df = df.append({'Text': prep,'GMTTweetDate': (gmt.date().strftime('%A %d %B %Y')),'Sentiment':s,'PreDayRate':pre,'CurrentDayRate':cur,'Status':stat}, ignore_index=True)
       print(prep)
# Create a Pandas Excel writer using XlsxWriter as the engine.
       writer = pd.ExcelWriter('IntialDataSet.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
       df.to_excel(writer, sheet_name='Sheet1')
# Get the xlsxwriter workbook and worksheet objects.
       workbook  = writer.book
       worksheet = writer.sheets['Sheet1']

# Add some cell formats
       format1= workbook.add_format({'num_format':'0'})
       format2 = workbook.add_format({'num_format':'0.0000'})
       format3=workbook.add_format()

# Note: It isn't possible to format any cells that already have a format such
# as the index or headers or any cells that contain dates or datetimes.
# Set the column width and format.
       worksheet.set_column('B:B', 100, format3)
       worksheet.set_column('C:C', 30, format3)
       worksheet.set_column('D:D', 15, format1)
       worksheet.set_column('E:E', 15, format2)
       worksheet.set_column('F:F', 15, format2)
       worksheet.set_column('G:G', 15, format3)           
      else:
        print("Not Relevevent")
     else:
        print("Tweet is not in full english")
   else:
        print("Ignore Tweet Except than 2018,2017,2016,2015,2014,2013 Tweets or of urdu words tweets")  
print('Thanks Check File Now') 
# Close the Pandas Excel writer and output the Excel file.
writer.close()  