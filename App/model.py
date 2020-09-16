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
               'genre': None,}

    catalog['movies'] = lt.newList('SINGLE_LINKED', compareRecordIds)
    catalog['productionCompany'] = mp.newMap(825000,  #471428,  825000
                                   maptype='CHAINING', 
                                   loadfactor=10, #CHAINING 10 , PROBING 0.4
                                   comparefunction=compareProductionCompany)

    return catalog

def newProductionCompany(name):
    """
    Crea una nueva estructura para modelar las películas
    y su promedio de ratings
    """
    prod_company = {'name': "", "movies": None,  "vote_average": 0}
    prod_company['name'] = name
    prod_company['movies'] = lt.newList('SINGLE_LINKED', compareProductionCompany)
    return prod_company

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
    except:
        print("Hubo un error con la carga de los archivos")
    return catalog

def addProductionCompany(catalog, movie):
    """
    Esta función adiciona una pelicula por su productora en el map
    """
    ProductionCompanies = catalog['productionCompany']
    comp_name = movie["production_companies"]
    existProd_Comp = mp.contains(ProductionCompanies, comp_name)
    if existProd_Comp:
        entry = mp.get(ProductionCompanies, comp_name)
        company = me.getValue(entry)
    else:
        company = newProductionCompany(comp_name)
        mp.put(ProductionCompanies, comp_name, company)
    lt.addLast(company['movies'], movie)

    comp_avg = company['vote_average']
    movie_avg = movie['vote_average']
    if (comp_avg == 0.0):
        company['vote_average'] = float(movie_avg)
    else:
        company['vote_average'] = (comp_avg + float(movie_avg)) / 2


# ==============================
# Funciones de consulta
# ==============================

def getMoviesByProdComp(catalog, comp_name):
    """
    Retorna una compañia de produccion con sus películas
    """
    company = mp.get(catalog['productionCompany'], comp_name)
    if company:
        return me.getValue(company)
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

def compareProductionCompany(keyname, productionCompany):
    """
    Compara dos nombres de productoras. El primero es una cadena
    y el segundo un entry de un map
    """
    pc_entry = me.getKey(productionCompany)
    if (keyname == pc_entry):
        return 0
    elif (keyname > pc_entry):
        return 1
    else:
        return -1
