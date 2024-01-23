def grouper(lst, taille):  # taille = taille maximale des groupes
    groupes = []
    accum = []
    for elem in lst:
        accum.append(elem)
        if len(accum) == taille:
            groupes.append(accum)
            accum = []
    if len(accum) > 0:
        groupes.append(accum)
    return groupes


def table(contenu): return '<div id = "jeu"><table>' + contenu + '</table><div/>'


def tr(contenu): return '<tr>' + contenu + '</tr>'


def td(contenu): return '<td onclick="clic()">' + contenu + '</td>'  # Need to modify


def trJoin(lst): return tr(''.join(lst))  # <tr> contenu de lst </tr>


def tableJoin(lst): return table(''.join(lst))  # <table> Contenu </table>


def listeToTable(lst, taille):
    return tableJoin(list(map(trJoin, grouper(list(map(td, lst)), taille))))


def getindex(string):
    index = [string.find(' onclick')];
    j = 0
    for i in range(len(string)):
        temp = string.find(' onclick', i)
        if index[j] == temp:
            next
        else:
            index.append(temp)
            j += 1
    return index


def add_grid_value(string):  # This works !!
    index = getindex(string)
    temp = string[:index[0]] + ' id ="case' + str(0) + '"'
    temp += string[index[0]:index[0] + 15] + str(0)
    for i in range(1, 36, 1):
        temp += string[index[i - 1] + 15:index[i]] + ' id ="case' + str(i) + '"'
        temp += string[index[i]:index[i] + 15] + str(i)
    # add 13 char every time
    return temp


def symbol_values():  # Returns vector of different symbol values, no doubles
    symbol_values = [0] * 5;
    k = 0
    while k != 5:
        condition = True
        temp = round(random() * 20)
        for i in range(5):
            if temp == symbol_values[i] or temp == 0:
                condition = False
                break
        if condition:
            symbol_values[k] = temp
            k += 1
    return symbol_values


def initial_matrix(symbol_values, nrow):  # base matrix of values

    initial_matrix = [None] * 5
    for i in range(nrow):
        initial_matrix[i] = [0] * 5

    condition = True
    while condition:
        condition = False
        validate = [0] * 5
        for i in range(nrow):
            for j in range(5):
                index = round(random() * 4)
                initial_matrix[i][j] = symbol_values[index]
                validate[index] = 1

        ## VALIDATION THAT ALL SYMBOLS ARE THERE
        for i in range(5):
            if validate[i] == 0:
                condition = True

    return initial_matrix


def sum_row(matrix):  # These add the sum value to the matrix
    matrix_row = matrix
    sum_row = 0
    for i in range(len(matrix)):
        for j in range(5):
            sum_row += matrix[i][j]
        matrix_row[i].append(sum_row)
        sum_row = 0
    return matrix_row


def sum_col(matrix):  # These add the sum value to the matrix
    matrix_col = matrix
    sum_col = [0] * 5
    for i in range(5):
        for j in range(5):
            sum_col[i] += matrix[j][i]
    matrix = matrix + [sum_col]
    return matrix


# Create the starting game matrix
def initialize(nrow, symbol):
    matrix_0 = initial_matrix(symbol, 5)
    matrix_agg_row = sum_row(matrix_0)
    matrix_agg_col = sum_col(matrix_agg_row)

    return matrix_agg_col


def convert_symbols(matrix, symbol):  # for testing
    symbol_matrix = matrix.copy()
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == symbol[0]:
                # symbol_matrix[i][j] = 'A'
                symbol_matrix[i][j] = '''<img src="symboles/circle.svg">'''
            if matrix[i][j] == symbol[1]:
                # symbol_matrix[i][j] = 'B'
                symbol_matrix[i][j] = '''<img src="symboles/pyramide.svg">'''
            if matrix[i][j] == symbol[2]:
                # symbol_matrix[i][j] = 'C'
                symbol_matrix[i][j] = '''<img src="symboles/penta.svg">'''
            if matrix[i][j] == symbol[3]:
                # symbol_matrix[i][j] = 'D'
                symbol_matrix[i][j] = '''<img src="symboles/star.svg">'''
            if matrix[i][j] == symbol[4]:
                # symbol_matrix[i][j] = 'E'
                symbol_matrix[i][j] = '''<img src="symboles/cube.svg">'''
    return symbol_matrix


