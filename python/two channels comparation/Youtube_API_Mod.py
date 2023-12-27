#!/usr/bin/env python
# coding: utf-8



import os
import pandas as pd
import googleapiclient.discovery
import requests
import json
from tqdm import tqdm, trange
import re
import math

path=os.path.join(os.getcwd(), "Data")
folder=os.path.join(path, "")


# Disable OAuthlib's HTTPS verification when running locally.

# *DO NOT* leave this option enabled in production.
#os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"


DEVELOPER_KEY = "put your api key here"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)


# In[ ]:
def gets_youtube(DEVELOPER_KEY):

    api_service_name = "youtube"
    api_version = "v3"


    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
    return youtube

def search_comments_per_page(youtube,video,page_token):
    
    """
    search comments from video in the respective page
    
    INPUT:
    youtube:Youtube googleapiclient session
    videoname: identification of the video
    page_token: token identification
    
    OUTPUT:
    response: the whole snippet from youtube
    
    """

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video,
        pageToken=page_token
    )
    response = request.execute()

    return response
def process_comments_response(response, video):
    
    """
    search comments from video in the respective page
    
    INPUT:
    response: the whole snippet from youtube
    videoname: identification of the video
    
    
    OUTPUT:
    next_page_token:token identification for next page
    result: dictionary of author and comment text
    
    """
    
    next_page_token = response.get('nextPageToken')
    result = []
    for i, item in enumerate(response["items"]):
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]  # Use Later
        comment_text = comment["snippet"]["textDisplay"]
        #video_id = video['video_id']
        #video_title = video['video_title']
        result.append(
            {
             #   'video_id': video_id,
             #   'video_title': video_title,
                'author': author,
                'comment_text': comment_text
            }
        )
        #logger.debug(f"Comment: {comment_text[:50]}... for {video_title}")

    return next_page_token, result

def read_comments(youtube,videoname,imax):
    """
    read the coments of a video from imax pages
    
    INPUT:
    youtube:Youtube googleapiclient session
    videoname: identification of the video
    imax: number of pages
    
    OUTPUT:
    comments: dictionary of author and comment text
    
    """
    next_page = None
    comments = []
    i=0
    #imax=15
    while True:
        response = search_comments_per_page(youtube, videoname, next_page)
        next_page, result = process_comments_response(response, videoname)
        comments += result
        #print(next_page)
        i=i+1
        if (not next_page) or (i>imax):
            break
            
    return comments

#if __name__ == "__main__":
#    main()


# In[ ]:





# In[2]:


def get_names(youtube,channel_id,imax):  
    
        """
        gets the video names and different public statistics from videos
    
        INPUT:
        youtube:Youtube googleapiclient session
        channel_id: identification of the channel
        imax: number of pages to look
    
        OUTPUT:
    
        videos: dictionary of video names with statistics
    
        """
        videos=[]
        next_page = None
        i=0

        next_page = None
        while True:
            i=i+1
            #gets the video names from a page in channel
            response = search_videos(youtube, channel_id, next_page)
            #proccess the response and gets statistics
            next_page, result = process_search_response(response)
            videos += result
            if not next_page:
                break
            if (not next_page) or (i>imax):
                break
        return videos


# In[ ]:


def search_videos(youtube, channel_id, page_token):
    
    
    """
    gets the video names response
    
    INPUT:
    youtube: Youtube googleapiclient session
    channel_id: identification of the channel
    page_token: token identification for page
    
    OUTPUT:
    
    response: dictionary of video names 
    
    """
    
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        type="video",
        pageToken=page_token
    )
    response = request.execute()
    #logger.debug("Received Video Search Response")
    return response


