#builder
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs


characters = {}


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
        
    def create_character(self, post_data):
        name = post_data.get('name', None)
        level = post_data.get('level', None)
        role = post_data.get('role', None)
        charisma = post_data.get('charisma', None)
        strength = post_data.get('strength', None)
        dexterity = post_data.get('dexterity', None)

        character = self.game.create_character(name, level, role, charisma, strength, dexterity)

        id_character_nuevo = max(self.characters.keys(), default=0) + 1
        self.characters[id_character_nuevo] = character 

        return character

    
    def list_characters(self):
        return self.characters

    def read_character_id(self, id):
        return self.characters.get(id, None)
    
    def read_character_role(self, role):
        return {id_character: character for id_character, character in self.characters.items() if character.role == role}

    def update_character(self, id_character, data): 
        if id_character in characters.items():
            return self.characters.update(data)
        return None
    
    def delete_character(self, id_character):
        if id_character in self.characters:
            return self.characters.pop(id_character, None)
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
            response = self.controller.list_characters().__dict__
            HTTPDataHandler.handle_response(self, 200, response)
        
        elif self.path.startswith("/characters") and "role" in query_params:            
            role = query_params["role"][0]
            character_roles = self.controller.read_character_role(role)     

            if character_roles:
                HTTPDataHandler.handle_response(self, 200, character_roles)
            else:
                HTTPDataHandler.handle_response(self, 204, [])            
        
        elif self.path.startswith("/characters/"):            
            index = int(self.path.split("/")[-1])
            response_data = self.controller.read_character_id(index).__dict__
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):

        if self.path.startswith("/characters/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            updated_character = self.controller.update_character(index, data)
            if updated_character:
                HTTPDataHandler.handle_response(self, 200, updated_character.__dict__)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Índice de personaje no válido"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):

        if self.path.startswith("/characters/"):
            index = int(self.path.split("/")[2])
            deleted_character = self.controller.delete_character(index)
            if deleted_character:
                HTTPDataHandler.handle_response(self, 200, {"message": "Personaje eliminado correctamente"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Índice de personaje no válido"})
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
