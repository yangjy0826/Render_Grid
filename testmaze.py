import numpy as np
import math


class MazeFactory:
    def __init__(self, command):  # command is the input string (2 rows)
        self.command = command

    def Create(self):
        self.error = 0
        if self.command.count('\n') != 1:  # determine 3rd error
            self.error = 3
            self.maze = np.array([], dtype='int32')
        else:
            [size, connection] = self.command.split('\n')
            if len(size.split(' ')) != 2:  # determine 3rd error
                self.error = 3
                self.maze = np.array([], dtype='int32')
            else:
                global m
                global n
                [m, n] = size.split(' ')  # m is the No. of rows of the road grid, and n is the No. of columns
                if is_number(m) == False or is_number(n) == False:  # determine 1st error
                    self.error = 1
                    self.maze = np.array([], dtype='int32')
                else:
                    if float(m) <= 0 or float(n) <= 0 or float(m) != math.floor(float(m)) or float(n) != math.floor(float(n)):  # determine 2nd error
                        self.error = 2
                        self.maze = np.array([], dtype='int32')
                    else:
                        m = int(m)
                        n = int(n)
                        self.maze = np.zeros([2*m+1, 2*n+1])  # 0 stands for wall, and 1 stands for road
                        for i in range(m):  # create render grid without connection roads
                            for j in range(n):
                                self.maze[2*(i+1)-1][2*(j+1)-1] = 1
                        if connection.find(';;') != -1 or connection[len(connection)-1] == ';':  # determine 3rd error
                            self.error = 3
                            self.maze = np.array([], dtype='int32')
                        else:
                            connections = connection.split(';')
                            for i in range(len(connections)):  # create connection roads
                                if self.error != 0:
                                    break
                                if connections[i].find(' ') == -1 or len(connections[i].split(' ')) != 2\
                                        or connections[i][len(connections[i])-1] == ' ':  # determine 3rd error
                                    self.error = 3
                                    self.maze = np.array([], dtype='int32')
                                else:
                                    [cell1, cell2] = connections[i].split(' ')
                                    if cell1.count(',') != 1 or len(cell1.split(',')) != 2 \
                                            or cell2.count(',') != 1 or len(cell2.split(',')) != 2:  # determine 3rd error
                                        self.error = 3
                                        self.maze = np.array([], dtype='int32')
                                    else:
                                        [cell1_x, cell1_y] = cell1.split(',')
                                        [cell2_x, cell2_y] = cell2.split(',')
                                        if is_number(cell1_x) == False or is_number(cell1_y) == False\
                                                or is_number(cell2_x) == False or is_number(cell2_y) == False:  # determine 1st error
                                            self.error = 1
                                            self.maze = np.array([], dtype='int32')
                                        else:
                                            if not (0 <= float(cell1_x) < m and 0 <= float(cell2_x) < m  # determine 2nd error
                                                    and 0 <= float(cell1_y) < n and 0 <= float(cell2_y) < n
                                                    and float(cell1_x) == math.floor(float(cell1_x)) and float(cell1_y) == math.floor(float(cell1_y))
                                                    and float(cell2_x) == math.floor(float(cell2_x)) and float(cell2_y) == math.floor(float(cell2_y))):
                                                self.error = 2
                                                self.maze = np.array([], dtype='int32')
                                            else:
                                                cell1_x = int(cell1_x)
                                                cell1_y = int(cell1_y)
                                                cell2_x = int(cell2_x)
                                                cell2_y = int(cell2_y)
                                                if not ((abs(cell1_x-cell2_x) == 1 and cell1_y == cell2_y)
                                                        or (abs(cell1_y-cell2_y) == 1 and cell1_x == cell2_x)):  # determine 4th error
                                                    self.error = 4
                                                    self.maze = np.array([], dtype='int32')
                                                else:
                                                    cell1_x = 2*(cell1_x+1)-1
                                                    cell1_y = 2*(cell1_y+1)-1
                                                    cell2_x = 2*(cell2_x+1)-1
                                                    cell2_y = 2*(cell2_y+1)-1
                                                    self.maze[int((cell1_x + cell2_x)/2)][int((cell1_y + cell2_y)/2)] = 1
        return self.maze

    def Render(self):
        if self.error == 1:
            self.mazeText = 'Invalid number format​.'
        elif self.error == 2:
            self.mazeText = 'Number out of range​.​'
        elif self.error == 3:
            self.mazeText = 'Incorrect command format​.​'
        elif self.error == 4:
            self.mazeText = 'Maze format error.'
        else:  # no error with input command
            self.mazeText = ''
            for i in range(2 * m + 1):  # create render grid without connection roads
                for j in range(2 * n + 1):
                    if self.maze[i][j] == 1:
                        self.mazeText += '[R]'
                    else:
                        self.mazeText += '[W]'
                self.mazeText += '\n'
            self.mazeText = self.mazeText.replace("][", "] [")
        return self.mazeText


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# correct
command = '3 3\n0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 正确输入，行等于列
# command = '3 3\n0,1 0,2'  # 正确输入，行等于列，只有一条连线
# command = '5 4\n' + '0,0 0,1;0,1 1,1;2,2 2,3;2,2 3,2;4,0 4,1;4,2 4,3'  # 正确输入，行大于列
# command = '4 5\n' + '0,0 0,1;0,1 1,1;2,2 2,3;2,2 3,2;0,4 1,4;2,4 3,4'  # 正确输入，行小于列
# error1 Invalid number format​.
# command = '。 3\n0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入字符串中有无效的符号
# command = '3 3\n0,1 0,2;0,a 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入字符串中有字母
# error2 Number out of range​.
# command = '3.3 3\n0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1' # 输入数字有小数
# command = '3 3\n-1,1.1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入数字有负数
# command = '3 3\n0,1 0,2;0,0 1,0;0,1 1,1;0,3 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入的坐标超过道路网络的范围
# error3 Incorrect command format​.
# command = '3 3 0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入字符串中没有换行
# command = '3 3\n\n0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入字符串中有两个（或以上）换行
# command = '3\n0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'# 输入矩阵的维度是一维
# command = '3 3 3\n0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'# 输入矩阵的维度是三维（或以上）
# command = '3 3 \n0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'# 输入矩阵维度时有多余的空格
# command = '3 3\n0,1 0,2 ;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入矩阵维度时有多余的空格
# command = '3 3\n0,1 0,2;;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入字符串中有连续的分号
# command = '3 3\n0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1;'  # 输入字符串以分号为结尾
# command = '3 3\n0,10,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入字符串第二行中，两cell的坐标间缺少空格
# command = '3 3\n0,1;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 输入字符串第二行中，cell的坐标不都是成对出现
# command = '3 3\n0,,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  # 连续多个逗号
# error4 Maze format error.
# command = '3 3\n0,1 0,2;0,0 2,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'  #  输入意欲连接两个不相邻，有间隔的cell
# command = '3 3\n0,1 1,0;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1' #  输入意欲连接两个斜对角的cell
out = MazeFactory(command)
maze = out.Create()
print(maze)
mazeText = out.Render()
print(mazeText)