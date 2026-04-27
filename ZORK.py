import random

riddles =[
{"riddle":"What has to be broken before you can use it?","answer":"egg"},
{"riddle":"I'm tall when I'm young, and I'm short when I'm old. What am I?","answer":"candle"},
{"riddle":"What month of the year has 28 days?","answer":"all"},
{"riddle":"What is full of holes but still holds water?","answer":"sponge"},
{"riddle":"What question can you never answer yes to?","answer":"are you asleep yet"},
{"riddle":"What is always in front of you but can't be seen?","answer":"future"},
{"riddle":"There's a one-story house where everything is yellow. What color are the stairs?","answer":"none"},
{"riddle":"What can you break, even if you never pick it up or touch it?","answer":"promise"},
{"riddle":"What goes up but never comes down?","answer":"age"},
{"riddle":"A man outside in the rain without an umbrella didn't get wet. Why?","answer":"he was bald"},
{"riddle":"What gets wet while drying?","answer":"towel"},
{"riddle":"What can you keep after giving to someone?","answer":"word"},
{"riddle":"I shave every day, but my beard stays the same. What am I?","answer":"barber"},
{"riddle":"You see a boat filled with people, yet there isn't a single person on board. How?","answer":"all the people on the boat are married"},
{"riddle":"You walk into a room with a match, a lamp, a candle and a fireplace. What would you light first?","answer":"match"},
{"riddle":"A man dies of old age on his 25th birthday. How is this possible?","answer":"born on february 29"},
{"riddle":"I have branches, but no fruit, trunk or leaves. What am I?","answer":"bank"},
{"riddle":"What can't talk but will reply when spoken to?","answer":"echo"},
{"riddle":"The more of this there is, the less you see. What is it?","answer":"darkness"}
]


class Chest:
    def __init__(self, color, has_key):
        self.color = color
        self.has_key = has_key
        self.is_open = False

    def open(self):
        self.is_open = True
        print(f"{self.color} chest is open")


class Dragon:
    def __init__(self, riddle, answer):
        self.riddle = riddle
        self.answer = answer
        self.silent = False
        self.told = False
        self.riddle_active = False

    def ask(self):
        self.riddle_active = True
        print(f"Dragon asks '{self.riddle}'")

    def check_answer(self, user_answer, key_chest_color):
        if user_answer == self.answer:
            self.told = True
            self.riddle_active = False
            print(f'Dragon says correct, the key is in the {key_chest_color} chest.')
        else:
            self.silent = True
            self.riddle_active = False
            print("Dragon says wrong. It will not speak again.")


class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room
        self.has_key = False
        self.exit_unlocked = False


class Map:
    def __init__(self):
        self.opposites = {"north":"south", "south":"north", "east":"west", "west":"east"}
        self.directions = list(self.opposites.keys()) #["north", "south", "east", "west"]
        colors = ["Green", "Yellow", "Red", "Blue", "White"]
        random.shuffle(colors)
        self.every_state = {}
        for color in colors:
            self.every_state[color] = {"chest": None, "dragon": None}
        self.build_connections(colors)
        
    def build_connections(self, rooms):
        connected = [rooms[0]]
        remaining = rooms[1:]

        while remaining:
            room_a = random.choice(connected)
            room_b = random.choice(remaining)
            free_a = []
            for d in self.directions:
                if d not in self.every_state[room_a]:
                    free_a.append(d)
            free_b = []
            for d in self.directions:
                if d not in self.every_state[room_b]:
                    free_b.append(d)
            shared = []
            for d in free_a:
                if self.opposites[d] in free_b:
                    shared.append((d, self.opposites[d]))
            if not shared:
                continue
            result = random.choice(shared)
            d_a = result[0]
            d_b = result[1]
            self.every_state[room_a][d_a] = room_b
            self.every_state[room_b][d_b] = room_a
            connected.append(room_b)
            remaining.remove(room_b)



