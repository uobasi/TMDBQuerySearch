from flask import Flask, render_template, request, redirect, url_for
import json
import urllib.request
from urllib.error import HTTPError

app = Flask(__name__)

#api key and search movie url 
api_key = "6478ea326187eb3ae9d55585ee8170ef"
search_url = "https://api.themoviedb.org/3/search/movie?api_key="+api_key+"&query="

#main web page function
@app.route("/", methods=['GET','POST'])
def Home():
    #Gets the query text from the html form if available to get json object
    if request.method =='POST' and request.form.get('query'):
        try :
            query = request.form['query'].replace(' ','%20')
            jsonData = json.loads(urllib.request.urlopen(search_url+query).read())
            getAllPages = search_url+query+'&page='
            jsonDict = []
        except urllib.error.HTTPError:
            return render_template('layout.html', noResult='No Results Found')  

        totalPage = jsonData["total_pages"]
        print(totalPage)
        return redirect(url_for('SearchQuery',query=query, pageNum=1, totalPage=totalPage))

    else:
        return render_template('layout.html')

# this function gets the indiviual json result per page
@app.route('/search/<query>/<pageNum>/<totalPage>', methods=['GET','POST'])
def SearchQuery(query,pageNum,totalPage):
    try:
        getPage=search_url+query+'&page='+str(pageNum)
        jsonDict = json.loads(urllib.request.urlopen(getPage).read())["results"]
        if len(jsonDict) >= 1:
                for i in range(len(jsonDict)):
                    if jsonDict[i]['backdrop_path'] != None:
                        jsonDict[i]['backdrop_path'] = 'https://image.tmdb.org/t/p/w500/'+jsonDict[i]['backdrop_path'] 
                    else:
                        jsonDict[i]['backdrop_path'] = '/static/NoImage.png'
                return render_template('searchResults.html', data=jsonDict, vars=[query,int(pageNum),int(totalPage)])
        else:
            return render_template('searchResults.html', noResult='No Results Found')
    except urllib.error.HTTPError:
            return render_template('layout.html', noResult='No Results Found')
    

if __name__ == '__main__':
    app.run(debug=True)