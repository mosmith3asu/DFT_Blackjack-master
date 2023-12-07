import numpy as np
# import matplotlib.pyplot as plt
from experimental_blocks import BlackJack,DataLogger
# from interface_utils import render_textrect
import pygame
import time

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
class Interface():
    def __init__(self):
        # Experimental Procedure
        self.practice_timepressure = None
        self.low_timepressure = None
        self.med_timepressure = None
        self.high_timepressure = None


        self.istage = 0
        self.stages = [
                    'consent',
                    'instruction0', 'instruction1',
                    'ready_practice','countdown', 'practice',
                    'ready_game','countdown', 'game',
                    'ready_game','countdown', 'game',
                    'ready_game','countdown', 'game',
                    'save', 'debrief'
                  ]

        # Window Config
        self.display_width = 800
        self.display_height = 800
        self.display_color = (42,122,95) # bg color

        self.card_color = (255,255,255)
        self.card_width = 200
        self.card_height = (3.5/2.5)*self.card_width

        self.card_font_style = 'freesansbold.ttf'
        self.card_font_sz = 40
        self.card_font_color = (0,0,0)

        # Initializing Pygame
        pygame.init()
        pygame.display.set_caption('Blackjack Study')
        self.card_font = pygame.font.Font(self.card_font_style, self.card_font_sz)
        self.surface = pygame.display.set_mode((self.display_width, self.display_height)) # create window
        self.surface.fill(self.display_color)


    ##############################
    # Drawing Utilities ##########
    ##############################
    def draw_background(self):
        self.surface.fill(self.display_color)
        # pygame.display.flip()

    def draw_bg_label(self,x,y,val,font_sz = None,font_color = None):
        if font_sz == None: font_sz = self.card_font_sz
        if font_color == None: font_color = black

        font = pygame.font.Font(self.card_font_style, font_sz)
        text = font.render(f'{val}', True, font_color, self.display_color)
        textRect = text.get_rect()
        text_width = textRect[2]
        text_height = textRect[3]

        if x == 'center': x = self.display_width / 2
        if y == 'center': y = self.display_height / 2
        elif y == 'top': y = text_height/2
        elif y == 'centertop': y = self.display_height / 3
        # elif x == 'left center': x = self.display_width / 2 - text_width - 0.1 * text_width
        # elif x == 'right center': x = self.display_width / 2 + 0.1 * text_width
        textRect.center = (x,y)
        # textRect1.left = x + 0.05 * self.card_width
        # textRect1.top = y + 0.05 * self.card_height
        self.surface.blit(text, textRect)


    def draw_page_title(self,title,font_sz = 80):
        font = pygame.font.Font(self.card_font_style, font_sz)
        text = font.render(f'{title}', True, white)
        textRect = text.get_rect()
        text_width,text_height = textRect[2], textRect[3]
        x = self.display_width / 2
        y = text_height/2
        textRect.center = (x, y)
        self.surface.blit(text, textRect)
        # pygame.draw.rect(self.surface, self.card_color, textRect)

    def draw_multiline_text(self,text,x_start,y_start,font_sz=18,ypad=0):
        x,y = x_start,y_start+ypad
        for txt_val in text:
            font = pygame.font.Font(self.card_font_style, font_sz)
            text = font.render(f'{txt_val}', True, self.card_font_color)
            textRect = text.get_rect()
            textRect.center = (x, y)
            # text_width = textRect[2]
            self.surface.blit(text, textRect)
            y += font_sz + ypad



    def draw_button(self,text,
                    font_sz=50,bg_color = (255,255,255),
                    xloc='center',yloc='bottom',
                    width = 400,height=100,):
        if xloc == 'center': x = self.display_width / 2
        elif xloc == 'centerleft': x = self.display_width / 3
        elif xloc == 'centerright': x = self.display_width* 2/ 3
        else: raise Exception(f'invalid xloc {xloc}')

        if yloc == 'center': y = self.display_height/2
        elif yloc == 'bottom': y = self.display_height - height/2
        else: raise Exception(f'invalid yloc {yloc}')

        font = pygame.font.SysFont("Arial", font_sz)
        button_text = font.render(text, True, self.card_font_color,bg_color)
        button_rect = button_text.get_rect()
        button_rect.center = (x, y)
        button_rect.width = width
        button_rect.height = height
        # text_width = textRect[2]
        self.surface.blit(button_text, button_rect)

        # if button_rect.collidepoint(event.pos):
        #     button pressed...

        return button_rect
    ##############################
    # Drawing Entities ###########
    ##############################
    def draw_hand(self,player_hand,dealer_hand):
        self.draw_card('center', 50, val=dealer_hand)  # dealer card
        self.draw_card('left center', 475, val=player_hand[0])  # player card 1
        self.draw_card('right center', 475, val=player_hand[1])  # player card 2
        # self.draw_bg_label('center', 30, val='Dealer:')
        # interface.draw_bg_label('center', 780, val='Player:')
        self.draw_bg_label('center', 380, val='Take an additional card?')
        self.draw_bg_label('center', 420, val='b=YES     n=NO')

    def draw_card(self,x,y,val):
        if x=='center': x = self.display_width/2 - self.card_width/2
        elif x=='left center': x = self.display_width/2 - self.card_width - 0.1*self.card_width
        elif x == 'right center':  x = self.display_width / 2 + 0.1*self.card_width
        # Drawing Card Rectangle
        card_rect = pygame.draw.rect(self.surface, self.card_color, pygame.Rect(x, y, self.card_width, self.card_height))

        text = self.card_font.render(f'{val}', True, self.card_font_color, self.card_color)
        textRect1 = text.get_rect()
        textRect1.left = x + 0.05 * self.card_width
        textRect1.top = y + 0.05 * self.card_height
        self.surface.blit(text, textRect1)

        textRect2 = text.get_rect()
        textRect2.left = x + self.card_width - textRect2[2] - 0.05 * self.card_width
        textRect2.top = y + self.card_height - textRect2[3] - 0.05 * self.card_height
        self.surface.blit(text, textRect2)

        # pygame.display.flip()
        # pass

    def draw_notification(self,out_of_time=False,notification_time=0.35):
        notification_tstart = time.time()
        self.surface.fill(self.display_color)

        if out_of_time:
            self.draw_bg_label('center', 'center', 'X',font_sz=100,font_color=red)
        else:
            self.draw_bg_label('center', 'center', '!',font_sz=100)
        pygame.display.flip()

        while time.time() - notification_tstart <= notification_time:  # 350 ms
            pygame.event.get()

        self.surface.fill(self.display_color)
        pygame.display.flip()

    def draw_consent(self,y_start=100):
        consent_text = ["consent",  "consent",  "consent"]

        self.draw_multiline_text(consent_text, x_start= self.display_width / 2, y_start=y_start)

    def draw_instructions(self,i, y_start = 100, font_sz = 18):
        # 8 possible player hands [12-19]
        # 9 possible dealer hands [2-10]
        # 3 time trials [] with 56 hand combinations

        instructions1 = ["You will be playing a simplified blackjack game.",
                         "",
                         "You will be given two cards at the BOTTOM of the screen",
                         "and the dealer will be given one card at the TOP of the screen.",
                         "",
                         "The goal in this game is to maximize the sum of your cards",
                         "without going over 21 such that your cards exceed the dealer’s.",
                         "",
                         "The dealer will be given the chance to draw additional cards",
                         "until the sum of their cards exceed 16.",
                         "",
                         "If the dealer goes over 21 or your sum of cards exceeds the dealer's,",
                         'you win!']

        instructions2 = ["You will play a series of 168 hands.",
                         "",
                         f"One third of hands you will be asked to make your decision within {self.low_timepressure} seconds,",
                         f"another third will ask to make your decision within {self.med_timepressure} seconds,",
                         f"and the last third will ask to make your decision within {self.high_timepressure} seconds.",
                         "",
                         "If you DO NOT make a decision within the allowed time,",
                         "You will briefly see a red 'X'",
                         "If you DO make a decision within the allowed time,",
                         "You will briefly see a black '!'",
                         "",
                         "For each hand, you will be given the opportunity to take ONE additional card.",
                         "",
                         "Based on your and the dealer's cards,",
                         "you will press the 'B' key if you want to take an additional card",
                         "and press the 'N' key if you do not want to take an additional card."]

        ready_practice = ["Before we begin the experiment,",
                         "you will be given an opportunity to practice.",
                          "",
                          "Use this time to familiarize yourself with the controls and game.",
                         f"For the PRACTICE ONLY, you will be given {self.practice_timepressure} seconds to make you choice.",
                          "",
                          "When you are ready to begin the practice round,",
                          "Click the 'Ready' button.",
                          "",
                          "If you wish to re-read the instructions,",
                          "click the 'Back' button."
                        ]
        instruction_list = [instructions1,instructions2,ready_practice]
        self.draw_multiline_text(instruction_list[i],self.display_width / 2,y_start,ypad=5)



    def draw_debrief(self,y_start = 100, font_sz = 18):
        debreif = ["Thank you for participating!",
                   "The experiment is now complete.",
                   "",
                   "Your data will be used to fit a risk-sensitive model ",
                   "of human decision-making to see if time-pressure",
                   "affects the model's accuracy.",
                   "",
                   "If you have any questions, please contact me at",
                   "mosmith3@asu.edu",
                         ]
        self.draw_multiline_text(debreif, self.display_width / 2, y_start, ypad=5)


