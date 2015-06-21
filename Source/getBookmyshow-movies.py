import json
import time
from pprint import pprint
import urllib2 as ul
from bs4 import BeautifulSoup


with open("City_json.json") as data_file:
     json_data=json.load(data_file)


for i in json_data["City"]:
    try:
        j=i.encode('utf-8')
        url_str="http://in.bookmyshow.com/"+j+"/movies"
        start_time = time.time()
        print("trying to open link "+url_str)
        response = ul.urlopen(url_str)
        print("response from "+j)
        page_content = response.read()
        print("response 1 from "+j)
        soup = BeautifulSoup(page_content)
        print("response 2 from "+j)
        print("--- %s seconds to read main webpage---" % (time.time() - start_time)) 
        json_string='{"movie":['
        soup_itemprops=soup.find_all('h3',itemprop="name")
        for movie in soup_itemprops:
            try:
                start_time = time.time()
                var_movie=movie.find('a')['title']
                var_movie=var_movie.strip()# Movie name to be used later in json
                S=var_movie+" official trailer" # Appending the official trailer in the name of the movie
                json_string+='"'+var_movie+'",'
            except:
                print("inside except fetch new movie")
        json_string=json_string[0:-1]+']}'
        parsed = json.loads(json_string)
	path = "../output_bookmyshow/"
        filename=j+"_movies.json"
        print("filename " +filename)
        try:
               print("generating file in try")
               os.remove(path+filename)
               with open(path+filename, "w") as outfile:
                    json.dump(parsed, outfile, indent=4)
        except:
               with open(path+filename, "w") as outfile:
                    json.dump(parsed, outfile, indent=4)

        
    except:
        print("fetch next city :"+j+" is currently not available on bookmyshow")
