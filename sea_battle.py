from random import randint  # импорт генератора случайных целых чисел
from time import sleep      # импорт временной задержки
from os import system       # импорт метода для очистки экрана

#размер игрового поля
board_size = 6



# классы исключений
class BoardExeption(Exception):
    pass



class BoardOutException(BoardExeption):
    def __str__(self):
        return "Выстрел за пределами игрового поля! "



class BoardRepeatShotException(BoardExeption):
    def __str__(self):
        return "Выстрел в уже открытую клетку! "



class BoardWrongShipCoordsException(BoardExeption):
    def __str__(self):
        return "Невозможно разместить корабль по указанным координатам! "



# класс точки для размещения кораблей и проверки хода
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # сравнение точек
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    # формат вывода точки
    def __repr__(self):
        return f"Dot({self.x}, {self.y})"



# класс описания корабля
class Ship:
    def __init__(self, start, length, orient):
        self.length = length
        self.start = start
        self.orient = orient
        self.lives = length

    # точки корабля
    @property
    def get_dots(self):
        coords = []
        h = v = 1
        if self.orient == 0:
            v = self.length
        elif self.orient == 1:
            h = self.length
        for x in range(self.start.x, self.start.x + h):
            for y in range(self.start.y, self.start.y + v):
                coords.append(Dot(x, y))
        return coords


    # признак, что корабль ранен
    def is_hit(self, dot):
        return dot in self.get_dots


    # признак, что корабль убит
    def is_killed(self):
        return self.lives == 0



# класс игрового поля
class Board:
    def __init__(self, hid=False, size=board_size):
        self.hid = hid
        self.size = size

        self.count = 0

        self.blank_symb = "O"

        self.hit_symb = "X"

        self.miss_symb = "."

        self.occupied = []

        self.ships = []

        self.field = [[self.blank_symb]*self.size for i in range(self.size)]

        self.hit_dot = None

        self.kill = None

        self.killed_ship = None


    # формирование таблицы представления данных для вывода на экран
    def __str__(self):
        if board_size < 10:
            table = "   │ "
            for i in range(1, self.size + 1):
                table += f"{i} │ "
            table += "\n" + "───┼" * self.size + "───┤ "
            for j in range(self.size):
                table += f"\n {j + 1} │ "
                for k in range(self.size):
                    table += f"{self.field[j][k]} │ "
                if j != (self.size - 1):
                    table += "\n" + "───┼" * self.size + "───┤ "
                else:
                    table += "\n" + "───┴" * self.size + "───┘ "

            if self.hid:
                table = table.replace("■", self.blank_symb)
        else:
            table = "    │ "
            for i in range(1, self.size + 1):
                table += f"{i:2} │ "
            table += "\n" + "────┼" * self.size + "────┤ "
            for j in range(self.size):
                table += f"\n {(j + 1):2} │ "
                for k in range(self.size):
                    table += f"{self.field[j][k]:2} │ "
                if j != (self.size - 1):
                    table += "\n" + "────┼" * self.size + "────┤ "
                else:
                    table += "\n" + "────┴" * self.size + "────┘ "

            if self.hid:
                table = table.replace("■", self.blank_symb)            

        return table


    # признак того, что точка находится за пределами игрового поля
    def out_of_field(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))


    # метод добавления корабля
    def add_ship(self, ship):
        for dot in ship.get_dots:
            if self.out_of_field(dot) or dot in self.occupied:
                raise BoardWrongShipCoordsException()
        for dot in ship.get_dots:
            self.field[dot.x][dot.y] = "■"
            self.occupied.append(dot)
        
        self.ships.append(ship)
        self.contour(ship)


    # метод добавления контрура корабля
    def contour(self, ship, mark = False):
        around = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.get_dots:
            for dx, dy in around:
                current = Dot(dot.x + dx, dot.y + dy)
                if (not self.out_of_field(current)) and (current not in self.occupied):
                    if mark:
                        self.field[current.x][current.y] = "."
                    self.occupied.append(current)


    # метод проверки результата выстрела
    def shot(self, dot):
        if self.out_of_field(dot):
            raise BoardOutException()
        
        if dot in self.occupied:
            raise BoardRepeatShotException()

        self.occupied.append(dot)

        self.kill = False
        
        for ship_ in self.ships:
            if ship_.is_hit(dot):
                ship_.lives -= 1
                self.field[dot.x][dot.y] = self.hit_symb
                if ship_.is_killed():
                    self.count += 1
                    self.contour(ship_, mark = True)
                    print("Корабль уничтожен! ")
                    self.kill = True
                    self.killed_ship = ship_
                    return False
                else:
                    print("Корабль ранен! ")
                    self.hit_dot = dot
                    return True
        self.field[dot.x][dot.y] = self.miss_symb
        print("Мимо! ")
        return False
        

    # очистка игрового поля
    def begin(self):
        self.occupied = []


    # признак проигрыша
    def is_lose(self):
        return self.count == len(self.ships)


    # расстановка кораблей в ручном режиме
    def ask_ship_loc(self):
        while True:
            if g.ship_len > 1:
                text = f"Введите координаты носа {g.ship_len}-палубного корабля (цифры, разделенные пробелом): "
            else:
                text = f"Введите координаты {g.ship_len}-палубного корабля (цифры, разделенные пробелом): "
            pl_input_coords = input(text)
            try:
                x, y = map(int, pl_input_coords.split())
            except ValueError:
                print("Этот ход не допустим! ")
            else:
                if not ((0 < x <= self.size) and (0 < y <= self.size)):
                    print("Координаты за пределами игрового поля! ")
                    continue
                break

        orient = 0

        while g.ship_len != 1:
            pl_input_orient = input("Введите ориентацию корабля (0 - горизонтальная, 1 - вертикальная): ")
            try:
                orient = int(pl_input_orient)
            except ValueError:
                print("Этот ход не допустим! ")
            else:
                if orient not in [0, 1]:
                    print("Число должно быть 0 или 1! ")
                    continue
            break

        return Dot(x - 1, y - 1), orient 



