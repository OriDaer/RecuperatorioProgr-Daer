import requests, os, json

url = 'https://jsonplaceholder.typicode.com/users'
url_posts = 'https://jsonplaceholder.typicode.com/posts'
usersVowals = []
usersConsonants = []

dir = 'UsersData'
if not os.path.exists(dir):
    os.makedirs(dir)

def descArchiv(nombreArchiv, nombreArchivCons):
    archiv = open(os.path.join(dir, nombreArchiv), 'w')
    json.dump(usersVowals, archiv, indent=4)
    archiv.close()
    archivCons = open(os.path.join(dir, nombreArchivCons), 'w')
    json.dump(usersConsonants, archivCons, indent=4)
    archivCons.close()

def vowalsAndConsonants(cantN):
    if cantN and cantN[0] in '0123456789':
        cantN = int(cantN)
        if 1 <= cantN <= 10:
            response = requests.get(url)
            if response.status_code == 200:
                users = response.json()
                for user in users[:cantN]:
                    userName = user['name']
                    if userName[0] in 'AEIOUaeiou':
                        usersVowals.append(userName)
                    else:
                        usersConsonants.append(userName)
                descArchiv("usersVowels.json", "usersConsonants.json")
            else:
                print("Error con la response, intenta de nuevo")
        else:
            print("Número fuera de rango, intenta otra vez")
    else:
        print("Error, intente de nuevo")

def filtraUbic(users, ubic):
    filtraUsers = []
    for user in users:
        if ubic.lower() in user['address']['city'].lower() or ubic.lower() in user['address']['street'].lower():
            filtraUsers.append(user)
    if filtraUsers:
        archivo = open(os.path.join(dir, "filteredUsers.json"), 'w')
        json.dump(filtraUsers, archivo, indent=4)
        archivo.close()
        print(f"Se encontraron {len(filtraUsers)} usuarios en la ubicación '{ubic}'.")
    else:
        print(f"No se encontraron usuarios en '{ubic}'.")

def contOcurr(texto, palabraClave):
    palabraClave = palabraClave.lower()
    texto = texto.lower()
    ocurr = 0
    palabras = texto.split()
    for palabra in palabras:
        if palabra == palabraClave:
            ocurr += 1
    return ocurr

def buscUser(numId, palabraClave):
    totalOcurr = 0
    response = requests.get(url_posts)
    if response.status_code == 200:
        posts = response.json()
        user_posts = []
        for post in posts:
            if post['userId'] == numId:
                user_posts.append(post)
        for post in user_posts:
            title_ocurr = contOcurr(post['title'], palabraClave)
            body_ocurr = contOcurr(post['body'], palabraClave)
            ocurr_post = title_ocurr + body_ocurr
            totalOcurr += ocurr_post
            if ocurr_post > 0:
                print(f"Post ID {post['id']}: ocurr de '{palabraClave}' = {ocurr_post}")

        print(f"Total de ocurrencias de '{palabraClave}': {totalOcurr} veces")
    else:
        print("Error al obtener los posts")

cantN = input('Ingrese la cantidad de usuarios que desea obtener, debe ser entre 1 y 10: ')
vowalsAndConsonants(cantN)

ubic = input('Ingrese una ubicación (ciudad o estado): ')
response = requests.get(url)
if response.status_code == 200:
    users = response.json()
    filtraUbic(users, ubic)
else:
    print("Error en la response, intenta de nuevo")

numId = int(input('Ingrese el ID del usuario: '))
palabraClave = input('Ingrese una palabra clave: ')
buscUser(numId, palabraClave)