def process_search_response(response):
    
    """
    proccess the video names of the page and return them with statistics
    
    INPUT:
    
    response: dictionary of video names 
    
    OUTPUT:
    
    next_page_token: token identification for next page
    result: video names with statistics per page
    
    """
    
    next_page_token = response.get('nextPageToken')
    result = []
    for i, item in enumerate(response["items"]):
        video_id = item["id"]["videoId"]
        video_title = item['snippet']['title']
        description = item['snippet']['description']
        publishTime = item['snippet']['publishTime']
        #Gets the video statistics
        tags,vid_dur,statistic=videos_statistics(youtube, video_id)
        views= int(statistic['viewCount'])
        likes= int(statistic['likeCount']) 
        favorite= statistic['favoriteCount']
        comments= int(statistic['commentCount'])
        result.append({
            'video_id': video_id,
            'video_title': video_title,
            'publish_time': publishTime,
            'description': description,
            "tags":tags,
            "vid_dur_(sec)":vid_dur,
            "views":views,
            "likes":likes,
            "favorite":favorite,
            "comments":comments
        })
        #logger.debug(f"Received comment Search Response for {video_id} ")

    return next_page_token, result


def videos_statistics(youtube, video_id):
    
    """
    Gets the statistics of the video
    
    INPUT:
    
    youtube: Youtube googleapiclient session
    video_id: identification of the video
    
    OUTPUT:
    
    tags: tags of the video
    vid_dur: duration of the video
    statistics: statistics of the video
    
    """
    
    ##################################
    #gets the tags
    ##################################
    request = youtube.videos().list(
        part="snippet",#contentDetails,statistics",
        id=video_id,
        #type="video"
    )
    response = request.execute()
    tags=response["items"][0]["snippet"]["tags"]
    
    #logger.debug("Received Video Search Response")
    ##################################
    #gets the duration
    ##################################
    request = youtube.videos().list(
        part="contentDetails",#statistics",
        id=video_id,
        #type="video"
    )
    response = request.execute()
    
    vid_dur=response["items"][0]["contentDetails"]['duration'].replace("PT", "")
    vid_dur = vid_dur.replace("PT", "") 
    vid_dur = vid_dur.replace("S", "")
    vid_dur = vid_dur.replace("M", "*60+")
    vid_dur = vid_dur.replace("H", "*60*60+")
    vid_dur = vid_dur.replace("D", "*24*60*60+")
    vid_dur = re.sub("[+]$","", vid_dur)
    vid_dur=eval(vid_dur)
    ##################################    
    #gets the statistics
    ##################################
    request = youtube.videos().list(
        part="statistics",
        id=video_id,
        #type="video"
    )
    response = request.execute()
    
    
    
    
    statistics=response["items"][0]['statistics']
    #print(vid_dur)
    
    return tags,vid_dur,statistics


# In[ ]:





# In[ ]:
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
#
#
#   Old Stuff For GETTING VIDEOS FROM CHANNEL
#
#
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################




def get_video_data_channel_old(key,channel_id,pages,initoken=None):
    
    """
    gets the video names and different public statistics from videos
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    pages: number of pages to look
    
    OUTPUT:
    channel_videos:dictionary of video names with all data
    videosdic: dictionary of video names with statistics
    
    """
    
    
    
    channel_videos,npt=get_channel_videos_old(key,channel_id,50,pages,initoken)
    print("videos to load",len(channel_videos))
    videosdic=[]
    parts=["snippet","statistics","contentDetails"]
    for video_id in tqdm(channel_videos):
        data=get_single_video_data_old(key,video_id)
        for part in parts:
            #gets data for each part of the video
            #data=get_single_video_data(key,video_id,part)
            try:
                data1=data[part]
            except:
                print("error get single data")
                data1=dict()
    
            #data1=data[part]
            channel_videos[video_id].update(data1)
        #proccess the statistical data
        vid_data=procces_video_info_old(channel_videos[video_id],video_id)
        videosdic += vid_data
    video_data=channel_videos
    return channel_videos,videosdic,npt
            
            
