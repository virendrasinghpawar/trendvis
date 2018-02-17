import pagetimebased

file=open("user_pages.txt","r")
fileWrite=open("noToken.txt","w+")
datas=file.readlines()

for data in datas:
    data=data.rstrip()
    data=data.split(",")
    page_id=data[0]
    access_token=data[1]
    # print(data)
    print(page_id,access_token)
    returnob=pagetimebased.testFacebookPageFeedData(page_id,access_token)
    print(returnob)
    if returnob=="ok":
        print("it works")
    if returnob=="nothing":
        fileWrite.write(str(page_id)+"\n")
        print("access not work")
    else:
        print("there is problem in module")  
fileWrite.close() 
