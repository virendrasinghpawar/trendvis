import facebook
# from rake_nltk import Rake
import urllib.request, urllib.error, urllib.parse
import json
import re
from datetime import datetime
from googletrans import Translator
import uuid
import requests
import siteAnalyze


# page_id="1327038517331134"
# access_token="EAAGKRLDmUpIBALxr02yGvYkUJZCeIQCXHdJzrKg346UO4VZCnDPONoqtB1UvpxEP3sB3AdaYApbzuhFXZC2A0rUFzFFgWwmpAC4HOr0oZAYxiXF9sR91g57eZBPTFdjupuwwu7cMzKXZChNbXSW4yWcFG6rZA27ZCmqTLYqXLz8nZA0rCtbigRGWW"

def request_until_succeed(url):
    # req = requests.request("GET",url)
    # response=requests.request("GET",url)
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try: 
            # response=json.loads(response.content.decode('utf-8'))
            response = urllib.request.urlopen(req)
            
            if response.getcode() == 200:
                success = True
        except Exception as e:
            return "nothing"
            print(e)
            # time.sleep(5)
            
            print("Error for URL %s: %s" % (url, datetime.datetime.now()))

    # print(json.loads(response.read()))
    return response.read().decode('utf-8')


def testFacebookPageFeedData(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.7"
    node = "/" + page_id + "/posts?fields=id,created_time,message,link,story&since=2018-01-1&limit=100" 
    parameters = "&access_token=%s" % access_token
    url = base + node + parameters
    
#  "https://graph.facebook.com/v2.11/186123565075095?fields=posts.limit(2)&access_token=EAACEdEose0cBAF4iFH4ZCAOSpbuL91UPEpUjtBn5FZCWgZA1bDsIvzAUBz8wWO2ggaqr8xRz6W05oX1SG5yxMZAZBBsO43l1vWWf7ZC6OWlYDyYwYkMhhRckmygXgk3Und5EXJCJG3XOJr7YxqjZCXXVS64Y3LjdJKRNsQuhcFUSdd6CJHgjdz4GHWsi93E9pYSQaZCzJ2YMlAZDZD"
    # retrieve data
    data = request_until_succeed(url)

    # print data
    # return
    # print data['paging']['next']
    # return
    next=True
    
    if data != "nothing":
        data=json.loads(request_until_succeed(url))
        # file = open("message.txt", "w")
        while next:
            
            # print data
            for dt in data['data']:
                # message=" "
                # pass
                # print dt['message']
                # if 'link' in dt:
                date=dt['created_time']
                print(dt['id'])
                print(dt['created_time'])
                date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+0000')
                # print(date.month,date.hour)
                time=date.hour
                month=date.month
                    
                message=" "
                # if 'message' in dt:
                    # print dt['message']
                    # message=message+dt['message']
                    # file.write(dt['message'])
                    # print(dt['created_time'])
                    # print(message)
                # if 'story' in dt:
                    # print dt['message']
                    # file.write(dt['story'])
                    # message=message+dt['story']
                    # print(message)

                #     # date.split()
                if 'link' in dt:   
                    print('link',dt['link']) 
                    
                    if 'wittyfeed.com' in dt['link']:
                        story_id=dt['link'].split('/')[4]
                        url="https://api.wittyfeed.com/Sdk/storyFrame?story_id="+str(story_id)
                        response=requests.request("GET",url)
                        res=json.loads(response.content.decode('utf-8'))
                        if 'story'in res['result']:
                            story=res["result"]["story"]
                            title=story["story_title"]
                            message=message+title
                            # print(title)
                        # print(message)
                        # translator = Translator()
                            translator = Translator(service_urls=[
                                'translate.google.com',
                                'translate.google.co.in',
                                ])
                            
                            emoji_pattern = re.compile("["
                                    u"\U0001F600-\U0001F64F"  # emoticons
                                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                                    "]+", flags=re.UNICODE)
                            message=emoji_pattern.sub(r'', message)
                            #tr=translator.translate(message)
                            #message=tr.text
                            # print("message",message)
                            # getStoryId=dt['link'].split('/')[4]
                            params={
                                "page_id":page_id,
                                "time":time,
                                "month":month,
                                "postScore":getPostScore(dt['id'],access_token),
                                "keywords":siteAnalyze.pageKeywords(message)

                            }
                            # print("1",params)
                            # print("2",message)
                            # print("3",time,month)
                            print(params)
                            updateDB(params)

                    # response=updateDB(params)
                    # print(response,"put to ES")
                    # print(getStoryId)

                        
                        
            # print('next' in data['paging'])
            
            if 'paging' in data:
                if 'next' in data['paging']:
                    # print(data['paging']['next'])
                    url= data['paging']['next']
                    data = json.loads(request_until_succeed(url))
                else:
                    print("end of the story")

                    return "ok"    
            else:
                return "ok";
         
    else:
        # print("nothing here") 
        return "nothing"
        # file = open("message.txt", "w")   

    
def updateDB(params):

    url = "https://search-viral9-ww2w3fk7uhagdcrjfebkamzp4y.us-east-1.es.amazonaws.com/feed_new/page_keywords/_search"
    headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
         }
    payload={
                "size":10,
                "query": {
                    "bool": {
                    "must": [
                        {
                        "match": {
                            "month": params['month']
                        }
                        },{
                        "match": {
                            "time": params['time']
                        }
                        },{
                        "bool": {
                            "should": [
                            
                            {
                                "match": {
                                "page_id":params['page_id']
                                }
                            
                            }
                            ]
                        }
                        }
                        
                    ]
                    }
                }
    }
            
    payloadNew=json.dumps(payload)
    
    # print(payloadNew)
    response = requests.request("GET", url, data=payloadNew, headers=headers)
    # print(response.text)
    responseJSON=json.loads(response.text)['hits']['hits']
    if not responseJSON:
        print("i am new")
        id=uuid.uuid4().hex
        url = "https://search-viral9-ww2w3fk7uhagdcrjfebkamzp4y.us-east-1.es.amazonaws.com/feed_new/page_keywords/"+id
        keylist=[]
        for keyword in params['keywords']:
            obj={
                "key":keyword,
                "value":params['postScore'],
                "count":1
            }
            keylist.append(obj)
            
        payload={
                    "page_id":params['page_id'],
                    "time":params['time'],
                    "month":params['month'],
                    "comments":keylist

        }
                
        payloadNew=json.dumps(payload)
        # print(payloadNew)

        response = requests.request("PUT", url, data=payloadNew, headers=headers)
        # print(response)
        return response
    else:
        # print("it matches with me and i am merging")
        id=responseJSON[0]['_id']
        source=responseJSON[0]['_source']
        url = "https://search-viral9-ww2w3fk7uhagdcrjfebkamzp4y.us-east-1.es.amazonaws.com/feed_new/page_keywords/"+id
        # postCount=source['count']+1
        # print(source['comments'])
        # return "i am affraid whoilla"
        for keyword in params['keywords']:
            iter=True
            count=0
            while iter:
                if count==(len(source['comments'])):
                    iter=False
                    print("not finding and appending keyword")
                    ob={
                        "key":keyword,
                        "value":params['postScore'],
                        "count":1
                        }
                        
                    source['comments'].append(ob)
                elif keyword == source['comments'][count]["key"]:
                    tempObj=source['comments'][count]
                    tempObj["value"]=((tempObj["value"]*tempObj["count"])+params['postScore'])/(tempObj["count"]+1)
                    tempObj["count"]=tempObj["count"]+1
                    source['comments'][count].update(tempObj)
                    iter=False
                # else:
                    # print("how can i come here howw")
                    # iter=False    
                count=count+1

                
        payload={
                    "page_id":params['page_id'],
                    "time":params['time'],
                    "month":params['month'],
                    "comments":source['comments']

        }
                
        payloadNew=json.dumps(payload)
        # print(payloadNew)

        response = requests.request("PUT", url, data=payloadNew, headers=headers)
        # print("else response",response)

    return response


