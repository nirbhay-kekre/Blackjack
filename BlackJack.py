from random import randint
import os


class Cards(object):
    def __init__(self, num_of_decks=4):
        self.num_of_decks = num_of_decks
        self.total_cards = 52 * self.num_of_decks
        self.deck = [('♠', ' A'), ('♠', ' 2'), ('♠', ' 3'), ('♠', ' 4'),
                     ('♠', ' 5'), ('♠', ' 6'), ('♠', ' 7'), ('♠', ' 8'),
                     ('♠', ' 9'), ('♠', '10'), ('♠', ' J'), ('♠', ' Q'),
                     ('♠', ' K'), ('♦', ' A'), ('♦', ' 2'), ('♦', ' 3'),
                     ('♦', ' 4'), ('♦', ' 5'), ('♦', ' 6'), ('♦', ' 7'),
                     ('♦', ' 8'), ('♦', ' 9'), ('♦', '10'), ('♦', ' J'),
                     ('♦', ' Q'), ('♦', ' K'), ('♥', ' A'), ('♥', ' 2'),
                     ('♥', ' 3'), ('♥', ' 4'), ('♥', ' 5'), ('♥', ' 6'),
                     ('♥', ' 7'), ('♥', ' 8'), ('♥', ' 9'), ('♥', '10'),
                     ('♥', ' J'), ('♥', ' Q'), ('♥', ' K'), ('♣', ' A'),
                     ('♣', ' 2'), ('♣', ' 3'), ('♣', ' 4'), ('♣', ' 5'),
                     ('♣', ' 6'), ('♣', ' 7'), ('♣', ' 8'), ('♣', ' 9'),
                     ('♣', '10'), ('♣', ' J'), ('♣', ' Q'), ('♣', ' K'), ] * self.num_of_decks

    def initialize(self):
        self.total_cards = 52 * self.num_of_decks
        self.deck = [('♠', ' A'), ('♠', ' 2'), ('♠', ' 3'), ('♠', ' 4'),
                     ('♠', ' 5'), ('♠', ' 6'), ('♠', ' 7'), ('♠', ' 8'),
                     ('♠', ' 9'), ('♠', '10'), ('♠', ' J'), ('♠', ' Q'),
                     ('♠', ' K'), ('♦', ' A'), ('♦', ' 2'), ('♦', ' 3'),
                     ('♦', ' 4'), ('♦', ' 5'), ('♦', ' 6'), ('♦', ' 7'),
                     ('♦', ' 8'), ('♦', ' 9'), ('♦', '10'), ('♦', ' J'),
                     ('♦', ' Q'), ('♦', ' K'), ('♥', ' A'), ('♥', ' 2'),
                     ('♥', ' 3'), ('♥', ' 4'), ('♥', ' 5'), ('♥', ' 6'),
                     ('♥', ' 7'), ('♥', ' 8'), ('♥', ' 9'), ('♥', '10'),
                     ('♥', ' J'), ('♥', ' Q'), ('♥', ' K'), ('♣', ' A'),
                     ('♣', ' 2'), ('♣', ' 3'), ('♣', ' 4'), ('♣', ' 5'),
                     ('♣', ' 6'), ('♣', ' 7'), ('♣', ' 8'), ('♣', ' 9'),
                     ('♣', '10'), ('♣', ' J'), ('♣', ' Q'), ('♣', ' K'), ] * self.num_of_decks

    def draw_card(self):
        if (self.total_cards <= 39):
            self.initialize()
        self.total_cards -= 1
        return self.deck.pop(randint(0, self.total_cards))

global_cards = Cards()
try:
    width = os.get_terminal_size().columns
except:
    width =80