def game_setup(test):
    string = []
    for i in range(5):
        for j in range(5):
            string.append(test[i][j])
        string.append(str(test[i][-1]))
    for k in range(5):
        string.append(str(test[-1][k]))
    return string


def clic(index):  #### ----> modify
    global data
    global count
    state = None
    symbol = data[index]
    if count < 5:
        value = input('Value for symbol')  # change for a html input
    else:
        alert("Game Will Reload"); init()
    if count < 5 and value == '' or int(value) > 20:
        alert("Invalid Choice")
        init()
        return  # Terminate Function --

    for i in range(len(data)):
        if symbol == data[i]:
            data[i] = '''<div class="jeu">''' + data[i] + '''
						<div class="centered"> ''' + value + '''</div>
						</div>'''
            # Modify sums
            data[i // 6 + (i // 6 + 1) * 5] = str(int(data[i // 6 + (i // 6 + 1) * 5]) - int(value))
            # if int(data[i//6+(i//6+1)*5]) < 0 : state = False
            data[i % 6 - 5] = str(int(data[i % 6 - 5]) - int(value))
        # if int(data[i%5-5]) < 0 : state = False

    main = document.querySelector("#main")
    display = add_grid_value(listeToTable(data, 6))
    game_state = """
				<button onclick='init()'>Click to Reload</button><br>
				<style>
      			p { color: red; font-size: 34px;}
      			</style>
      			<p>&nbsp;&nbsp;Jouer!</p> 
      			"""

    count += 1
    if count == 5:  # Validation at end of game ------------
        for i in range(5):
            if int(data[6 * (i + 1) - 1]) == 0 and int(data[-(i + 1)]) == 0:
                state = True
            else:
                state = False

        if state:
            game_state = """
      			<button onclick='init()'>Click to Reload</button><br>
      			<style>
      				p { color: red; font-size: 34px;}
      			</style>
      			<p>&nbsp;&nbsp;WIN</p> 
      			"""

    if state == False:
        game_state = """
      			<button onclick='init()'>Click to Reload</button><br>
      			<style>
      				p { color: red; font-size: 34px;}
      			</style>
      			<p>&nbsp;&nbsp;LOSE</p> 

      			"""

    base = game_state + """
      		<style>
        		#jeu table { float: none; }
        		#jeu table td {
            	border: 1px solid black; 
            	padding: 1px 2px;
            	width: 80px;
            	height: 80px;
            	font-family: Helvetica; 
            	font-size: 20px; 
            	text-align: center;
        	}
        	#jeu table td img {
            	position: relative;
            	display: block;
            	margin-left: auto;
            	margin-right: auto;
            	object-fit: contain;
            	width: 80%;
            	height: 80%;

        	.centered {
        		position: absolute;
        		top:50%;
        		left:50%;
        		translate(-50%, -50%);
        	}
      		</style>

      		"""
    main.innerHTML = base + display


def element(id):
    return document.querySelector('#' + id)


def grid(index):
    return element('case' + str(index))


def init():
    global data
    global count
    count = 0
    symbol = symbol_values()
    print(symbol)  # for testing only
    base_values = initialize(5, symbol)
    convert_symbols(base_values, symbol)

    data = game_setup(base_values)
    main = document.querySelector("#main")

    display = add_grid_value(listeToTable(data, 6))  # We now have positionnal values
    base = """
      		<button onclick='init()'>Click to Reload</button><br>
      		<style>
      			p { color: red; font-size: 34px;}
      		</style>
      		<p>&nbsp;&nbsp;Jouer!</p>
      		<style>
        		#jeu table { float: none; }
        		#jeu table td {
            	border: 1px solid black; 
            	padding: 1px 2px;
            	width: 80px;
            	height: 80px;
            	font-family: Helvetica; 
            	font-size: 20px; 
            	text-align: center;
        	}
        	#jeu table td img {
            	position: relative;
            	display: block;
            	margin-left: auto;
            	margin-right: auto;
            	object-fit: contain;
            	width: 80%;
            	height: 80%;

        	}
        	.centered {
        		position: absolute;
        		top:50%;
        		left:50%;
        		translate(-50%, -50%);
        		text-align: center;
        	}
      		</style>

      		"""
    # while
    main.innerHTML = base + display

# for i in range(test_2):
#	main.innerHTML = listeToTable(game_setup(), 6)
#	sleep(0.01)