def get_single_video_data_old(key,video_id):
    
    """
    gets the data for part
    
    INPUT:
    Key:api key
    video_id: identification of the video
    part: part of the statistics
    
    OUTPUT:
    
    data: dictionary of data for part 
    
    """
    
  
    #url=f"https://www.googleapis.com/youtube/v3/video?id={video_id}&part={part}&key={key}"
    #part=snippet&part=statistics&part=statistics
    url=f"https://www.googleapis.com/youtube/v3/videos?part=snippet&part=statistics&part=contentDetails&id={video_id}&key={key}"
    #print("llego")
    #print(url)
    #######################################
    #makes request to YT
    #######################################
    json_url=requests.get(url)
    data=json.loads(json_url.text)
    
    try:
        data=data["items"][0]#[part]
    except:
        print("error get single data")
        data=dict()
    return data



def procces_video_info_old(aux,nameid):
    
    """
    procces the statistical data from channel_videos dic
    
    INPUT:
    nameid: id of the video and key from channel_videos dic
    aux: channel_videos dic value correspondent to key

    OUTPUT:
    
    result: proccessed data statistics for video nameid
    
    """
    
    result=[]
    video_id=nameid
    video_tittle = aux['title']
    description = aux['description']
    publishTime = aux['publishedAt']
    
    vid_dur = aux['duration']
    #print(vid_dur,video_tittle,video_id)
    if vid_dur=="P0D":
        print("Video has 0 duration, probably not published livestream")
        print(vid_dur,video_tittle,video_id)
    vid_dur = vid_dur.replace("P0D", "0")
    #vid_dur = vid_dur.replace("PT", "") 
    vid_dur = vid_dur.replace("S", "")
    vid_dur = vid_dur.replace("M", "*60+")
    vid_dur = vid_dur.replace("H", "*60*60+")
    vid_dur = vid_dur.replace("DT", "*24*60*60+")
    vid_dur = vid_dur.replace("PT", "")
    vid_dur = vid_dur.replace("P", "")

    vid_dur = re.sub("[+]$","", vid_dur)
    vid_dur = eval(vid_dur)
    try:
        tags=aux["tags"]
    except:
        #print("No tags in video",video_tittle,video_id)
        tags=None   
    
    views= int(aux['viewCount'])
    likes= int(aux['likeCount'])
    favorite= int(aux['favoriteCount'])
    comments= int(aux['commentCount'])
    result.append({
            'video_id': video_id,
            'video_title': video_tittle,
            'publish_time': publishTime,
            'description': description,
            "tags":tags,
            "vid_dur_(sec)":vid_dur,
            "views":views,
            "likes":likes,
            "favorite":favorite,
            "comments":comments
        })
    return result


def get_channel_videos_old(key,channel_id,limit,maxpages,initoken):
    """
    gets the video names from channel all pages up to maxpage
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    limit:limit per page
    maxpages: number of pages to look
    
    OUTPUT:
    vid:names of all videos as dic keys and empty content
    npt: next page token
    """
    
    
    url=f"https://www.googleapis.com/youtube/v3/search?key={key}&channelId={channel_id}&part=id&order=date&maxResults={limit}"
    url1=url
    #print(url)
    
    if initoken:
        #print("initial token",initoken)
        url1=url+"&pageToken="+ initoken 
    
    
    vid,npt= get_channel_videos_per_page_old(key,channel_id,limit,url1)

    idx=0
    #print ("#################################################")
    #print (url)
    #print ("#################################################")
    
    while (npt is not None and idx < maxpages):
        nexturl=url+"&pageToken="+ npt
        

        next_vid,npt=get_channel_videos_per_page_old(key,channel_id,limit,nexturl)

        vid.update(next_vid)
        #print(npt)
        #print(vid)
        idx+=1
        #print("reading page",idx)
        #print(npt)
    return vid,npt