class CardScore(object):
    def __init__(self, cards=[], score=[0]):
        self.cards = []
        self.score = score

    def get_card_str(self):
        string = ''
        for card in self.cards:
            if (card[0] in ['♣', '♠']):
                string += ('\x1b[1;30;47m {}{} \x1b[0m '.format(card[0], card[1]))
            elif card[0] in ['♦', '♥']:
                string += ('\x1b[1;31;47m {}{} \x1b[0m '.format(card[0], card[1]))
            elif card[0] == 'face_down':
                string += ('\x1b[0;37;41m {} \x1b[0m '.format('░░░'))  # face down card
        return string

    def get_score_str(self):
        string = ''
        string += ("score: {}".format(self.score))
        if (self.score[-1] > 21):
            string += " ----BUSTED---- "
        return string

    def add_card(self, card):
        self.cards.append(card)
        return self.calculate_score(card)

    def calculate_score(self, card):
        if card[1] in [' J', ' Q', ' K']:
            score_temp = [x + 10 for x in self.score if (x + 10 <= 21)]
            if (len(score_temp) == 0):
                score_temp = [self.score[0] + 10]
        elif card[1] == ' A':
            score_temp = [x + 1 for x in self.score if x + 1 <= 21] + [x + 11 for x in self.score if x + 11 <= 21]
            if (len(score_temp) == 0):
                score_temp = [self.score[0] + 1]
        elif card[1] in [' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10']:
            score_temp = [x + int(card[1]) for x in self.score if x + int(card[1]) <= 21]
            if (len(score_temp) == 0):
                score_temp = [self.score[0] + int(card[1])]
        elif card[0] == 'face_down':
            score_temp = self.score
        self.score = list(set(score_temp))
        self.score.sort()
        return self.score


class Dealer(object):
    global global_cards

    def __init__(self):
        self.card_score = CardScore()
        self.firstmove = True
        self.peeked = False
        self.ask_for_insurance = False

    def play(self, is_player_busted):
        self.peeked = False
        if(is_player_busted):
            if(len(self.card_score.cards) ==1):
                self.hit()
            return
        while self.card_score.score[-1] < 17:
            self.hit()

    def hit(self):
        self.card_score.add_card(global_cards.draw_card())

    def distribute(self):
        if self.firstmove:
            self.hit()
            self.ask_for_insurance = self.card_score.cards[0][1] == ' A'
            self.firstmove = False

    def peek(self):
        if (len(self.card_score.cards) == 1 and self.card_score.cards[0][1] == ' A'):
            self.hit()
            self.peeked = True
            return self.card_score.score == 21

    def set_peeked(self, peeked):
        self.peeked = peeked

    def has_blackjack(self):
        return len(self.card_score.cards)==2 and self.card_score.score[-1] ==21

    def __str__(self):
        global width
        string = 'Dealer'.center(width) + "\n"
        card_space_exp = " " * (int(width / 2) - int(len(self.card_score.cards) * 5 / 2))
        if (self.peeked or len(self.card_score.cards) == 1):
            temp_card_score = CardScore()
            temp_card_score.add_card(self.card_score.cards[0])
            temp_card_score.add_card(('face_down', ''))
            string += card_space_exp + temp_card_score.get_card_str() + card_space_exp
            string += "\n" + temp_card_score.get_score_str().center(width)

        else:
            string += card_space_exp + self.card_score.get_card_str() + card_space_exp
            string += "\n" + self.card_score.get_score_str().center(width)
        return string


