import json
import time
import threading
import urllib2 as ul
from bs4 import BeautifulSoup
from apiclient.discovery import build
from optparse import OptionParser
import os
# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyA_NDpr8L3Ie42WH6ZjDeKu8UBu1pb2EHg" #old "AIzaSyCndc_YwoZgZjGRHltV-GzydtaVTKjyKxI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

cities = ['Agartala', 'Agra', 'Ahmedabad', 'Ajmer', 'Aligarh', 'Allahabad', 'Amritsar', 'Aurangabad', 'Bengaluru', 'Bhopal', 'Bilaspur', 'Chandigarh', 'Chennai', 'Coimbatore', 'Dehradun', 'Durgapur', 'Goa', 'Guwahati', 'Gwalior', 'Haridwar', 'Hyderabad', 'Indore', 'Jabalpur', 'Jaipur', 'Jamnagar', 'Jamshedpur', 'Jodhpur', 'Kanpur', 'Kolhapur', 'Kolkata', 'Kota', 'Lucknow', 'Ludhiana', 'Madurai', 'Mangalore', 'Meerut', 'Mumbai', 'Muzaffarnagar', 'Mysore', 'Nagpur', 'Nashik', 'Patiala', 'Patna', 'Pune', 'Raipur', 'Rajkot', 'Ranchi', 'Rohtak', 'Solapur', 'Surat', 'Udaipur', 'Ujjain', 'Vadodara']
#cities=['Agra']
#cities=['faridabad']
distinct_movies = set()
movie_dict = dict()
movies_with_id = dict()
movies_with_rating=dict()
movies_with_lang=dict()

def BookMyShow():
    for i in cities:
        try:
            j=i.encode('utf-8')
            url_str="http://in.bookmyshow.com/"+j+"/movies"
            count=0
            print("trying to open link "+url_str)
            response = ul.urlopen(url_str)
            page_content = response.read()
            soup = BeautifulSoup(page_content)
            soup_itemprops=soup.find_all('h3',itemprop="name")
            movies=set()
            for movie in soup_itemprops:
                try:
                    start_time = time.time()
                    var_movie=movie.find('a')['title']
                    var_movie=var_movie.strip()# Movie name to be used later in json
                    idx = var_movie.find('(')
                    if idx !=-1:
                        var_movie = var_movie[0:idx-1]
                    soup_lang=((soup.findAll("span", { "class" : "language" })[count]['title']).encode('utf-8')).strip()
                    count=count+1
                    #print("soup_lang "+soup_lang)
                    idx = soup_lang.find(' ')
                    if idx !=-1:
                        soup_lang = soup_lang[0:idx]
                    movies_with_lang[var_movie]=soup_lang
                    movies.add(var_movie)
                    distinct_movies.add(var_movie)
                    
                except:
                    print("inside except fetch new movie")
            movie_dict[i] = movies
            
        except:
            print("fetch next city :"+j+" is currently not available on bookmyshow")

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
  search_response = youtube.search().list(q=options.q, part="id,snippet", maxResults=options.maxResults).execute()

  videos = []

  for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
          videos.append("%s " % (search_result["id"]["videoId"]))
      try:
          return videos[0].encode('utf-8')
      except:
          return ''
        
def YouTube():
    parser = OptionParser()
    for m in distinct_movies:
        toSearch=(m+" official trailer").encode('utf-8')
        
        parser = OptionParser(conflict_handler="resolve")
        parser.add_option("--q", dest="q", help="Search term",default=toSearch)
        parser.add_option("--max-results", dest="maxResults",help="Max results", default=1)
        (options, args) = parser.parse_args()
        VideoId=youtube_search(options)
        movies_with_id[m]=VideoId
        #if VideoId:
        #    print m+" : "+VideoId

lock = threading.Lock()
def updateSharedDict(movie,rating,duration,genre,language):
    with lock:
        movies_with_rating[movie]=(rating,duration,genre,language)
    
