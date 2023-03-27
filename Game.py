from Player import *

TIMEOUT = 10

class Game:
    def __init__(self, players):

        if not players:
            print("Number of Players should be at least one.")
            exit(-1)

        cards = [Card(color, type) for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type) for type in BLACK_CARD_TYPES]
        shuffle(cards)

        self.deck = Deck(cards)
        self.players = players
        self.current_player_index = 0
        self.current_card = None
        self.direction = 1

    def reverse_card_clicked(self):
        self.direction = -1
        self.current_player_index = None
        return self

    def can_play(self, card):
        """
        :param: card
        :return: whether card can be played(True) or not(False)
        """
        if card.color == self.current_card.color or card.type == self.current_card.type or card.color == "black":
            return True
        return False

    def auto_draw_card(self):
        print("카드 선택 시간을 초과하였습니다. 자동으로 카드를 뽑아옵니다.")
        self.players[self.current_player_index].draw_card(self.deck)
        return -1

    def deal_cards(self):
        for i in range(7):
            for player in self.players:
                player.draw_card(self.deck)

    def pick_current_card(self):
        while True:
            self.current_card = self.deck.pop_card()
            if self.current_card.color != "black":
                break
            else:
                self.deck.cards.append(self.current_card)
                shuffle(self.deck.cards)

    def start(self):

        while True:
            # 현재 플레이어
            player = self.players[self.current_player_index]

            # 현재 카드 출력
            print(f"\n현재 카드: {self.current_card}")

            # 플레이어의 카드 출력
            print(f"\n{player.name} 턴입니다. 당신의 카드는:")
            for i, card in enumerate(player.cards):
                print(f"\t{i+1}.{card}")

            card_indexes_can_play = [idx for idx, card in enumerate(player.cards) if self.can_play(card)]
            if not card_indexes_can_play:
                print("낼 수 있는 카드가 없습니다. 자동으로 카드를 뽑습니다.")
                self.players[self.current_player_index].draw_card(self.deck)
            else:
                # TODO 일정 시간동안 입력이 없으면 자동으로 카드를 뽑아오는 코드
                # start_time = time.time()
                # card_index = -1
                # while True:
                #     if time.time() - start_time > 2:
                #         break
                #     card_index = int(input("카드를 선택하세요 (카드를 뽑으려면 0을 입력하세요): ")) - 1
                #     if card_index:
                #         break

                card_index = int(input("카드를 선택하세요 (카드를 뽑으려면 0을 입력하세요): ")) - 1

                # 플레이어가 카드를 뽑는 경우
                if card_index == -1:
                    drawn_card = player.draw_card(self.deck)
                    print(f"\n뽑은 카드: {drawn_card}")

                    # 덱에 카드가 없는 경우
                    if not self.deck.cards:
                        print("더이상 카드가 없습니다.")
                        break

                # 선택한 카드가 유효한 경우
                elif self.can_play(player.cards[card_index]):
                    played_card = player.play_card(card_index)
                    print(f"\n{player.name} 낸 카드는 {played_card}입니다")
                    self.current_card = played_card

                    # 특수 카드 처리(skip, reverse, +2, wildcard, +4)
                    if played_card.type == 'skip':
                        self.current_player_index += self.direction
                    elif played_card.type == 'reverse':
                        self.direction *= -1
                    elif played_card.type == '+2':
                        next_player_index = (self.current_player_index + self.direction) % len(self.players)
                        self.players[next_player_index].draw_card(self.deck)
                        self.players[next_player_index].draw_card(self.deck)
                    elif played_card.type == 'wildcard':
                        chosen_color = input("Choose color (red, yellow, green, blue): ")
                        self.current_card.color = chosen_color
                    elif played_card.type == '+4':
                        chosen_color = input("Choose color (red, yellow, green, blue): ")
                        next_player_index = (self.current_player_index + self.direction) % len(self.players)
                        self.players[next_player_index].draw_card(self.deck)
                        self.players[next_player_index].draw_card(self.deck)
                        self.players[next_player_index].draw_card(self.deck)
                        self.players[next_player_index].draw_card(self.deck)
                        self.current_card.color = chosen_color

                    # 게임 종료
                    if len(player.cards) == 0:
                        print(f"\n{player.name} 승리했습니다!")
                        break

                # 선택한 카드가 유효하지 않은 경우
                else:
                    print("낼 수 없는 카드입니다.")
                    continue

                # 다음 플레이어로 넘어가기
                self.current_player_index = (self.current_player_index + self.direction) % len(self.players)


if __name__ == "__main__":

    player1 = Player("Player 1")
    player2 = Player("com1")
    player3 = Player("com2")
    game = Game([player1, player2, player3])
    game.start()