class Split(object):
    global global_cards

    def __init__(self, amount, card_score, player):
        self.amount = amount
        self.card_score = card_score
        self.player = player
        player.total_amount -= amount
        self.isDoublePlayed = False
        self.split_over = False
        self.isBust=False
        self.result=''

    def hit(self):
        if (self.card_score.score[-1] >= 21):
            self.split_over = True
            self.isBust= self.card_score.score[-1] > 21
            return
        self.card_score.add_card(global_cards.draw_card())
        if (self.card_score.score[-1] >= 21):
            self.isBust = self.card_score.score[-1] > 21
            self.split_over = True

    def stand(self):
        self.split_over = True

    def double(self):
        if (self.can_play_double()):
            self.isDoublePlayed = True
            self.player.total_amount -= self.amount
            self.hit()
            self.isBust = self.card_score.score[-1] > 21
            self.split_over = True

    def check_win(self, dealers_score):
        if(dealers_score > 21 and self.isBust):
            self.result='PUSH'
            self.player.push(self)
        elif(dealers_score>21):
            self.result='Win'
            if(self.isDoublePlayed):
                self.player.win(self,4)
            else:
                self.player.win(self,2)
        elif(self.isBust):
            self.result='Lost'
        elif(dealers_score == self.card_score.score[-1]):
            self.result='PUSH'
            self.player.push(self)
        elif(dealers_score > self.card_score.score[-1]):
            self.result='Lost'
        elif(dealers_score < self.card_score.score[-1]):
            self.result='Win'
            if (self.isDoublePlayed):
                self.player.win(self, 4)
            else:
                self.player.win(self, 2)

    def play(self):
        global t
        while (self.split_over == False):
            i = 1
            action = {}
            string = "press {} to hit, ".format(i)
            action[i] = self.hit
            i += 1
            string += ("press {} to stand".format(i))
            action[i] = self.stand
            if (self.can_play_double()):
                i += 1
                string += (", press {} to double".format(i))
                action[i] = self.double
            if (self.player.can_split()):
                i += 1
                string += (", press {} to split".format(i))
                action[i] = self.player.split
            while True:
                try:
                    resp = int(input(string + ": "))
                except:
                    continue
                else:
                    if (1 <= resp <= i):
                        break;
                    else:
                        continue
            func = action[resp]
            func()
            print(t)

    def can_play_double(self):
        return self.player.total_amount >= self.amount and self.isDoublePlayed == False


class Player(object):
    global global_cards

    def __init__(self, amount, total_amount=5000):
        self.total_amount = total_amount
        self.is_splited = False
        self.splits = [Split(amount, CardScore(), self)]
        self.is_player_busted=False

    def __str__(self):
        global width
        string = 'Player'.center(width)
        num_splits = len(self.splits)
        split_width = int(width / num_splits)
        card_str = ''
        score_str = ''
        bet_amount = ''
        result=''
        pointer=''
        for i in range(0, num_splits):
            if(self.splits[i].split_over):
                pointer+=" ".center(split_width)
            else:
                pointer+="*".center(split_width)
            card_space_exp = " " * (int(split_width / 2) - int(len(self.splits[i].card_score.cards) * 5 / 2))
            card_str += card_space_exp + self.splits[i].card_score.get_card_str() + card_space_exp
            score_str += self.splits[i].card_score.get_score_str().center(split_width)
            bet_amount += "bet amount : {}".format(self.splits[i].amount).center(split_width)

            if self.splits[i].result != '':
                result+="Game result : {}".format(self.splits[i].result).center(split_width)
        string += '\n'+ pointer + '\n' + card_str + '\n' + score_str + "\n" + bet_amount + "\n"+result+"\n"
        string += "total money: {}".format(self.total_amount).center(width)
        return string

    def split(self):
        if (self.can_split()):
            self.is_splited = True
            newcard_score = CardScore()
            oldcard_score = self.splits[0].card_score
            newcard_score.add_card(oldcard_score.cards.pop(0))
            oldcard_score.score = newcard_score.score
            self.splits.append(Split(self.splits[0].amount, newcard_score, self))

            newcard_score.add_card(global_cards.draw_card())
            oldcard_score.add_card(global_cards.draw_card())

        else:
            print("you can not Split!")
            return False

    def pay_insurance(self, split):
        global width
        if (self.can_pay_insurance(split)):
            self.total_amount -= int(split.amount / 2)
            print("\n" + "you have put {} as insurance".format(int(self.splits[0].amount / 2)).center(width))

    def won_insurance(self, split):
        global width
        print("\nyou won {} as insurance".format(3 * int(split.amount / 2)).center(width))
        self.total_amount += 3 * int(split.amount / 2)

    def can_split(self):
        return (self.is_splited == False and len(self.splits) == 1 and
                len(self.splits[0].card_score.cards) == 2 and
                self.splits[0].card_score.cards[0][1] == self.splits[0].card_score.cards[1][1] and
                self.total_amount >= self.splits[0].amount)

    def has_blackjack(self):
        return (len(self.splits) == 1 and
                len(self.splits[0].card_score.cards) == 2 and
                self.splits[0].card_score.score[-1] == 21)

    def push(self,split):
        if(split.isDoublePlayed):
            self.total_amount += split.amount
        self.total_amount += split.amount

    def win(self,split,multiplier):
        self.total_amount+= int(multiplier* split.amount)

    def can_pay_insurance(self, split):
        return self.total_amount >= int(split.amount / 2)

    def distribute(self):
        self.splits[0].hit()
        self.splits[0].hit()

    def check_is_player_busted(self):
        for s in self.splits:
            if(s.isBust == False):
                self.is_player_busted=False
                return
        self.is_player_busted=True
        return


    def play(self):
        i =0
        while i < len(self.splits):
            self.splits[i].play()
            i += 1


