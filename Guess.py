from abc import ABC, abstractmethod
from users import User, Game



class Guess(ABC):
    def __init__(self, player:User, room:str, weapon:str, suspect:str):
        self.room = room
        self.weapon = weapon
        self.player = player
        self.suspect = suspect
        super().__init__()

    @abstractmethod
    def make_guess(self):
        pass


class Accusation(Guess):
    def make_guess(self, game:Game):
        try:
            options = {"win": "Correct, you win!", "lose":"Incorrect, turn lost!"}
            # Array [character,room,weapon]
            answer = game.confidential_case
            cleaned_answer = list()

            for i in answer:
                cleaned_answer.append(i.value[0])

            if not self.player.is_accusation:
                self.player.is_accusation = True
                count = 0
                guess = [self.suspect, self.room, self.weapon]
                for i in cleaned_answer:
                    if i == guess[count]:
                        count +=1

                if count == len(cleaned_answer):
                    return options["win"]
                else:
                    return options["lose"]
            else:
                return "{} cannot make an accusation".format(self.player.name)
        except:
            return "Improper Arguments"


class Suggestion(Guess):
    def make_guess(self):
        message = ("{0} has made suggestion: {1} has committed murder "+
        "with the {2} in the {3}").format(self.player.character.name,
        self.suspect, self.weapon, self.room)
        print(message)
        print("Players other than " + self.player.character.name +
        " please press 'Reveal a Card' to attempt to disprove")
        return message

    def disprove_suggestion(self, usercards, card):
        ucards = []
        for c in usercards:
            ucards.append((c.name).lower())
            #print(ucards)
        if card in self.__dict__.values(): #checking if card is part of suggestion
            print("Validated that " + card + " is in suggestion")
            if card in ucards: #if card in current user's usercards
                #print(ucards)
                print("Validated that " + card + "is in current user's cards")
                message = "Suggestion has been disproved with " + card
            else:
                print(card + " was not part of the current user's cards")
                message = "Suggestion was unable to be disproved"
        else: #card is not part of the suggestion
            print(card + " was not part of the suggestion")
            message = "Suggestion was unable to be disproved"
        print(message)
        return message

    def move_suspect(self):
        message = self.suspect + " has been moved to " + self.room
        return message



#if __name__ == '__main__':
