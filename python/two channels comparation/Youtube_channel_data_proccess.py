#!/usr/bin/env python
# coding: utf-8



import os
import pandas as pd
import json
import re
import math

from datetime import date
from datetime import datetime
import Youtube_API_Mod as YAM # Module developed by victor


path=os.path.join(os.getcwd(), "Data")
folder=os.path.join(path, "")


# Disable OAuthlib's HTTPS verification when running locally.

# *DO NOT* leave this option enabled in production.
#os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"





# In[ ]:
def print_info(df):
    
    """
    prints a summary of the data such as:
    total views, likes, comments
    mean vid duration
    number of published videos and mean views per video
    
    Top 5 videos in views with views%
    """
    dfout=df.copy()
    #calculates 
    published_vid=dfout["views"].count()
    sumcols=["views","likes","comments"]
    meancols=["vid_dur_(sec)"]#,"tags_length"]
    print("########################################")
    print("suma")
    for col in sumcols:    
        print(col,dfout[col].sum())
    print("########################################")
    print("             \t","mean","  ","std")
    for col in meancols: 
        print(col+"\t",round(dfout[col].mean(),0),round(dfout[col].std(),0))
    print("########################################")
    print("number of published videos",published_vid)
    print("views per video",round(dfout["views"].mean(),1))
    #print("views per video std",dfout["views"].std().round(1))
    print("########################################")
    print("Top 5 videos in views")
    dfout2=dfout.sort_values(by='views', ascending=False)#.head(5)
    number=5
    print("...................")
    totviews=dfout["views"].sum()
    for x in range(number):
        print(dfout2.video_title[x])
        print("Vistas:",dfout2["views"][x],"\t\t",str(round((100*dfout2["views"][x]/totviews),2))+"%")
        print("Link:","https://www.youtube.com/watch?v="+dfout2["video_id"][x])
        print("...................")
    return
    #print(dfh[top_col][x])
    #print(dfh[top_col+" %"][x])
    
    
def proccess_data(name,pages,save,DEVELOPER_KEY):

    """
    Uses the YAM library to get the public videos data from a channel and proccess the data into a
    dataframe
    
    Input:
    name: channel name (must be inside the list of channels from YAM.show_channel_dict(), new channels can be added with YAM.add_channel )
    pages: number of pages (total videos= 50*(pages+1))
    save: if 1 saves to a csv file in scrapped_data folder
    DEVELOPER_KEY: api key
    
    """
    
    channels=YAM.show_channel_dict()
    channel_id=channels[name]
    channel_id
    npt=None

    
    cs,vids,npt,data0=YAM.get_video_data_channel_opt(DEVELOPER_KEY,channel_id,pages,npt)

    video_names=pd.DataFrame.from_dict(vids)#100+494+594+594+594+591 murio
    video_names.publish_time=pd.to_datetime(video_names["publish_time"])
    
    video_names.sort_values(by=['publish_time'])
    video_names.tags.fillna("",inplace=True)

    if save==1 :
        today=datetime.today().strftime('%Y_%m_%d')
        num="_"+str(len(video_names))+"_"
        folder="scrapped_data/"
        filename=name+num+today+".csv"
        video_names.to_csv(folder+filename)
        filename

    
    video_names.tags.fillna("",inplace=True)
    df=video_names
    aux=df.tags.apply(len)
    df["tags_length"]=aux
    df.publish_time=pd.to_datetime(df["publish_time"])
    df = df.set_index("publish_time")
    #name="channelname"
    df['vid_dur_(min)']=df['vid_dur_(sec)']/60
    
    
    
    
    # this stuff might change due to possible actualizations in pandas or in datetime data
    df=df.reset_index()
    df['publish_time']=df['publish_time'].dt.tz_localize(None)
    #df=df.reset_index()

    return df

def print_basic_info_channel(channel2,df2,inidate1,enddate1,show):
    
    """
    print information of the channel for a selected date range such as total views,top videos etc.
    
    Input:
    channel2: channel name 
    df2: dataframe with the data
    inidate1: initial date
    enddate1: final date
    show: name of an specific show to study
    
    """
    print(channel2)
    mask = (df2['publish_time'] > inidate1) & (df2['publish_time'] <= enddate1) 


    din2=df2.loc[mask]
    din2.set_index('publish_time', inplace = True)


    
    din2["video_title"]=din2["video_title"].str.lower()

    mask1=din2['description'].str.contains(show)
    mask2=din2["video_title"].str.contains(show)
    din2[mask1]


    print(show," tuvo ",din2[mask1 | mask2]["views"].sum()," visualizaciones.")


    print_info(din2.copy())
    
    return

def normalize(s):
    """
    
    """
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s