class Table(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.first_round = True
        while True:
            try:
                amt = int(input("Enter the bet amount between {} and {}: ".format(min, max)))
            except:
                print("Try again")
                continue
            else:
                if (min <= amt <= max <5000):
                    break
                else:
                    continue
        self.player = Player(amt)
        self.dealer = Dealer()

    def play(self):
        global width
        game_on = True
        while (game_on):
            self.reset_except_Player_total_amount_and_deck()
            self.player.distribute()
            self.dealer.distribute()
            print(self)
            if (self.dealer.ask_for_insurance and self.player.can_pay_insurance(self.player.splits[0])):
                if (input("do you want insurance y/n? :".center(width)).upper().startswith('Y')):
                    self.dealer.ask_for_insurance = False
                    self.player.pay_insurance(self.player.splits[0])
                    if (self.dealer.peek()):
                        print(self)
                        self.player.won_insurance(self.player.splits[0])
                        if self.player.has_blackjack():
                            self.player.splits[0].result='PUSH'
                            self.player.push()
                            print(t)
                            self.first_round = False
                            game_on = input("do you want to play one more game (y/n)?: ").upper().startswith("Y")
                            continue
                        else:
                            self.player.splits[0].result='Lost'
                            print(t)
                            self.first_round = False
                            game_on = input("do you want to play one more game (y/n)?: ").upper().startswith("Y")
                            continue
                    else:
                        print("\nYou lost the insurance".center(width))
            if(self.player.has_blackjack() ==False):
                self.player.play()
            self.player.check_is_player_busted()
            self.dealer.set_peeked(False)
            self.dealer.play(self.player.is_player_busted or self.player.has_blackjack())
            self.check_who_win()
            print(t)
            self.first_round=False
            game_on= input("do you want to play one more game (y/n)?: ").upper().startswith("Y")

    def check_who_win(self):
        if (self.player.has_blackjack() and self.dealer.has_blackjack()):
            self.player.splits[0].result='PUSH'
            self.player.push(self.player.splits[0])
        elif (self.player.has_blackjack()):
            self.player.splits[0].result = 'Win'
            self.player.win(self.player.splits[0],5/2)
        elif (self.dealer.has_blackjack()):
            for s in self.player.split():
                s.result='Lost'
        else:
            dealers_score = self.dealer.card_score.score[-1]
            for s in self.player.splits:
                s.check_win(dealers_score)

    def reset_except_Player_total_amount_and_deck(self):
        if self.first_round == False:
            total_amount = self.player.total_amount
            if(total_amount < self.min):
                print("Insufficient Amount!, adding 5000 to player's total amount")
                total_amount += 5000
        while self.first_round == False:
            try:
                amt = int(input("Enter the bet amount between {} and {}: ".format(self.min, self.max)))
            except:
                continue
            else:
                if (self.min <= amt <= self.max and amt <= total_amount ):
                    break
                else:
                    continue
        if self.first_round == False:
            del (self.player)
            del (self.dealer)
            self.player = Player(amt, total_amount)
            self.dealer = Dealer()

    def __str__(self):
        global width
        os.system('cls' if os.name == 'nt' else 'clear')
        string = self.dealer.__str__()
        string += "\n" + "-".center(width, "-")
        string += "\n" + "min : {}, max: {}".format(self.min, self.max).center(width)
        string += "\n" + "BLACKJACK PAYS 3 TO 2".center(width)
        string += "\n" + "Dealer must draw to 16, and stand on all 17's".center(width)
        string += "\n" + "Insurance pays 2 to 1".center(width)
        string += "\n" + "-".center(width, "-")
        string += "\n" + self.player.__str__()
        return string

t = Table(100,500)
t.play()