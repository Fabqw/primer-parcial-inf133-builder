#builder
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs


characters = {
    {
       "name": "Gandalf",
       "level": 10,
       "role": "Wizard",
       "charisma": 15
       "strength": 10,
       "dexterity": 10 
    },
}


class Character:
    def __init__(self):
        self.name = None
        self.level = None
        self.role = None
        self.charisma = None
        self.strength = None
        self.dexterity = None
    
    def __str__(self):
        return f"Character, name: {self.name}, level: {self.level}, role: {self.role}, charisma: {self.charisma}, strength: {self.strength}, dexterity: {self.dexterity}"


class CharacterBuilder:
    def __init__(self):
        self.character = Character()
        
    def set_name(self, name):
        self.character.name = name
    
    def set_level(self, level):
        self.character.level = level

    def set_role(self, role):
        self.character.role = role

    def set_charisma(self, charisma):
        self.character.charisma = charisma

    def set_strength(self, strength):
        self.character.strength = strength

    def set_dexterity(self, dexterity):
        self.character.dexterity = dexterity
        
    def get_character(self):
        return self.character
        

class Game:
    def __init__(self, builder):
        self.builder = builder
    
    def create_character(self, name, level, role, charisma, strength, dexterity):

        self.builder.set_name(name)
        self.builder.set_level(level)
        self.builder.set_role(role)
        self.builder.set_charisma(charisma)
        self.builder.set_strength(strength)
        self.builder.set_dexterity(dexterity)

        
        return self.builder.get_character()


class CharacterService:
    def __init__(self):
        self.builder = CharacterBuilder()
        self.game = Game(self.builder)
        self.characters = characters
        
    @staticmethod
    def create_character(self, post_data):
        name = post_data.get('name', None)
        level = post_data.get('level', None)
        role = post_data.get('role', None)
        charisma = post_data.get('charisma', None)
        strength = post_data.get('strength', None)
        dexterity = post_data.get('dexterity', None)

        character = self.game.create_character(name, level, role, charisma, strength, dexterity)

        id_character_nuevo = max(characters.keys()) + 1 if characters else 1
        characters[id_character_nuevo] = character
        
        return character
    
    @staticmethod
    def read_characters(self):
        return characters

    @staticmethod
    def read_character_id(self, id):
        for character in characters.items():
            if character["id"] == id:
                return character
        return None
    
    @staticmethod
    def character_role(role):
        return {id_character: character for id_character, character in characters.items() if character["rol"] == rol} 

    @staticmethod
    def read_character_level(self, level):
        return {id_character: character for id_character, character in characters.items() if character["level"] == level} 

    @staticmethod
    def read_character_charisma(self, charisma):
        return {id_character: character for id_character, character in characters.items() if character["charisma"] == charisma} 

    @staticmethod
    def update_character(id_character, data):         
        if id_character in characters:
            characters[id_character].update(data)
            return animales
        return None
    
    @staticmethod
    def delete_character(id_character):
        if id_character in characters:
            characters.pop(id_character)
            return animales
        return None

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
        
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
class CharacterHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = CharacterService()
        super().__init__(*args, **kwargs)

    def do_POST(self):

        if self.path == "/characters":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_character(data)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):

        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        if self.path == "/characters":
            response_data = self.controller.read_characteres()
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        elif self.path.startswith("/charactrs") and "role" in query_params:            
            role = query_params["role"][0]
            character_roles = self.controller.read_character_role(role)     

            if characteres_roles:
                HTTPDataHandler.handle_response(self, 200, character_roles)
            else:
                HTTPDataHandler.handle_response(self, 204, [])            
        
        elif self.path.startswith("/characters/"):            
            index = int(self.path.split("/")[-1])
            response_data = self.controller.read_character_id(index)
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):

        if self.path.startswith("/characters/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            update_character = self.controller.update_character(index, data)
            if update_character:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Índice de character no válido"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):

        if self.path.startswith("/characters/"):
            index = int(self.path.split("/")[2])
            deleted_character = self.controller.delete_character(index)
            if deleted_character:
                HTTPDataHandler.handle_response(self, 200, {"message": "paciente eliminado correctamente"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Índice de paciente no válido"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=CharacterHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor HTTP...")
        httpd.server_close()
        print("Servidor detenido correctamente.")

if __name__ == "__main__":
    run()