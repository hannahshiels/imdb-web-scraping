import re
import requests
from bs4 import BeautifulSoup
import json

# https://www.imdb.com/search/title/ select tv movies/feature film and actor

def get_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_genres(soup):
    item = soup.select('.lister-item .genre')
    genres = []
    for genre in item:
        g =  str(genre.string)
        g = g[1:len(g)]
        genres.append(re.sub(' ', '', g))
    return genres

def get_titles(soup):
    link_titles = soup.select('.lister-item-header a')
    titles = []
    for title in link_titles:
        titles.append(title.string)
    return titles

def get_links(soup):
    link_titles = soup.select('.lister-item-header a')
    links = []
    for link in link_titles:
        links.append('https://www.imdb.com/' + link.get('href'))
    return links

def get_ratings(soup):
    rating_items = soup.select('.lister-item')


    ratings = []
    for i, rating in enumerate(rating_items):
        # print(rating.get('data-value'))
        x = rating.select('.ratings-imdb-rating')
        if len(x)==0:
            ratings.append('Not rated')
        for a in x:
            ratings.append(a.get('data-value'))
    return ratings

def get_descs(soup):
    content = soup.find_all('div', class_="lister-item-content")
    desc_items = []
    for i in content:
        x =i.select('p')[1].get_text(strip=True)
        x = re.sub('See full summary', '', x)
        x = re.sub('See full synopsis', '', x)
        x = re.sub('»', '', x)
        desc_items.append(x)
    return desc_items

def get_years(soup):
    yearsSpans = soup.select('.lister-item-year')
    years = []
    for year in yearsSpans:
            y = str(year.string)
            y = re.sub('[a-zA-Z]', '', y)
            y = re.sub('[\W\_]', '', y)
            if y != '':
                years.append(y)
            else: 
                years.append('Not released')
    return years

def create_json(titles, links,descs, genres, ratings, years): 
    movies = []
    # should all be the same number, otherwise there is a mistake 
    # print(str(len(titles)), ' ' + str(len(links)) , ' ' , str(len(descs)) , ' ' , str(len(genres)) , ' ' , str(len(ratings)) , ' ' , str(len(years) ))
    for i,data in enumerate(titles):
        doc = { 'movie': {"title": titles[i],
                "link": links[i],
                "desc": descs[i],
                "genre": genres[i],
                "rating": ratings[i],
                "year": years[i]
         }}
        movies.append(doc)
    full_doc = {"movies": movies}
    with open('matt.json', 'a') as f:
        f.write(json.dumps(full_doc, ensure_ascii=False, indent=4))
    

def main():
    # change link to get movies from other actors
    soup = get_page('https://www.imdb.com/search/title/?title_type=feature,tv_movie&role=nm0000354&adult=include')
    titles = get_titles(soup)
    descs = get_descs(soup)
    links = get_links(soup)
    ratings = get_ratings(soup)
    genres = get_genres(soup)
    years = get_years(soup)
    create_json(titles, links, descs, genres, ratings, years)
    



main()