def get_channel_videos_per_page_old(key,channel_id,limit,url):
    """
    gets the video names from page
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    limit:limit per page
    url: number of pages to look
    
    OUTPUT:
    channel_videos:
    nextPageToken:  token for next page
    
    """
    #######################################
    #makes request to YT
    #######################################
    json_url= requests.get(url)
    #######################################
    data=json.loads(json_url.text)
    channel_videos=dict()
    if "items" not in data:
        return channel_videos, None
    item_data=data["items"]
    nextPageToken=data.get("nextPageToken",None)
    
    for item in item_data:
        try:
            kind=item["id"]["kind"] #
            if kind =="youtube#video":
                video_id=item["id"]["videoId"]
                channel_videos[video_id]=dict()
        except KeyError:
            print("error getting video per page")
             
    return channel_videos, nextPageToken


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
#
#
#   current Stuff For GETTING VIDEOS FROM CHANNEL from uploads playlist
#
#
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
def get_playlist_video_data(key,playid,channel_id,pages,initoken=None):
    
    """
    gets the video names and different public statistics from videos
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    pages: number of pages to look
    
    OUTPUT:
    channel_videos:dictionary of video names with all data
    videosdic: dictionary of video names with statistics
    
    """
    
    
    
    channel_videos,npt=get_playlist_videos_from_channel(key,playid,channel_id,50,pages,initoken)
    print("videos to load",len(channel_videos))
    videosdic=[]
    parts=["snippet","statistics","contentDetails"]
    for video_id in tqdm(channel_videos):
        data=get_single_video_data_old(key,video_id)
        for part in parts:
            #gets data for each part of the video
            #data=get_single_video_data(key,video_id,part)
            try:
                data1=data[part]
            except:
                print("error get single data")
                data1=dict()
    
            #data1=data[part]
            channel_videos[video_id].update(data1)
        #proccess the statistical data
        vid_data=procces_video_info_old(channel_videos[video_id],video_id)
        videosdic += vid_data
    video_data=channel_videos
    return channel_videos,videosdic,npt
            


def get_playlist_videos_from_channel(key,playid,channel_id,limit,maxpages,initoken):
    """
    gets the video names from playlist
    PLAYLIST
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    limit:limit per page
    maxpages: number of pages to look
    
    OUTPUT:
    vid:names of all videos as dic keys and empty content
    npt: next page token
    """
    #playid="UU"+channel_id[2:]
    url=f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults={limit}&playlistId={playid}&key={key}"
    
    url1=url
    #print(url)
    
    if initoken:
        #print("initial token",initoken)
        url1=url+"&pageToken="+ initoken 
    
    #hsta aca voy
    vid,npt= get_channel_videos_per_page(key,channel_id,limit,url1)

    idx=0
    #print ("#################################################")
    #print (url)
    #print ("#################################################")
    
    while (npt is not None and idx < maxpages):
        nexturl=url+"&pageToken="+ npt
        

        next_vid,npt=get_channel_videos_per_page(key,channel_id,limit,nexturl)

        vid.update(next_vid)
        #print(npt)
        #print(vid)
        idx+=1
        #print("reading page",idx)
        #print(npt)
    return vid,npt


def get_channel_videos(key,channel_id,limit,maxpages,initoken):
    """
    gets the video names from channel all pages up to maxpage from UPLOADS
    PLAYLIST
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    limit:limit per page
    maxpages: number of pages to look
    
    OUTPUT:
    vid:names of all videos as dic keys and empty content
    npt: next page token
    """
    playid="UU"+channel_id[2:]
    url=f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults={limit}&playlistId={playid}&key={key}"
    
    url1=url
    #print(url)
    
    if initoken:
        #print("initial token",initoken)
        url1=url+"&pageToken="+ initoken 
    
  
    vid,npt= get_channel_videos_per_page(key,channel_id,limit,url1)

    idx=0
    #print ("#################################################")
    #print (url)
    #print ("#################################################")
    
    while (npt is not None and idx < maxpages):
        nexturl=url+"&pageToken="+ npt
        

        next_vid,npt=get_channel_videos_per_page(key,channel_id,limit,nexturl)

        vid.update(next_vid)
        #print(npt)
        #print(vid)
        idx+=1
        #print("reading page",idx)
        #print(npt)
    return vid,npt

