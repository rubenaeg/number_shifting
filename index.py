import sys
import math

lvl = open('./level.txt', 'r')

# Read width and height of level.
width, height = [int(i) for i in lvl.readline().split()]

# Gathers every cell with a value, plus it's position in the grid. 
def sort(field):
    cells = []
    for y in range(0, height):
        row = lvl.readline().split()
        for x in range(0, width):
            cell = int(row[x])

            if(cell == 0):
                continue

            cells.append({
                'value': cell,
                'position': {
                    'x': x,
                    'y': y
                }
            })

    return cells

def get_zero_combinations(cells):
    cell_values = list(map(lambda cell: str(cell['value']), cells))
    signs = ['+'] * len(cell_values)
    results = []

    for counter in range(2 ** len(signs)):
        test = format(counter, '0' + str(len(cell_values))  + 'b')
        for i in range(len(test)):
            if test[i] == '0':
                signs[i] = '+'
            else:
                signs[i] = '-'

        # Join signs with cellValues to check if current combination evaluates to 0.
        calcStr = [None] * (len(cell_values) + len(signs))
        calcStr[::2] = signs
        calcStr[1::2] = cell_values
        calc = ''.join(calcStr)

        result = eval(calc)

        if result == 0:
            results.append(signs[:])
    
    return results

def shift(cells, directions, count):
    count += 1
    # Threshold for max iterations set to 30.
    if len(cells) <= 1 or count > 30:
        return

    cell = cells.pop(0)
    x = cell['position']['x']
    y = cell['position']['y']
    cell_other = cell_found = None
    single = False
        
    # Calc new position L,R,D,U
    xL = x - cell['value']
    cell_found = check_pos({'x': xL, 'y': y}, cell, cells, width, height, single, 'L')
    if cell_found:
        if cell_other:
            single = False
        else: 
            cell_other = cell_found.copy()
            single = True

    xR = x + cell['value']
    cell_found = check_pos({'x': xR, 'y': y}, cell, cells, width, height, single, 'R')
    if cell_found:
        if cell_other:
            single = False
        else: 
            cell_other = cell_found.copy()
            single = True

    yU = y - cell['value']
    cell_found = check_pos({'x': x, 'y': yU}, cell, cells, width, height, single, 'U')
    if cell_found:
        if cell_other:
            single = False
        else: 
            cell_other = cell_found.copy()
            single = True

    yD = y + cell['value']
    cell_found = check_pos({'x': x, 'y': yD}, cell, cells, width, height, single, 'D')
    if cell_found:
        if cell_other:
            single = False
        else: 
            cell_other = cell_found.copy()
            single = True


    if not cell_other:
        cells.append(cell)
        return shift(cells, directions, count)

    if not single:
        return
    else: 
        # Calculate properties for new cell and append it to cells list.
        new_value = eval(cell['sign'] + str(cell['value']) + cell_other['sign'] + str(cell_other['value']))
        sign = '+' if str(new_value)[0].isdigit() else '-'
        new_sign = '+' if str(eval('%s1*%s1' %(cell['sign'], cell_other['sign'])))[0].isdigit() else '-'

        cell_new = {
            'value': abs(new_value),
            'sign': sign,
            'position': {
                'x': cell_other['position']['x'],
                'y': cell_other['position']['y']
            }
        }

        direction = '%d %d %s %s' %(cell['position']['x'], cell['position']['y'], cell['direction'], new_sign)
        directions.append(direction)

        if cell_new['value'] != 0:
            cells.insert(0, cell_new)

        return shift(cells, directions, count)


def check_pos(position, cell, cells, width, height, single, direction): 
    # Check if position is out of bounds, or cells contains the position
    if(position['x'] < 0 or position['x'] > width):
        return None
    
    if(position['y'] < 0 or position['y'] > height):
        return None

    for i in range(len(cells)):
        if (position == cells[i]['position']):
            if not single:
                cell_found = cells.pop(i)
                cell['direction'] = direction
                return cell_found
                
        
    return None

def copy(list):
    list_copy = []
    for el in list:
        list_copy.append(el.copy())
    return list_copy

cells = sort(lvl)
results = get_zero_combinations(cells)

for signs in results:
    count = 0
    directions = []
    cells_copy = copy(cells)
    for i in range(len(signs)):
        cells_copy[i]['sign'] = signs[i]
    
    shift(cells_copy, directions, count)

    # print(cells_copy)
    # print(directions)c

    if len(cells_copy) <= 1 and len(directions) > 0:
        for direction in directions:
            print(direction)
        break
    else:
        directions = []