# класс игрока
class Player:
    def __init__(self, self_board, enemy_board, size=board_size):
        self.board = self_board
        self.enemy = enemy_board
        self.size = size
        self.shots = []
        self.hit_dots = []


    # метод запроса координат выстрела
    def ask_move(self):
        raise NotImplementedError


    # метод, реализующий выстрел
    def move(self):
        while True:
            try:
                target = self.ask_move()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExeption as e:
                print(e)



# класс игрока-компьютера
class AI(Player):
    
    # переопределение метода запроса координат выстрела
    def ask_move(self):
        
        if self.hit_dots != []:
            dot = self.finish_off()
        else:    
            while True:
                dot = Dot(randint(0, self.size - 1), randint(0, self.size - 1))
                if dot not in self.shots:
                    print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
                    self.shots.append(dot)
                    break

        return dot


    # добивание корабля
    def finish_off(self):

        around_xy = [
                    (-1, 0),
                (0, -1), (0, 1),
                    (1, 0)
            ]
        
        around_x = [
                (0, -1), (0, 1)
        ]

        around_y = [
                (-1, 0),
                (1, 0)
        ]

        around = around_xy

        dx = dy = 1

        if len(self.hit_dots) > 1:
            dx = self.hit_dots[1].x - self.hit_dots[0].x
            dy = self.hit_dots[1].y - self.hit_dots[0].y

        if dx == 0:
            around = around_x

        if dy == 0:
            around = around_y

        for dot_ in self.hit_dots:
            for dx, dy in around:
                current = Dot(dot_.x + dx, dot_.y + dy)
                if (not self.board.out_of_field(current)) and (current not in self.shots):
                    dot = current
                    print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
                    self.shots.append(dot)
                    return dot        


    def killed_ship_contour(self, ship):
        around = [
                (-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.get_dots:
            for dx, dy in around:
                current = Dot(dot.x + dx, dot.y + dy)
                if (not self.board.out_of_field(current)) and (current not in self.shots):
                    self.shots.append(current)

# класс игрока-человека
class User(Player):
    # переопределение метода запроса координат выстрела
    def ask_move(self):
        while True:
            pl_input = input("Введите координаты вашего хода (цифры, разделенные пробелом): ")
            try:
                x, y = map(int, pl_input.split())
            except ValueError:
                print("Этот ход не допустим! ")
            else:
                break
        
        return Dot(x - 1, y - 1)



# класс самой игры
class Game:
    def __init__(self, size=board_size):
        self.ship_lens = [3, 2, 2, 1, 1, 1, 1]
        self.ship_len = None
        self.size = size
 

    # вывод приветствия на экран
    def greet(self):
        system("cls") 
        print("┌───────────────────────────────────────────────────────────────────┐")
        print("│            Добро пожаловать в игру 'Морской бой'!                 │")
        print("│   Игрок ходит первым. В случае попадания в корабль противника     │")
        print("│ игроку дается еще один ход. Подбитые корабли помечаются буквой X, │")
        print("│ промахи и область вокруг убитого корабля (в которой не могут      │")
        print("│ находиться другие корабли и куда нельзя стрелять) - точками.      │")
        print("│   Игра идет до тех пор, пока игрок или компьютер не потопит все   │")
        print("│ корабли противника.                                               │")
        print("│   Формат ввода: x y, где x - номер строки, y - номер столбца.     │")
        print("│   Для начала игры нажмите Enter, в этом случае корабли будут      │")
        print("│ расставлены автоматически.                                        │")
        print("│   Если вы хотите расставить корабли самостоятельно - нажмите S.   │")
        print("└───────────────────────────────────────────────────────────────────┘")


    # вывод правил размещения кораблей на экран (для ручного режима размещения кораблей)
    def ship_loc_info(self):
        system("cls") 
        print("┌───────────────────────────────────────────────────────────────────┐")
        print("│                 Правила размещения кораблей                       │")
        print("│   Для размещения доступно 7 кораблей: 1 трехпалубный,             │")
        print("│ 2 двухпалубных и 4 однопалубных.                                  │")
        print("│   В целях оптимального использования пространства игрового поля,  │")
        print("│ первым размещается самый большой корабль и далее по убыванию.     │")
        print("│   Формат ввода носа корабля: x y, где x - номер строки,           │")
        print("│ y - номер столбца.                                                │")
        print("│   Формат ввода ориентации в пространстве: 0 - горизонтальное      │")
        print("│ положение, 1 - вертикальное положение.                            │")
        print("│   Если возникает ситуация, когда невозможно разместить оставшиеся │")
        print("│ корабли, после трех попыток неудачного размещения предлагается:   │")
        print("│ либо разместить все корабли заново в ручном режиме, либо в        │")
        print("│ автоматическом.                                                   │")
        print("└───────────────────────────────────────────────────────────────────┘")        


    # печать игровых полей
    def print_boards(self):
        system("cls")
        print()
        print("     Ваше игровое поле:\tИгровое поле компьютера:".expandtabs(6 * board_size + 1))
        print()
        user_board = str(self.user.board).split("\n")
        ai_board = str(self.ai.board).split("\n")
        for i in range(len(user_board)):
            print((user_board[i]+ "\t" + ai_board[i]).expandtabs(35))
        print()


    # основной игровой цикл
    def loop(self):
        num = 0
        while True:
            if num % 2 == 0:
                self.print_boards()
                print("Ваш ход!")
                repeat = self.user.move()
                sleep(5)
            else:
                self.print_boards()
                repeat = self.ai.move()

                if repeat and (self.ai.enemy.hit_dot is not None):
                    self.ai.hit_dots.append(self.ai.enemy.hit_dot)
                elif self.ai.enemy.kill:
                    self.ai.hit_dots = []
                    self.ai.killed_ship_contour(self.ai.enemy.killed_ship)

                sleep(5)
       
            if repeat:
                num -= 1

            if self.user.board.is_lose() and self.ai.board.is_lose():
                self.print_boards()
                print()
                print("Ничья!")
                print()
                break           

            if self.user.board.is_lose():
                self.ai.board.hid = False
                self.print_boards()
                print()
                print("Вы проиграли!")
                print()
                break

            if self.ai.board.is_lose():
                self.print_boards()
                print()
                print("Поздравляю, вы выиграли!")
                print()
                break

            num += 1
    

    # начало игры
    def start(self):
        choice = None
        
        while choice not in ["", "S", "s", "Ы", "ы"]:
            self.greet()
            print()
            choice = input()

        comp_board = self.random_board()
        comp_board.hid = True
          
        if choice == "":
            player_board = self.random_board()
 
        else:
            player_board = self.manual_board()
 
        self.ai = AI(comp_board, player_board)
        self.user = User(player_board, comp_board)

        self.loop()


    # попытка сгенерировать случайное расположение кораблей на игровом поле
    def try_board(self):
        board = Board()
        attempts = 0
        for length in self.ship_lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size - 1), randint(0, self.size - 1)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipCoordsException:
                    pass
        board.begin()
        return board

    # если не удалось разместить корабли в автоматическом режиме, очистка игрового поля и повтор автоматического режима
    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board


    # попытка задать расположение кораблей на игровом поле в ручном режиме
    def try_manual_board(self):
        board = Board()
        for index, self.ship_len in enumerate(self.ship_lens):
            fail = (len(self.ship_lens) - index) < 4
            attempts = 0
            while True:
                if attempts > 2:
                    print()
                    print("На поле невозможно разместить корабли! Повторить размещение?")
                    pl_input = ""
                    while pl_input not in ["Y", "y", "Н", "н", "N", "n", "Т", "т"]:
                        pl_input = input("Введите Y для повторного ручного размещения или N для автоматического размещения: ")
                        if pl_input in ["N", "n", "Т", "т"]:
                            board = self.random_board()
                            return board
                    else:
                        return None
                self.ship_loc_info()
                print()
                print(board)
                print()
                dot, orient = board.ask_ship_loc()
                ship = Ship(dot, self.ship_len, orient)
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipCoordsException as e:
                    if fail:
                        attempts += 1
                    print(e)
                    sleep(5)
                    
        board.begin()
        return board


    # если не удалось разместить корабли в ручном режиме, очистка игрового поля и повтор ручного режима
    def manual_board(self):
            board = None
            while board is None:
                board = self.try_manual_board()
            return board


g = Game()

# запуск игры
g.start()