def get_channel_videos_per_page(key,channel_id,limit,url):
    """
    gets the video names from page of playlist
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    limit:limit per page
    url: number of pages to look
    
    OUTPUT:
    channel_videos:
    nextPageToken:  token for next page
    
    """
    #######################################
    #makes request to YT
    #######################################
    try:
        json_url= requests.get(url)
        data=json.loads(json_url.text)
    except:
        data=dict() # json.loads(json_url.text)
        print("failed api request")
    #json_url= requests.get(url)
    #######################################
    #data=json.loads(json_url.text)
    channel_videos=dict()
    if "items" not in data:
        return channel_videos, None
    item_data=data["items"]
    nextPageToken=data.get("nextPageToken",None)
    
    for item in item_data:
        try:
            kind=item["snippet"]["resourceId"]["kind"]
            if kind =="youtube#video":
                video_id=item["snippet"]["resourceId"]["videoId"]
                channel_videos[video_id]=dict()
        except KeyError:
            print("error getting video per page")
             
    return channel_videos, nextPageToken

def get_video_data_channel(key,channel_id,pages,initoken=None):
    
    """
    gets the video names and different public statistics from videos
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    pages: number of pages to look
    
    OUTPUT:
    channel_videos:dictionary of video names with all data
    videosdic: dictionary of video names with statistics
    
    """
    
    
    
    channel_videos,npt=get_channel_videos(key,channel_id,50,pages,initoken)
    print("videos to load",len(channel_videos))
    videosdic=[]
    parts=["snippet","statistics","contentDetails"]
    for video_id in tqdm(channel_videos):
        data=get_single_video_data_old(key,video_id)
        for part in parts:
            #gets data for each part of the video
            #data=get_single_video_data(key,video_id,part)
            try:
                data1=data[part]
            except:
                print("error get single data")
                data1=dict()
    
            #data1=data[part]
            channel_videos[video_id].update(data1)
        #proccess the statistical data
        vid_data=procces_video_info_old(channel_videos[video_id],video_id)
        videosdic += vid_data
    video_data=channel_videos
    return channel_videos,videosdic,npt
            
            
def get_single_video_data_old(key,video_id):
    
    """
    gets the data for part
    
    INPUT:
    Key:api key
    video_id: identification of the video
    part: part of the statistics
    
    OUTPUT:
    
    data: dictionary of data for part 
    
    """
    
  
    #url=f"https://www.googleapis.com/youtube/v3/video?id={video_id}&part={part}&key={key}"
    #part=snippet&part=statistics&part=statistics
    url=f"https://www.googleapis.com/youtube/v3/videos?part=snippet&part=statistics&part=contentDetails&id={video_id}&key={key}"
    #print("llego")
    #print(url)
    #######################################
    #makes request to YT
    #######################################
    json_url=requests.get(url)
    data=json.loads(json_url.text)
    
    try:
        data=data["items"][0]#[part]
    except:
        print("error get single data")
        data=dict()
    return data



