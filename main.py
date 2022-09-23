#coding:utf-8
from os import system
import requests
from bs4 import BeautifulSoup
import wget
#add proxy

WEB_SITE_URL = "https://www.example.com/"

def userArgent()-> list: 
    
    return [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.93 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"
    ]

def wgetPage(urlList:dict) :
    for key ,value in urlList.items() :
        cmd = "curl '{0}' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' > {1}".format(value,key)
        system(cmd)

def wgetAsset(linkAssets:list) :
    for link in linkAssets :
	    # wget.download(link)
        try :
            wget.download(link)
            print("ok....")
        except :
            print("error....")
            pass

def  getPageContent(url:str) :
    
    try :
        return requests.get(url).content
    except :
        pass
        # exit("Could not get url content")

def htmlParst(htmlContent:str):
    
    return BeautifulSoup(htmlContent,'html.parser')


def getWebSiteLinks(WebSiteUrl:str) -> list:
    siteLinks = []
    # siteLinks.append(WebSiteUrl)
    htmlCOntent = htmlParst(getPageContent(WebSiteUrl))
    possibleLink = htmlCOntent.find_all("a")
    for link in possibleLink :
        if link.get('href') in ["javascript:void()","#","mailto:contact@"+WebSiteUrl.rstrip("/").replace("https://","")] :
            pass
        else :
            link = WebSiteUrl+link.get('href')
            if link not in siteLinks :
                print("***[] "+link)
                siteLinks.append(link)
            #     siteLinks.append(link)
            # else :
            #     siteLinks.extend(getWebSiteLinks(link))
            
    return siteLinks

def getWebSiteAssetsLinks(WebSiteUrl:str) -> list:
    siteLinks = []
    siteScripts = []
    siteImages = []
    # siteLinks.append(WebSiteUrl)
    htmlCOntent = htmlParst(getPageContent(WebSiteUrl))
    possibleAssetsLink = htmlCOntent.find_all("link")
    possibleAssetsScript = htmlCOntent.find_all("script")
    possibleAssetsImage = htmlCOntent.find_all("img")
    for link in possibleAssetsLink :
        if link.get('href') in ["javascript:void()","#","mailto:contact@"+WebSiteUrl.rstrip("/").replace("https://","")] :
            pass
        else :
            link = WebSiteUrl+link.get('href')
            if link not in siteLinks :
                print("***[] "+link)
                siteLinks.append(link)
            #     siteLinks.append(link)
            # else :
            #     siteLinks.extend(getWebSiteLinks(link))
    for script in possibleAssetsScript :

        try :
            script = WebSiteUrl+script.get('src')
            if script not in siteScripts :
                print("***[] "+script)
                siteScripts.append(script)
        except :
            pass

    for img in possibleAssetsImage :

        try :
            img = WebSiteUrl+img.get('src')
            if img not in siteImages :
                print("***[] "+img)
                siteImages.append(img)
        except :
            pass
            
    # return siteLinks, siteScripts, siteImages
    return  siteImages

def urlListToDict(urlList:list,WebSiteUrl:str):
    urlDict = {}
    for link in urlList :
        name = link.replace(WebSiteUrl,"").rstrip("/").replace("/","-")+""
        if name == ".html" :
            name = "index.html"
        urlDict[name] = link
    
    return urlDict

linkList = getWebSiteLinks(WEB_SITE_URL)
linkDict = urlListToDict(linkList,WEB_SITE_URL)
# linkAssets = getWebSiteAssetsLinks(WEB_SITE_URL)

wgetPage(linkDict)
# wgetAsset(linkAssets)