def IMDBRating1():
    baseurl="http://www.imdb.com"
    length = len(distinct_movies)
    distinct_movies_list = list(distinct_movies)
    for m in range(length//2):
        nameurl = "/find?s=tt&q="+distinct_movies_list[m]
        response = ul.urlopen(baseurl+nameurl)
        namePageSoup = BeautifulSoup(response.read())
        rating_link = namePageSoup.table.a['href']
        response2 = ul.urlopen(baseurl+rating_link)
        ratingPageSoup = BeautifulSoup(response2.read())
        rating=''
        duration=''
        genre=''
        lang=''
        try:
            rating = ratingPageSoup.findAll("div", { "class" : "star-box-details" })[0].span.contents[0]
            duration = ratingPageSoup.findAll("div", { "class" : "infobar" })[0].time.contents[0]
            duration = duration.strip()
            allGenreItems = ratingPageSoup.findAll("span", {"itemprop" : "genre"})
            genre = allGenreItems[0].contents[0]
            for g in range(1,len(allGenreItems)):
                genre+= '|'+ allGenreItems[g].contents[0]
        except:
            rating = "0"
        temp_movie=distinct_movies_list[m]
        try:
            lang=movies_with_lang[temp_movie]

            print "temp_movie ->"+temp_movie+" language "+lang
        except:
            #print "inside exception for language for "+temp_movie
            print "temp_movie ->"+temp_movie+" language "+lang
        updateSharedDict(distinct_movies_list[m],rating,duration,genre,lang)
        #print distinct_movies_list[m]+" -> "+rating+" -> "+duration + " -> " +genre
    

def IMDBRating2():
    baseurl="http://www.imdb.com"
    length = len(distinct_movies)
    distinct_movies_list = list(distinct_movies)
    for m in range(length//2,length):
        nameurl = "/find?s=tt&q="+distinct_movies_list[m]
        response = ul.urlopen(baseurl+nameurl)
        namePageSoup = BeautifulSoup(response.read())
        rating_link = namePageSoup.table.a['href']
        response2 = ul.urlopen(baseurl+rating_link)
        ratingPageSoup = BeautifulSoup(response2.read())
        rating=''
        duration=''
        genre=''
        lang=''
        try:
            rating = ratingPageSoup.findAll("div", { "class" : "star-box-details" })[0].span.contents[0]
            duration = ratingPageSoup.findAll("div", { "class" : "infobar" })[0].time.contents[0]
            duration = duration.strip()
            allGenreItems = ratingPageSoup.findAll("span", {"itemprop" : "genre"})
            genre = allGenreItems[0].contents[0]
            for g in range(1,len(allGenreItems)):
                genre+= '|'+ allGenreItems[g].contents[0]
        except:
            rating = "0"
        temp_movie=distinct_movies_list[m]
        try:
            lang=movies_with_lang[temp_movie]
            print "temp_movie ->"+temp_movie+" language "+lang
        except:
            #print "inside exception for language for "+temp_movie
            print "temp_movie ->"+temp_movie+" language "+lang
        updateSharedDict(distinct_movies_list[m],rating,duration,genre,lang)
        #print distinct_movies_list[m]+" -> "+rating+" -> "+duration + " -> " +genre


if __name__ == "__main__":
    start_time = time.time()
    BookMyShow()
    thread1 = threading.Thread(target=YouTube,args=())
    thread2 = threading.Thread(target=IMDBRating1,args=())
    thread3 = threading.Thread(target=IMDBRating2,args=())
    thread1.daemon=True
    thread2.daemon=True
    thread3.daemon=True
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    path="../Main_Website/Output/"
    for city in movie_dict:
        outfile=open(path+city+".json","w")
        IntermediateOutputString="{"
        for movie in movie_dict[city]:
            if movies_with_id[movie]:
                try:
                    IntermediateOutputString+='\"' + movie + '\":[' + '\"' + movies_with_id[movie].strip() + '\",' + '\"' + movies_with_rating[movie][0] +'\",'+'\"'+movies_with_rating[movie][1]+'\",'+'\"'+movies_with_rating[movie][2] +'\",'+'\"'+movies_with_rating[movie][3]+'\"],'
                except:
                    IntermediateOutputString+='\"' + movie + '\":[' + '\"' + movies_with_id[movie].strip() + '\",' + '\"' + '' +'\",'+'\"'+ '' +'\",'+'\"'+ ''+'\",'+'\"'+'' +'\"],'
                    #print movie " -> " + movies_with_id[movie].strip() +" -> "+movies_with_rating[movie][0]+" -> "+movies_with_rating[movie][1]+" -> "+movies_with_rating[movie][2]+" -> "+movies_with_rating[movie][3]
                    #Just to be safe and handle key errors    

        IntermediateOutputString= IntermediateOutputString[0:-1] + "}"
        JsonOutputString = json.loads(IntermediateOutputString)
        try:    
            json.dump(JsonOutputString, outfile, indent=4)
        except:
            print "Unable to write file : "+city
        outfile.close()
    print("--- %s seconds to read and write ---" % (time.time() - start_time))