def procces_video_info_old(aux,nameid):
    
    """
    procces the statistical data from channel_videos dic
    
    INPUT:
    nameid: id of the video and key from channel_videos dic
    aux: channel_videos dic value correspondent to key

    OUTPUT:
    
    result: proccessed data statistics for video nameid
    
    """
    
    result=[]
    video_id=nameid
    video_tittle = aux['title']
    description = aux['description']
    publishTime = aux['publishedAt']
    
    vid_dur = aux['duration']
    #print(vid_dur,video_tittle,video_id)
    if vid_dur=="P0D":
        print("Video has 0 duration, probably not published livestream")
        print(vid_dur,video_tittle,video_id)
    vid_dur = vid_dur.replace("P0D", "0")
    #vid_dur = vid_dur.replace("PT", "") 
    vid_dur = vid_dur.replace("S", "")
    vid_dur = vid_dur.replace("M", "*60+")
    vid_dur = vid_dur.replace("H", "*60*60+")
    vid_dur = vid_dur.replace("DT", "*24*60*60+")
    vid_dur = vid_dur.replace("PT", "")
    vid_dur = vid_dur.replace("P", "")

    vid_dur = re.sub("[+]$","", vid_dur)
    #print(vid_dur)
    vid_dur = eval(vid_dur)
    try:
        tags=aux["tags"]
    except:
        #print("No tags in video",video_tittle,video_id)
        tags=None   
    
    
    try:
        views= int(aux['viewCount'])
    except:
        print("No views",video_tittle,video_id)
        views= 0
    #likes= int(aux['likeCount'])
    try:
        likes= int(aux['likeCount'])
    except:
        #print("No likes",video_tittle,video_id)
        likes=0
    #favorite= int(aux['favoriteCount'])
    #comments= int(aux['commentCount'])
    try:
        favorite= int(aux['favoriteCount'])
    except:
        #print("No favorites",video_tittle,video_id)
        favorite=0
    try:
        comments= int(aux['commentCount'])
    except:
        #print("No comments",video_tittle,video_id)
        comments=0
    result.append({
            'video_id': video_id,
            'video_title': video_tittle,
            'publish_time': publishTime,
            'description': description,
            "tags":tags,
            "vid_dur_(sec)":vid_dur,
            "views":views,
            "likes":likes,
            "favorite":favorite,
            "comments":comments
        })
    return result


#####################################################
#####################################################
#####################################################
#####################################################

#optimized code

#####################################################
#####################################################
#####################################################
#####################################################

#channel and key 

###############

def add_channel(new_channel_name,new_channel_id):
    
    #loads
    f = open(folder+'channel_data.json')
    channels = json.load(f)
    

    channels[new_channel_name]=new_channel_id
    
    #saves
    with open(folder+'channel_data.json', 'w') as f:
        json.dump(channels, f)
    
    print("Channel added") 

def rem_channel(new_channel_name):
    
    #loads
    f = open(folder+'channel_data.json')
    channels = json.load(f)
    

    try:
        del channels[new_channel_name]
        print("Channel deleted")
    except:
        print("Channel ",new_channel_name," not in list")

    #saves
    with open(folder+'channel_data.json', 'w') as f:
        json.dump(channels, f)

        
def show_channel_list():
    #loads
    f = open(folder+'channel_data.json')
    channels = json.load(f)
    return channels.keys()


def show_channel_dict():
    f = open(folder+'channel_data.json')
    channels = json.load(f)
    return channels



###########
######################
##########################

def get_video_data_channel_opt(key,channel_id,pages,initoken=None):
    
    """
    gets the video names and different public statistics from videos on a channel
    
    INPUT:
    Key:api key
    channel_id: identification of the channel
    pages: number of pages to look
    initoken: token of initial page
    
    OUTPUT:
    channel_videos:dictionary of video names with all data
    videosdic: dictionary of video names with statistics
    npt:token of next page
    data0:unfiltered data from api
    
    """



    playid="UU"+channel_id[2:]
    
    
    return get_video_data_playlist(key,playid,pages,initoken=None)

