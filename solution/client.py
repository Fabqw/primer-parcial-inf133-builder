#builder cliente
import requests

url = "http://localhost:8000/characters"
headers = {'Content-type': 'application/json'}

print("--- Characters actuales ---")
get_response = requests.get(url)
print(get_response.text)

print("--- Nuevo charcater ---")
nuevo_character = {
    "name": "Legolas",
    "level": 5,
    "role": "Archer",
    "charisma": 15
    "strength": 10,
    "dexterity": 10 
}
response = requests.post(url, json=nuevo_character, headers=headers)
print(response.text)

response = requests.get(url)
print(response.text)

print("--- Character con id ---")
id = 1
response_id = requests.get(f"{url}/{id}")
print(response_id.text)


role = "Archer"
response2 = requests.get(f"{url}/?role={role}")
print(response2.text)


print("--- Actualizacion character con id ---")
id = 2
actualizacion = {

}
response = requests.put(f"{url}/{id}", json=actualizacion)
print(response.text)

print("--- Eliminar character con id ---")
id = 3
response = requests.delete(f"{url}/{id}")
print(response.text)

print("--- Characters Actuales ---")
response = requests.get(url)
print(response.text)