def main():
    debug_mode = True

    # Set up experiment
    practice_timepressure = 10
    low_timepressure = 5
    med_timepressure = 4
    high_timepressure = 3
    Timepressures = [low_timepressure,med_timepressure,high_timepressure]
    np.random.shuffle(Timepressures)
    time_pressure = practice_timepressure
    igame = -1

    BJ = BlackJack()
    player_hand, dealer_hand = BJ.get_hand()

    # Set up utils
    data = DataLogger()
    n_practice = 10
    ready_delay = 5
    ready_tstart = time.time()
    hand_tstart = time.time()
    interface = Interface()
    interface.practice_timepressure = practice_timepressure
    interface.low_timepressure = low_timepressure
    interface.med_timepressure = med_timepressure
    interface.high_timepressure = high_timepressure

    back_rect = None
    next_rect = None
    close_rect = None


    ####################################################################################
    ############################## RUN EXPERIMENT ######################################
    while True:
        ################################################
        ###### INTERFACE GAMETICK ######################
        interface.draw_background()
        if interface.stages[interface.istage] == 'consent':
            interface.draw_page_title('Experiment Start')
            # interface.draw_consent()
            next_rect = interface.draw_button(text='Start', xloc='center', yloc='bottom')
            # back_rect = interface.draw_button(text='Agree', xloc='center', yloc='bottom')
        elif interface.stages[interface.istage] == 'instruction0':
            interface.draw_page_title('Instructions (1/2)')
            interface.draw_instructions(i=0)
            next_rect = interface.draw_button(text='Next', xloc='centerright', yloc='bottom')
            # back_rect = interface.draw_button(text='(B) Back', xloc='centerleft', yloc='bottom')
        elif interface.stages[interface.istage] == 'instruction1':
            interface.draw_page_title('Instructions (2/2)')
            interface.draw_instructions(i=1)
            next_rect = interface.draw_button(text='Next', xloc='centerright', yloc='bottom')
            back_rect = interface.draw_button(text='Back', xloc='centerleft', yloc='bottom')

        # PRACTICE ----------------------------------------------------------------------------
        elif interface.stages[interface.istage] == 'ready_practice':
            interface.draw_page_title('Practice Round')
            interface.draw_instructions(i=2)
            next_rect = interface.draw_button(text='Ready', xloc='centerright', yloc='bottom')
            back_rect = interface.draw_button(text='Back', xloc='centerleft', yloc='bottom')
            ready_tstart = time.time()
        elif interface.stages[interface.istage] == 'countdown':
            interface.draw_bg_label(x='center',y='centertop',val="Place your fingers on 'B' and 'N' keys")
            ready_tdur = time.time() - ready_tstart
            interface.draw_bg_label(x='center',y='center',val=f'{int(ready_delay-ready_tdur)}')
            if ready_tdur > ready_delay:
                interface.istage +=1
                BJ = BlackJack()
                player_hand, dealer_hand = BJ.get_hand()
            hand_tstart = time.time()
        elif interface.stages[interface.istage] == 'practice':
            time_pressure = practice_timepressure
            interface.draw_hand(player_hand, dealer_hand)
            hand_tdur = time.time() - hand_tstart
            if debug_mode:
                interface.draw_bg_label(x='center', y='top', val=f'{BJ.hand_index}/{n_practice}')
            if hand_tdur > time_pressure:
                interface.draw_notification(out_of_time=True)
                data.log(time_pressure, player_hand, dealer_hand, hand_tdur, 'None')
                player_hand, dealer_hand = BJ.get_hand()
                hand_tstart = time.time()
            if BJ.hand_index > n_practice:
                interface.istage += 1

        # GAMES ----------------------------------------------------------------------------
        elif interface.stages[interface.istage] == 'ready_game':
            time_pressure = Timepressures[igame]
            interface.draw_page_title(f'Game {igame+2}')
            interface.draw_bg_label(x='center',y='center',val=f"You have {time_pressure} seconds to decide")
            next_rect = interface.draw_button(text='Begin', xloc='center', yloc='bottom')
            ready_tstart = time.time()
        elif interface.stages[interface.istage] == 'countdown':
            interface.draw_bg_label(x='center',y='centertop',val="Place your fingers on 'B' and 'N' keys")
            ready_tdur = time.time() - ready_tstart
            interface.draw_bg_label(x='center',y='center',val=f'{int(ready_delay-ready_tdur)}')
            if ready_tdur > ready_delay:
                interface.istage +=1
                BJ = BlackJack()
                player_hand, dealer_hand = BJ.get_hand()
            hand_tstart = time.time()
        elif interface.stages[interface.istage] == 'game':
            time_pressure = Timepressures[igame]
            interface.draw_hand(player_hand, dealer_hand)
            if debug_mode:
                interface.draw_bg_label(x='center',y='top',val=f'G{igame}: {BJ.hand_index}/{BJ.num_hands}')
            hand_tdur = time.time() - hand_tstart
            if hand_tdur > time_pressure:
                interface.draw_notification(out_of_time=True)
                BJ.add_hand(player_hand,dealer_hand)
                player_hand, dealer_hand = BJ.get_hand()
                hand_tstart = time.time()
            if BJ.hand_index >= BJ.num_hands:
                interface.istage += 1
                igame += 1
                print(f'iGame = {igame}')


        # Debrief ----------------------------------------------------------------------------
        elif interface.stages[interface.istage] == 'save':
            interface.draw_bg_label(x='center',y='center',val=f'Saving data...')
            pygame.display.flip()
            data.save()
            interface.istage += 1

        elif interface.stages[interface.istage] == 'debrief':
            interface.draw_page_title(f'Debrief')
            interface.draw_debrief()
            close_rect = interface.draw_button(text='Close Game', xloc='center', yloc='bottom')

        # RENDER ---------------------------------------------------------------------------
        pygame.display.flip()  # render

        #########################################
        ###### GAME EVENTS ######################

        for event in pygame.event.get():
            # Key Event ----------------------------
            if event.type == pygame.KEYDOWN:
                if interface.stages[interface.istage] == 'practice' or interface.stages[interface.istage] == 'game':
                    if event.key == pygame.K_b or event.key == pygame.K_n:
                        # Log response
                        if event.key == pygame.K_b: response = 'y'
                        if event.key == pygame.K_n: response = 'n'
                        response_time = time.time() - hand_tstart
                        data.log(time_pressure,player_hand,dealer_hand,response_time,response)

                        # Start new hand
                        player_hand, dealer_hand = BJ.get_hand()
                        hand_tstart = time.time()
                        interface.draw_notification()
                if debug_mode:
                    if event.key == pygame.K_RIGHT:
                        if interface.stages[interface.istage] == 'game': igame += 1
                        interface.istage += 1

                    if event.key == pygame.K_LEFT:
                        if interface.stages[interface.istage] == 'game': igame -= 1
                        interface.istage -= 1


            # Mouse Event --------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                if interface.stages[interface.istage] != 'practice' and interface.stages[interface.istage] != 'game':
                    if next_rect.collidepoint(event.pos): interface.istage +=1
                    elif back_rect is not None and back_rect.collidepoint(event.pos):  interface.istage -=1
                    elif close_rect is not None and close_rect.collidepoint(event.pos):  pygame.quit(); quit()
            if event.type == pygame.QUIT: pygame.quit(); quit()


def main_bu():
    time_pressure = 0
    data = DataLogger()
    BJ = BlackJack()
    hand_tstart = time.time()

    interface = Interface()
    player_hand, dealer_hand = BJ.get_hand()

    dealer_hand = 10
    player_hand = [9,2]
    while True:
        if interface.stages[interface.istage] =='consent':
            # interface.draw_background()
            interface.draw_page_title('Consent')

            # interface.draw_bg_label('center', 'center', 'Consent')
            # interface.draw_consent()
            # interface.draw_hand(player_hand, dealer_hand)
        else:
            interface.draw_hand(player_hand,dealer_hand)



        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b or event.key == pygame.K_n:
                    # Log response
                    if event.key == pygame.K_b: response = 'y'
                    if event.key == pygame.K_n: response = 'n'
                    response_time = time.time() - hand_tstart
                    data.log(time_pressure,player_hand,dealer_hand,response_time,response)

                    # Start new hand
                    player_hand, dealer_hand = BJ.get_hand()
                    hand_tstart = time.time()
                    interface.draw_notification()








            if event.type == pygame.QUIT:
                pygame.quit()

                # quit the program.
                quit()

            # Draws the surface object t




if __name__ == "__main__":
    main()
