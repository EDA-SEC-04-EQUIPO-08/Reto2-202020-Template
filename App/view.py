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

import sys
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones y por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

casting_small = "Data/MoviesCastingRaw-small.csv"
details_small = "Data/SmallMoviesDetailsCleaned.csv"
casting_large = "Data/AllMoviesCastingRaw.csv"
details_large = "Data/AllMoviesDetailsCleaned.csv"

# ___________________________________________________
#  Funciones para imprimir la inforamación de
#  respuesta.  La vista solo interactua con
#  el controlador.
# ___________________________________________________

def printMovieData(element):
    print(element["title"]+":")
    print("a. Fecha de estreno: "+element["release_date"])
    print("b. Promedio de la votación: "+element["vote_average"])
    print("c. Número de votos: "+element["vote_count"])
    print("d. Idioma: "+element["original_language"]+"\n")

def printMoviesNames(lst):
    print("Las películas son:")
    iterator = it.newIterator(lst)
    i=1
    while  it.hasNext(iterator):
        element = it.next(iterator)
        print(str(i)+"- "+element["title"])
        i += 1 

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("Bienvenido")
    print("1- Iniciar catalogo del películas")
    print("2- Cargar películas al catalogo del películas")
    print("3- Descubrir productoras de cine ")
    print("0- Salir")


while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Iniciando catalogo ....")
        catalogo = controller.iniciarCatalogo()
        print("Se creo el catalogo con exito")
    elif int(inputs[0]) == 2:
        print("Cargando películas ....")
        catalog,size,first,last = controller.cargarPeliculas(catalogo, casting_large, details_large)
        print("Se cargaron "+str(size)+ " películas"+"\n")
        printMovieData(first)
        printMovieData(last)
    elif int(inputs[0]) == 3:
        comp_name = input("Ingrese el nombre de la productora de cine que quiere buscar\n")
        movies,size,vote_avarage = controller.getMoviesByProdComp(catalog, comp_name)
        print("La productora "+comp_name+" tiene "+str(size)+ " películas. \n")
        print("El promedio de la calificación de sus películas es "+str(vote_avarage) +"\n")
        printMoviesNames(movies)
        print("\n")
    else:
        sys.exit(0)
sys.exit(0)