# def postKeywords(message):
#     r = Rake() 

#     r.extract_keywords_from_text(message)

#     words=r.get_ranked_phrases()
#     print("words",words)
#     return words




def getPostScore(post_id,access_token):

    # access_token="EAACEdEose0cBAB2HFJIbZClW6SQXBc4gckhWqEM8QeGsOWgpGXCvF0LRCC47TdJGPCPlwwOfedwcS1isuxEnw0ZCB3AYTh6yPHKZCP2sVmqVurYIqDLgaE1QbeLUNA2y2lXzTIZAE75CsZBHA1zJcFy4sPBZA2EtZBcbZAsdtjkOIF0GXzq931XfA74ysedSq1F7g2OOl00KJgZDZD"
    graph = facebook.GraphAPI(access_token=access_token, version="2.7")

    # post_id="1290804767700294_1600353303412104"
    fields='''
    created_time,insights.metric(post_reactions_by_type_total).period(lifetime).as(post_reactions_by_type_total),shares.summary(true).limit(0),comments.summary(true).limit(0),insights.metric(post_impressions_unique).period(lifetime).as(post_impressions_unique),insights.metric(post_negative_feedback).period(lifetime).as(negative_feedback),insights.metric(post_consumptions_by_type).period(lifetime).as(post_consumption_type)
    '''
    response = graph.get_object(id=post_id, fields=fields)
    # print(post)



    like=response["post_reactions_by_type_total"]["data"][0]["values"][0]["value"]["like"]
    love=response["post_reactions_by_type_total"]["data"][0]["values"][0]["value"]["love"]
    wow=response["post_reactions_by_type_total"]["data"][0]["values"][0]["value"]["wow"]
    haha=response["post_reactions_by_type_total"]["data"][0]["values"][0]["value"]["haha"]
    sorry=response["post_reactions_by_type_total"]["data"][0]["values"][0]["value"]["sorry"]
    anger=response["post_reactions_by_type_total"]["data"][0]["values"][0]["value"]["anger"]

    print(like)

    reach=response["post_impressions_unique"]["data"][0]["values"][0]["value"]+1
    negative_feedback=response["negative_feedback"]["data"][0]["values"][0]["value"]
    post_link_consumption=0
    if 'post_consumption_type' in response:
        if "link_clicks" in response["post_consumption_type"]["data"][0]["values"][0]["value"]:
            post_link_consumption=response["post_consumption_type"]["data"][0]["values"][0]["value"]["link clicks"]
            
    shares=0
    if'shares'in response:
        shares=response["shares"]["count"]

    print(post_link_consumption)
    print(reach)
    print(negative_feedback)
    print(shares)

    comment_count=response["comments"]["summary"]["total_count"];

    commentsField='''message_tags{id}'''


    try:
        commentResponse = graph.get_object(id=post_id+"/comments", fields=commentsField)
        
    except expression as identifier:
        pass
    # print(commentResponse)
    tags_count=0
    if 'comments' in commentResponse:
        for comment in commentResponse['data']:
            # print(comment)
            if 'message_tags' in comment:
                print("icome here")        
                tags_count=len(comment['message_tags'])+tags_count
                # print(comment['message_tags'])

        

    print("tag_count",tags_count)
    post_score=(shares*20+
                    tags_count*10+
                    anger*2+
                    haha*2+
                    love*2+
                    wow*2+
                    sorry*2+
                    like*2+
                    comment_count*5-
                    negative_feedback*20)/(reach)
    return post_score                  

