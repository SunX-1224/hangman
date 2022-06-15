from random import randint
import os, time

__MAX_GUESSES = 9

def GetWord():
    with open("__words.txt",'r') as file:
        line = file.readline().split()
        wrd_index = randint(0,len(line))
        return line[wrd_index]

def Get_console_graphics():
    data, tmp = [],[]
    with open("__console_graphics.txt", 'r') as file:
        for line in file:
            if '@' in line:
                if tmp: data.append(tmp)
                tmp = []
                continue
            tmp.append(line)
    return data

def msg(m, em):
    print("\n", "|*" * 10, f"   {m}   ", "!" * 10,'\n',em)

def get_chance(score):
    t_avg = sum(score)/len(score)
    prtp = [sum(score[5*i:5*(i+1)])/5 for i in range(int(len(score)/5))]
    p_avg = 0
    for i in range(int(len(score)/5)-1):
        if (score[5*(i+1)+1] == 0 and prtp[i] > 0.5) or (score[5*(i+1)+1]>0 and prtp[i]>0 ): p_avg+=prtp[i+1]
        else : p_avg-= prtp[i]
    prob = 1.01 ** t_avg * 1.01**p_avg
    return prob

predict = lambda score:get_chance(score[1]) > get_chance(score[0])

def GameLoop(player):
    GRAPHICS = Get_console_graphics()
    WORD = GetWord()
    l_word = [WORD[i] for i in range(len(WORD))]
    l_guessed = ['-' for i in range(len(WORD))]
    guess_count = 0
    _play = True
    while _play:
        os.system("cls")
        print("#"*12, f" HANGMAN  ::::  Player : {player} ", "#"*12,"\n")
        print('\n',*GRAPHICS[guess_count])
        print('\n\n>>\t\t',*l_guessed)
        if ''.join(l_guessed) == WORD:
            msg("YOU GOT IT","\t\tGREAT JOB")
            time.sleep(3)
            return (__MAX_GUESSES-guess_count)/__MAX_GUESSES*5+5
        if guess_count == __MAX_GUESSES:
            msg(" BETTER LUCK NEXT TIME ", f"WORD : {WORD}")
            time.sleep(3)
            return 0

        inchar = input("Enter your guess : ")
        inchar = inchar[0] if inchar else ' '
        flag = True
        for i in range(len(l_word)):
            if inchar == l_word[i]:
                l_guessed[i] = inchar
                l_word[i] = 'null'
                flag = False
        guess_count+=flag

def main():
    print("__"*10, "  PVP  ", "__"*10)
    PLAYERS = [input(f"Enter player{i+1} name : ") for i in range(2)]
    SCORE = [[], []]
    while True:
        for i in range(2):
            SCORE[i].append(GameLoop(PLAYERS[i]))

        if len(SCORE[0]) >= 20:
            if input("Next Round ? (Enter 1 to play next round) : ") == '1':
                print('\n','^'*10,"   Predicted winner : ", PLAYERS[predict(SCORE)], '  ','-'*10)
                continue
            else: break

    os.system("cls")
    high_score = max([sum(SCORE[0]), sum(SCORE[1])])
    for i in range(2):
        print(f"\n{PLAYERS[i]} {'WINNER' if sum(SCORE[i]) == high_score else 'LOSER '}  : {SCORE[i]}")
    if input("Rematch ? ( Enter 1) : ") == '1': main()

if __name__ == "__main__":
    main()