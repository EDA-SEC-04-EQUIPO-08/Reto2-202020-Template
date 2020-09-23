"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""

# -----------------------------------------------------
# API del TAD Catalogo de Peliculas
# -----------------------------------------------------
def newCatalog():
    catalog = {'movies': None,
               'productionCompany': None,
               'country': None,
               'director': None,
               'actor': None,
               'genre': None}

    catalog['movies'] = lt.newList('SINGLE_LINKED', compareRecordIds)
    catalog['productionCompany'] = mp.newMap(825000,  #471428,  825000
                                   maptype='CHAINING', 
                                   loadfactor=10, #CHAINING 10 , PROBING 0.4
                                   comparefunction=compareNameInEntry)
    catalog['actor'] = mp.newMap(825000,  #471428,  825000
                                   maptype='CHAINING', 
                                   loadfactor=10, #CHAINING 10 , PROBING 0.4
                                   comparefunction=compareNameInEntry)
    catalog['director'] = mp.newMap(825000,  #471428,  825000
                                   maptype='CHAINING', 
                                   loadfactor=10, #CHAINING 10 , PROBING 0.4
                                   comparefunction=compareNameInEntry)
    catalog['genre'] = mp.newMap(825000,  #471428,  825000
                                   maptype='CHAINING', 
                                   loadfactor=10, #CHAINING 10 , PROBING 0.4
                                   comparefunction=compareNameInEntry)
    catalog['country'] = mp.newMap(825000,  #471428,  825000
                                   maptype='CHAINING', 
                                   loadfactor=10, #CHAINING 10 , PROBING 0.4
                                   comparefunction=compareNameInEntry)
    return catalog

def newProductionCompany(name):
    """
    Crea una nueva estructura para modelar las películas
    y promedio de ratings de una productora
    """
    prod_company = {'name': "", "movies": None,  "vote_average": 0}
    prod_company['name'] = name
    prod_company['movies'] = lt.newList('SINGLE_LINKED', compareText)
    return prod_company

def newActor(name):
    """
    Crea una nueva estructura para modelar las películas,
    el promedio de ratings y los directores 
    con quien ha trabajado de un actor
    """
    actor = {'name': "", "movies": None, "vote_average": 0, "directors":None, "most_feat":"No existe", "most_times":0}
    actor['name'] = name
    actor['movies'] = lt.newList('SINGLE_LINKED', compareText)
    actor["directors"] = mp.newMap(40, 
                                   maptype='PROBING', 
                                   loadfactor=0.4, #CHAINING 10 , PROBING 0.4
                                   comparefunction=compareNameInEntry)
    return actor

def newDirector(name):
    """
    Crea una nueva estructura para modelar las películas,
    el promedio de ratings de un director
    """
    director = {'name': "", "movies": None, "vote_average": 0}
    director['name'] = name
    director['movies'] = lt.newList('SINGLE_LINKED', compareText)

    return director

def newGenre(name):
    """
    Crea una nueva estructura para modelar las películas,
    el promedio de ratings de un genero
    """
    genre = {"name":"", "movies": None, "vote_count": 0}
    genre["name"] = name
    genre["movies"] = lt.newList('SINGLE_LINKED', compareText)

    return genre

def newCountry(name):
    country = {"name":"", "movies":None}
    country["name"]=name
    country["movies"] = lt.newList('SINGLE_LINKED', compareText)
    return country
# Funciones para agregar informacion al catalogo

def loadMovies(catalog, fileCasting, fileDetails):
    lst= catalog['movies']
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open( fileDetails, encoding="utf-8-sig") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row:
                del elemento["id"]
                lt.addLast(lst,elemento)
        with open( fileCasting, encoding="utf-8-sig") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            iterator = it.newIterator(lst)
            for elemento in row: 
                element = it.next(iterator)
                element.update(elemento)
                addProductionCompany(catalog,element)     #Se añade la película al map de Production Company
                addActor(catalog,element)                 #Se añade la película al map de actor
                addDirector(catalog,element)              #Se añade la película al map de director
                addGenre(catalog,element)                 #Se añade la película al map de genre
                addCountry(catalog,element)               #Se añade la película al map de country

    except:
        print("Hubo un error con la carga de los archivos")
    return catalog

def addProductionCompany(catalog, movie):
    """
    Esta función adiciona una pelicula por su productora en el map
    """
    ProductionCompanies = catalog['productionCompany']
    comp_name = movie["production_companies"].lower()
    existProd_Comp = mp.contains(ProductionCompanies, comp_name)
    title = movie["title"]
    if existProd_Comp:
        entry = mp.get(ProductionCompanies, comp_name)
        company = me.getValue(entry)
    else:
        company = newProductionCompany(comp_name)
        mp.put(ProductionCompanies, comp_name, company)
    lt.addLast(company['movies'], title)

    comp_avg = company['vote_average']
    movie_avg = movie['vote_average']
    if (comp_avg == 0.0):
        company['vote_average'] = float(movie_avg)
    else:
        company['vote_average'] = comp_avg + float(movie_avg)

