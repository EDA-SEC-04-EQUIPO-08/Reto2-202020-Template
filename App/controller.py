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

import config as cf
from App import model
from DISClib.ADT import list as lt
from time import process_time 
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta. Esta responsabilidad
recae sobre el controlador.
"""
# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def iniciarCatalogo():
    catalog = model.newCatalog()
    return catalog

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def cargarPeliculas(empty_catalog, casting, details):
    t1_start = process_time() #tiempo inicial
    catalog = model.loadMovies(empty_catalog,casting, details)
    lista = catalog["movies"]
    first = lt.getElement(lista,1)
    last = lt.lastElement(lista)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",(t1_stop-t1_start)," segundos")
    return(catalog, lt.size(lista),first,last)

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def getMoviesByProdComp(catalog, comp_name):
    """
    Retorna una compañia de produccion con sus películas,
    la cantidad de películas y su vote_avarage
    """
    
    company = model.getMoviesByProdComp(catalog, comp_name)
    movies = company['movies']
    size = model.moviesSize(movies)
    avarage = (company["vote_average"]/int(size))
    return (movies,size,avarage)

def getMoviesByActor(catalog, actor_name):
    actor = model.getMoviesByActor(catalog, actor_name)
    director = actor["most_feat"]
    movies = actor['movies']
    size = model.moviesSize(movies)
    avarage = (actor["vote_average"]/int(size))
    return (movies,size,avarage,director)

def getMoviesByDirector(catalog, director_name):
    director = model.getMoviesByDirector(catalog, director_name)
    movies = director['movies']
    size = model.moviesSize(movies)
    avarage = (director["vote_average"]/int(size))
    return (movies,size,avarage)

def getMoviesByGenre(catalog,genre_name):
    genre = model.getMoviesByGenre(catalog,genre_name)
    movies = genre["movies"]
    size = model.moviesSize(movies)
    count = (genre["vote_count"]/int(size))
    return (movies,size,count)