class Game:
    def __init__(self):
        self.map = Map()
        rooms = list(self.map.every_state.keys())

        self.current_room = random.choice(rooms)
        valid_exit_rooms = []
        for r in rooms:
            if r != self.current_room:
                number_of_doors = len(self.map.every_state[r]) - 2
                if number_of_doors < 4:
                    valid_exit_rooms.append(r)
        self.exit_room = random.choice(valid_exit_rooms)

        placeable = []
        for r in rooms:
            if r != self.exit_room:
                placeable.append(r)

        chest_rooms = random.sample(placeable, 2)
        key_chest_room = random.choice(chest_rooms)
        for r in chest_rooms:
            if r == chest_rooms[0]:
                color = "Gold"
            else:
                color = "Silver"

            if r == key_chest_room:
                has_key = True
            else:
                has_key = False

            self.map.every_state[r]["chest"] = Chest(color, has_key)


        valid_dragon_rooms = []
        for r in placeable:
            if r not in chest_rooms:
                valid_dragon_rooms.append(r)
        dragon_room = random.choice(valid_dragon_rooms)

        riddle = random.choice(riddles)
        new_dragon = Dragon(riddle["riddle"], riddle["answer"])
        self.map.every_state[dragon_room]["dragon"] = new_dragon

        self.player = Player(self.current_room)
        self.game_over = False
        self.in_dragon_conversation = False

    def describe_room(self):
        room = self.map.every_state[self.current_room]

        door_parts = []
        for d in room:
            if d not in ("chest", "dragon"):
                door_parts.append(f"a door {d}")

        if self.current_room == self.exit_room:
            if self.player.exit_unlocked:
                status = "unlocked"
            else:
                status = "locked"
            door_parts.append(f"the exit. Exit is {status}")

        print(f"\nYou're in the {self.current_room} room. There is " + " and ".join(door_parts) + ".")

        if room["chest"] and not room["chest"].is_open:
            print(f"There is a {room["chest"].color} chest.")
        if room ["dragon"]:
            print ("There is a dragon here.")
        if self.player.has_key:
            print ("(You have the exit key)")



    def handle_command(self, command):
        room = self.map.every_state[self.current_room]
        dragon = room["dragon"]
        chest = room["chest"]

        if command.startswith("go "):
            direction = command[3:]
            if direction in room:
                self.current_room = room[direction]
                self.describe_room()
            else:
                print("You can't go that way.")

        elif command == "talk to dragon":
            if not dragon:
                print("There is no dragon here.")

            elif dragon.silent:
                print("The dragon ignores you.")

            elif dragon.told:
                key_chest_color = None
                for c in self.map.every_state.values():
                    if c["chest"] and c["chest"].has_key:
                        key_chest_color = c["chest"].color
                print(f"The dragon told you. The key is in the {key_chest_color} chest.")
            else:
                self.in_dragon_conversation = True
                print("Dragon says you need to answer a question to tell you where the key is.")
                print("Type 'ask me' when you are ready.")

        elif command == "ask me":
            if not dragon:
                print("There is no dragon here.")
            elif dragon.silent:
                print("The dragon turns away.")
            elif dragon.told:
                print("The dragon has already told you everything.")
            else:
                dragon.ask()

        elif dragon and dragon.riddle_active:
            key_chest = None
            for c in self.map.every_state.values():
                if c["chest"] and c["chest"].has_key:
                    key_chest = c["chest"]
            dragon.check_answer(command, key_chest.color)
            self.in_dragon_conversation = False

        elif command == "open chest":
            if not chest:
                print("There is no chest here.")
            elif chest.is_open:
                print(f"The {chest.color} chest is already open.")
            else:
                chest.open()
                if not chest.has_key:
                    print("The other chest just locked permanently. You lose!")
                    self.game_over = True

        elif command == "get key":
            if chest and chest.is_open and chest.has_key:
                self.player.has_key = True
                print("You have the exit key now")
            else:
                print("There is no open chest with a key here.")

        elif command == "unlock exit":
            if self.current_room != self.exit_room:
                print("There is no exit here.")
            elif not self.player.has_key:
                print("You don't have the key, exit still locked")
            else:
                self.player.exit_unlocked = True
                print("The exit is unlocked now")

        elif command == "exit":
            if self.current_room != self.exit_room:
                print("There is no exit here.")
            elif not self.player.exit_unlocked:
                print("The exit is locked.")
            else:
                print("Congratulations! You made it!")
                self.game_over = True

        else:
            print(f"I don't understand '{command}'.")

    def show_actions(self):
        room = self.map.every_state[self.current_room]
        actions = []
        for d in room:
            if d not in ("chest", "dragon"):
                actions.append(f"go {d}")

        if room["dragon"] and not room["dragon"].silent:
            actions.append("talk to dragon")

        if room["chest"] and not room["chest"].is_open:
            actions.append("open chest")

        if room["chest"] and room["chest"].is_open and not self.player.has_key:
            actions.append("get key")

        if self.current_room == self.exit_room:
            if not self.player.exit_unlocked:
                actions.append("unlock exit")
            else:
                actions.append("exit")

        print("\nWhat now?")
        for action in actions:
            print(f"{action}")

    def play(self):
        print("Welcome to ZORK game. There are 5 rooms: Green, Yellow, Red, Blue, and White.")
        self.describe_room()
        while not self.game_over:
            room = self.map.every_state[self.current_room]
            dragon = room["dragon"]
            if dragon and dragon.riddle_active:
                command = input("\nYour answer: ").strip().lower()
                self.handle_command(command)
            elif self.in_dragon_conversation:
                command = input("\nPLAYER: ").strip().lower()
                self.handle_command(command)
            else:
                self.show_actions()
                command = input("\nPLAYER: ").strip().lower()
                self.handle_command(command)
        print("Bye!")


game = Game()
game.play()