def addActor(catalog, movie):
    """
    Esta función adiciona una pelicula por su actor en el map
    """
    actors = catalog['actor']
    actor_names = [movie["actor1_name"], movie["actor2_name"], movie["actor3_name"], movie["actor4_name"], movie["actor5_name"]]
    movie_avg = movie['vote_average']
    director_name = movie["director_name"]
    title = movie["title"]
    for actor_name1 in actor_names:
        actor_name = actor_name1.lower()
        if actor_name != "none":
            existActor = mp.contains(actors, actor_name)
            if existActor:
                entry = mp.get(actors, actor_name)
                actor = me.getValue(entry)
            else:
                actor = newActor(actor_name)
                mp.put(actors, actor_name, actor)
            lt.addLast(actor['movies'], title)

            actor_avg = actor['vote_average']      
            if (actor_avg == 0.0):
                actor['vote_average'] = float(movie_avg)
            else:
                actor['vote_average'] = actor_avg + float(movie_avg)

            actor_dir = actor["directors"]
            existDir = mp.contains(actor_dir, director_name)
            if existDir:
                entry = mp.get(actor_dir, director_name)
                times = (me.getValue(entry) + 1)
                me.setValue(entry, times)
                if times > actor["most_times"]:
                    actor["most_times"] = times
                    actor["most_feat"] = director_name
            else:
                if director_name != "none":
                    times1 = 1
                    mp.put(actor_dir, director_name, times1)
                    if times1 > actor["most_times"]:
                        actor["most_times"] = times1
                        actor["most_feat"] = director_name

def addDirector(catalog, movie):
    """
    Esta función adiciona una pelicula por su director en el map
    """
    directors = catalog['director']
    director_name = movie["director_name"].lower()
    movie_avg = movie['vote_average']
    title = movie["title"]
    if director_name != "none":
        existDirector = mp.contains(directors, director_name)
        if existDirector:
            entry = mp.get(directors, director_name)
            director = me.getValue(entry)
        else:
            director = newDirector(director_name)
            mp.put(directors, director_name, director)
        lt.addLast(director['movies'], title)
        director_avg = director['vote_average']      
        if (director_avg == 0.0):
            director['vote_average'] = float(movie_avg)
        else:
            director['vote_average'] = director_avg + float(movie_avg)

def addGenre(catalog, movie):
    """
    Esta función adiciona una pelicula por su director en el map
    """
    genres= catalog["genre"]
    genre_names = movie["genres"].split("|")
    movie_count = movie["vote_count"]
    title = movie["title"]
    for genres1 in genre_names:
        genre_name = genres1.lower()
        if genre_name != "none":
            existGenre =mp.contains(genres,genre_name)
            if existGenre:
                entry = mp.get(genres,genre_name)
                genre = me.getValue(entry)
            else:
                genre = newGenre(genre_name)
                mp.put(genres,genre_name,genre)
            lt.addLast(genre['movies'],title)
            genre_count = genre['vote_count']
            if (genre_count == 0.0):
                genre['vote_count'] = float(movie_count)
            else:
                genre['vote_count'] = genre_count + float(movie_count)

def addCountry (catalog,movie):
    """
    Esta función adiciona una pelicula por su país en el map
    """
    country = catalog["country"]
    country_name = movie["production_countries"].lower()
    movie_year= (movie["release_date"]+" ")[-5:-1]
    movie_director = movie["director_name"]
    title = movie["title"]
    if country_name != "none":
        existsCountry =mp.contains(country,country_name)
        if existsCountry: 
            entry = mp.get(country, country_name)
            pais = me.getValue(entry)
        else:
            pais = newCountry(country_name)
            mp.put(country,country_name,pais)
        lt.addLast(pais["movies"],(title,movie_year,movie_director))
    



# ==============================
# Funciones de consulta
# ==============================

def getMoviesByProdComp(catalog, comp_name):
    """
    Retorna una compañia de produccion con sus películas
    """
    company = mp.get(catalog['productionCompany'], comp_name.lower())
    if company:
        return me.getValue(company)
    return None

def getMoviesByActor(catalog, actor_name):
    """
    Retorna un actor con sus películas
    """
    actor = mp.get(catalog['actor'], actor_name.lower())
    if actor:
        return me.getValue(actor)
    return None

def getMoviesByDirector(catalog, director_name):
    """
    Retorna un director con sus películas
    """
    director = mp.get(catalog['director'], director_name.lower())
    if director:
        return me.getValue(director)
    return None

def getMoviesByGenre(catalog, genre_name):
    """
    Retorna las películas de un genero
    """
    genre = mp.get(catalog["genre"],genre_name.lower())
    if genre:
        return me.getValue(genre)
    else:
        return None  

def getMoviesByCountry(catalog,country_name):
    """
    Retorna las películas de un país
    """
    country = mp.get(catalog["country"],country_name.lower())
    if country:
        return me.getValue(country)
    else:
        return None

def moviesSize(lst):
    return lt.size(lst)



# ==============================
# Funciones de Comparacion
# ==============================

def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1

def compareNameInEntry(keyname, entry):
    """
    Compara un nombre con una llave de una entrada
    """
    pc_entry = me.getKey(entry)
    if (keyname == pc_entry):
        return 0
    elif (keyname > pc_entry):
        return 1
    else:
        return -1

def compareText(text1, text2):
    """
    Compara dos strings
    """
    if text1 == text2:
        return 0
    elif text1 > text2:
        return 1
    return -1