def get_video_data_playlist(key,playid,pages,initoken=None):
    
    """
    gets the video names and different public statistics from videos on a playlist
    
    INPUT:
    Key:api key
    playlist_id: identification of the playlist
    pages: number of pages to look
    initoken: token of initial page
    
    OUTPUT:
    channel_videos:dictionary of video names with all data
    videosdic: dictionary of video names with statistics
    npt:token of next page
    data0:unfiltered data from api
    
    """
    
    #playid="UU"+channel_id[2:]
    #Gets the list of videos from the public playlist of the channel
    channel_videos,npt=get_channel_videos_opt(key,playid,50,pages,initoken)
    
  #  print ("#################################################")
    print ("#################################################")
    print("videos to load",len(channel_videos))
    print ("#################################################")
    videosdic=[]
    #define search parameters
    parts=["snippet","statistics","contentDetails","topicDetails"]
    
    #make a string for the list of all videos in videolist and the search parameters on partslist
    videolist=""
    for video_id in channel_videos:
        videolist=videolist+video_id+"%2C"
    partslist=""
    for part in parts:
        partslist=partslist+part+"%2C"
    ########################################
    #select firts 50 videos
    ###########################
    partslist=partslist[0:-3] # eliminates useless characters for search
    unit=14*50  #length of string for the firts 50 videos
    number=math.ceil(len(videolist)/unit) #get the number of 50 groups in videolist

    data0={}
    #for i in trange(number, desc='Progress on 50 video pages'):
    for i in range(number):
           ########################################
        #select firts 50 videos
    
        videolist1=videolist[i*unit:(i+1)*unit] #gets the first 50 videos
        videolist1=videolist1[0:-3]# eliminates useless characters for search
    

        urlll= f"https://youtube.googleapis.com/youtube/v3/videos?part={partslist}&id={videolist1}&key={key}"
        json_url= requests.get(urlll)
        #######################################
        data0=json.loads(json_url.text)
    
    
        for i in range(len(data0["items"])):
    
            data=data0["items"][i]
            for part in parts:
                #gets data for each part of the video
                #data=get_single_video_data(key,video_id,part)
                try:
                    data1=data[part]
                except:
                    print("error get single data from ", part," in ",data["id"])
                    data1=dict()
    
            #data1=data[part]
                video_id=data["id"]
                channel_videos[video_id].update(data1) #updates dictionary
            #proccess the statistical data
            vid_data=procces_video_info_old_opt(channel_videos[video_id],video_id) #proccess data from dictionary
            videosdic += vid_data # add data from video to all videos data
        ########################################    
        
    video_data=channel_videos
    
    
    return channel_videos,videosdic,npt,data0


def get_channel_videos_opt(key,playid,limit,maxpages,initoken):
    """
    gets the video names from channel all pages up to maxpage from a PLAYLIST
    
    INPUT:
    Key:api key
    playid: identification of playlist
    limit:limit per page
    maxpages: number of pages to look
    initoken: token of initial page
    
    OUTPUT:
    vid:names of all videos as dic keys and empty content
    npt: next page token
    """
    #url for the api query to get video names
    url=f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults={limit}&playlistId={playid}&key={key}"
    
    url1=url
    #print(url)
    
    if initoken:
        #add initial page to query
        url1=url+"&pageToken="+ initoken 
    
    #gets the query for the fist page
    vid,npt= get_channel_videos_per_page_opt(key,limit,url1)

    idx=0
    #print ("#################################################")
 
    #print ("#################################################")
    #print ("#################################################")
   # print("    ")
    #print("Reading ",maxpages," pages of videos")
    #print("    ")
    #print ("#################################################")
    #pbar = tqdm(total = maxpages+1)
    #loops over pages to get all videos   
    while (npt is not None and idx < maxpages):
        nexturl=url+"&pageToken="+ npt
        

        next_vid,npt=get_channel_videos_per_page_opt(key,limit,nexturl)

        vid.update(next_vid)
        #print(npt)
        #print(vid)
        idx+=1
        #pbar.update(1)
        #print("reading page",idx)
        #print(npt)
    #pbar.close()
    #print("    ")
   # print(idx," pages of videos readed")
   # print("    ")    
   # print ("#################################################")
   # print ("#################################################")
    
    
    
    
    return vid,npt

