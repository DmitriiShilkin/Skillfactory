# список ходов (игровое поле)
moves = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
]

# список рзрешенных ходов
permit_moves = [(0, 0), (0, 1), (0, 2),
                (1, 0), (1, 1), (1, 2),
                (2, 0), (2, 1), (2, 2)]

# список победных линий
wins = [[(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]]
    
game_over = False


print("Давайте сыграем в игру Крестики-нолики:")

player_symb = input("Чем будете ходить - крестиком (x) или ноликом (o)? Крестик ходит первым! ")

while player_symb not in ["x", "o", "х", "о"]:
    player_symb = input("Неверный ввод. Введите x или o: ")

if player_symb == "x" or player_symb == "х":
    comp_symb = "o"
else:
    comp_symb = "x"
 

# отрисовка игрового поля
def draw(mv):
    print()
    print(f"  | 0 | 1 | 2 |")
    print("---------------")
    for i in range(3):
        print(i, end=" | ")
        for j in range(3):
            print(f"{mv[i][j]}", end=" | ")
        print()
        print("---------------")
    print()

# поиск линии с нужным количеством фигур для победы или хода
def chk_moves(c_moves, p_moves, cs = comp_symb, ps = player_symb):
    move = None
    for row in wins:
        cm = 0
        pm = 0

        for j in range(0,3):
            if moves[row[j][0]][row[j][1]] == cs:
                cm +=1
            if moves[row[j][0]][row[j][1]] == ps:
                pm +=1

        if cm == c_moves and pm == p_moves:
            for j in range(0,3):
                if moves[row[j][0]][row[j][1]] != cs and moves[row[j][0]][row[j][1]] != ps:
                    move = (row[j][0], row[j][1])
    return move

# ход компьютера
def c_move(cs = comp_symb, ps = player_symb):
    move = None
    # если на какой-либо из победных линий 2 фигуры компьютера и 0 фигур игрока, компьютер ходит и выигрывает
    move = chk_moves(2,0)

    # если на какой-либо из победных линий 0 фигур компьютера и 2 фигуры игрока, компьютер мешает победить игроку
    if move is None:
        move = chk_moves(0,2)

    # если центр пуст, то компьютер занимает его
    if move is None:
        if moves[1][1] != cs and moves[1][1] != ps:
            move = (1, 1)

    # если центр занят, то компьютер занимает первую ячейку
    if move is None:
        if moves[0][0] != cs and moves[0][0] != ps:
            move = (0, 0)

    # если первая ячейка занята, то компьютер занимает вторую ячейку
    if move is None:
        if moves[0][1] != cs and moves[0][1] != ps:
            move = (0, 1)

    # если вторая ячейка занята, то компьютер занимает третью ячейку
    if move is None:
        if moves[0][2] != cs and moves[0][2] != ps:
            move = (0,2)

    # если третья ячейка занята, то компьютер занимает четвертую ячейку
    if move is None:
        if moves[1][0] != cs and moves[1][0] != ps:
            move = (1, 0)

    # если четвертая ячейка занята, то компьютер занимает шестую ячейку
    if move is None:
        if moves[1][2] != cs and moves[1][2] != ps:
            move = (1, 2)
    
    # если шестая ячейка занята, то компьютер занимает седьмую ячейку
    if move is None:
        if moves[2][0] != cs and moves[2][0] != ps:
            move = (2, 0)
    
    # если седьмая ячейка занята, то компьютер занимает восьмую ячейку
    if move is None:
        if moves[2][1] != cs and moves[2][1] != ps:
            move = (2, 1)
    
    # если восьмая ячейка занята, то компьютер занимает девятую ячейку
    if move is None:
        if moves[2][2] != cs and moves[2][2] != ps:
            move = (2, 2)

    if move is not None:
        print(f"Компьютер сделал ход по координатам: {move}")

    return move

# ход игрока
def pl_move():
    move = None
    while True:
        pl_input = input("Введите координаты Вашего хода (разделенные пробелом): ").replace(" ", "")
        try:
            int(pl_input)
        except ValueError:
            print("Этот ход не допустим!")
            continue
        move = tuple(map(int, pl_input))
        if move in permit_moves and moves[move[0]][move[1]] != comp_symb and moves[move[0]][move[1]] != player_symb:
            break
        else:
            print("Этот ход не допустим!")

    return move

# проверка результатов игры
def get_result(cs = comp_symb, ps = player_symb):
    win = ""
    stop = []
 
    for row in wins:
        if moves[row[0][0]][row[0][1]] == cs and moves[row[1][0]][row[1][1]] == cs and moves[row[2][0]][row[2][1]] == cs:
            win = "компьютер"
        if moves[row[0][0]][row[0][1]] == ps and moves[row[1][0]][row[1][1]] == ps and moves[row[2][0]][row[2][1]] == ps:
            win = "игрок"
        
    for i in moves:
        for j in range(0, len(i)):
            stop.append(i[j])

    if "-" not in stop:
        win = "ничья"

    return win

if player_symb in ["x", "х"]:
    player_move = pl_move()
    moves[player_move[0]][player_move[1]] = player_symb
    draw(moves)
    comp_move = c_move()
    moves[comp_move[0]][comp_move[1]] = comp_symb
else:
    comp_move = c_move()
    moves[comp_move[0]][comp_move[1]] = comp_symb
    player_move = (3,3)


while not game_over:
    draw(moves)
    player_move = pl_move()
    moves[player_move[0]][player_move[1]] = player_symb
    draw(moves)
    comp_move = c_move()

    if comp_move is not None:
        moves[comp_move[0]][comp_move[1]] = comp_symb 
        win = get_result()
        
        if win != "":
            game_over = True
        else:
            game_over = False

    else:
        game_over = True
        win = "ничья"
        
         
# Игра окончена, рисуем игровое поле, объявляем победителя.        
draw(moves)
if win != "ничья":
    print(f"Победил {win}!")
else:
    print("Ничья!")