# testFacebookPageFeedData(page_id, access_token)



	  
	  

























































# import  urllib.request, urllib.error, urllib.parse
# # import urllib
# # import siteAnalyze
# import json
# # import putToES


# pageId="1290804767700294"
# # pageAmaze="1290804767700294"
# pageAccesToken='EAAWeCW1Hoy0BAJnZBsfckHWjfZBVXqFZCJbwKa8ZCYi3RofHF6IfUwQkNgH6r8UqqV78NEHllMZA3rzWAxMuIETHQHLpKvkjZCmNCBiIpSI5ZAB2KnKHZBsRyNaD4mfSOiz9ZCrg0EUnrVRuwXEgxSLluZBPBGoDqdD5bcCFMSVPoRAsQE5mKE7vFk9rGDTmdSKTSZAFf9XrkVoLAZDZD'
# appId="609100902619589"
# app_secret="c7d1ed8ff35d68a0964a73b448f4dac5"




# base = "https://graph.facebook.com/v2.7"
# node = "/" + "1290804767700294_1588958201218281"+ "/posts?fields=created_time,message,story&limit=1" 
# parameters = "&access_token=%s" %pageAccesToken

# url = base + node + parameters


# req = urllib.request.Request(url)
# response = urllib.request.urlopen(req)
# if response.getcode() == 200:
#     # success = True
#     print(response.read().decode('utf-8'))