def get_channel_videos_per_page_opt(key,limit,url):
    """
    gets the video names from page of playlist and return them alongside token of next page
    
    INPUT:
    Key:api key
    limit:limit per page
    url: number of pages to look
    
    OUTPUT:
    channel_videos:
    nextPageToken:  token for next page
    
    """
    #######################################
    #makes request to YT
    #######################################
    try:
        json_url= requests.get(url)
        data=json.loads(json_url.text)
    except:
        data=dict() # json.loads(json_url.text)
        print("failed api request")
    #json_url= requests.get(url)
    #######################################
    #data=json.loads(json_url.text)
    channel_videos=dict()
    if "items" not in data:
        return channel_videos, None
    item_data=data["items"]
    nextPageToken=data.get("nextPageToken",None)
    
    for item in item_data:
        try:
            kind=item["snippet"]["resourceId"]["kind"]
            if kind =="youtube#video":
                video_id=item["snippet"]["resourceId"]["videoId"]
                channel_videos[video_id]=dict()
            if kind =="youtube#liveStream":
                video_id=item["snippet"]["resourceId"]["videoId"]
                channel_videos[video_id]=dict()
                #print("Loaded a YT livestream ",video_id)
        except KeyError:
            print("error getting video per page")
             
    return channel_videos, nextPageToken

def procces_video_info_old_opt(aux,nameid):
    
    """
    proccess the statistical data from channel_videos dic
    
    INPUT:
    nameid: id of the video and key from channel_videos dic
    aux: channel_videos dic value correspondent to key

    OUTPUT:
    
    result: proccessed data statistics for video nameid
    
    """
    
    result=[]
    video_id=nameid
    video_tittle = aux['title']
    description = aux['description']
    publishTime = aux['publishedAt']
    
    vid_dur = aux['duration']
    #change the format of vid_dur to seconds
    if vid_dur=="P0D":
        print("Video has 0 duration, probably is a not published livestream")
        print(vid_dur,video_tittle,video_id)
    vid_dur = vid_dur.replace("P0D", "0")
    #vid_dur = vid_dur.replace("PT", "") 
    vid_dur = vid_dur.replace("S", "")
    vid_dur = vid_dur.replace("M", "*60+")
    vid_dur = vid_dur.replace("H", "*60*60+")
    vid_dur = vid_dur.replace("DT", "*24*60*60+")
    vid_dur = vid_dur.replace("PT", "")
    vid_dur = vid_dur.replace("P", "")

    vid_dur = re.sub("[+]$","", vid_dur)
    #print(vid_dur)
    vid_dur = eval(vid_dur)
    try:
        tags=aux["tags"]
    except:
        #print("No tags in video",video_tittle,video_id)
        tags=None   
    
    
    try:
        views= int(aux['viewCount'])
    except:
        print("No views",video_tittle,video_id)
        views= 0
    #likes= int(aux['likeCount'])
    try:
        likes= int(aux['likeCount'])
    except:
        #print("No likes",video_tittle,video_id)
        likes=0
    #favorite= int(aux['favoriteCount'])
    #comments= int(aux['commentCount'])
    try:
        favorite= int(aux['favoriteCount'])
    except:
        #print("No favorites",video_tittle,video_id)
        favorite=0
    try:
        comments= int(aux['commentCount'])
    except:
        #print("No comments",video_tittle,video_id)
        comments=0
        
##############################    
    try:
        thumbnails= aux['thumbnails']['high']["url"]
    except:
        #print("No thumbnails",video_tittle,video_id)
        thumbnails="None"       
        #snippet.thumbnails
        #data0["items"][1]["snippet"]['thumbnails']['high']["url"]
        
#########################################
    result.append({
            'video_id': video_id,
            'video_title': video_tittle,
            'publish_time': publishTime,
            'description': description,
            "tags":tags,
            "vid_dur_(sec)":vid_dur,
            "views":views,
            "likes":likes,
            "favorite":favorite,
            "comments":comments,
            "thumbnails":thumbnails
        })
    return result