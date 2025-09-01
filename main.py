import random, time
import asyncio
import words as w

random.seed(time.time())
L = w.word_list
word = L[random.randint(0,len(L))]

import pygame as pg
pg.init()

win_width = 500
win_height = 700
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Guess The Word')

white = (255, 255, 255)
black = (170,245,255)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)

font = pg.font.Font(None, 70)

game_board = [[' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ']]


count = 0
letters = 0

game_over = False
running = True

def draw_board():
    for col in range(5):
        for row in range(6):
            square = pg.Rect(col * 100 + 12, row * 100 + 12, 75, 75)
            pg.draw.rect(screen, white, square, width = 2)
            letter_text = font.render(game_board[row][col], True, gray)
            screen.blit(letter_text, (col * 100 + 30, row * 100 + 30))
    rectangle = pg.Rect(5, count * 100 + 5, win_width - 10, 90)
    pg.draw.rect(screen, green, rectangle, width = 2)


def check_match():
    global game_over
    for col in range(5):
        for row in range(6):    
            highlight = pg.Rect(col * 100 + 12, row * 100 + 12, 75, 75)
            if word[col] == game_board[row][col] and count > row:
                pg.draw.rect(screen, green, highlight)
            elif game_board[row][col] in word and count > row:
                pg.draw.rect(screen, yellow, highlight)

    for row in range(6):
        guess = ''.join(game_board[row])
        if guess == word and row < count:
            game_over = True
    

def draw_win():
    global game_over
    if count == 6:
        game_over = True
        text = font.render(f'Loser! {word}', True, white)
        screen.blit(text, (15, 610))

    if game_over and count < 6:
        text = font.render('Winner!', True, white)
        screen.blit(text, (15, 610))

async def main():
    global running, count, letters, game_over, game_board, word, word_list
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.TEXTINPUT and letters < 5 and not game_over:
                entry = event.text
                if entry != ' ':
                    game_board[count][letters] = entry
                    letters += 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE and letters > 0:
                    game_board[count][letters - 1] = ' '
                    letters -= 1

                if event.key == pg.K_SPACE and not game_over:
                    count += 1
                    letters = 0
                
                if event.key == pg.K_SPACE and game_over:
                    count = 0
                    letters = 0
                    game_over = False
                    word = random.choice(w.word_list)
                    game_board = [[' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ']]

            
        screen.fill(black)
        check_match()
        draw_board()
        draw_win()
        

        pg.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())