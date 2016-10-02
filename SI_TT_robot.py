import queue
import random


#liczniki
memory = 0
node_count = 0
problem_time = 0

#Linked list, pierwsze trzy funkcje wzięte z http://stackoverflow.com/questions/280243/python-linked-list#280284
cons = lambda el, lst: (el, lst)
car = lambda lst: lst[0] if lst else lst
cdr = lambda lst: lst[1] if lst else lst
def length(lst):
	count = 0
	if not lst:
		return 0
	while 1:
		lst = cdr(lst)
		count += 1
		if not lst:
			break
	return count
def display(lst):
	if not lst:
		return 'the list is empty'
	while 1:
		print(car(lst), end = " ")
		lst = cdr(lst)
		if not lst:
			break
def reversell ( lst ):
	last = None
	current = lst
	while(current is not None):
		nxt = cdr(current)
		last = cons(car(current), last)
		current = nxt
	return last

#KLASY
class State:
	def __init__(self, size, board, position):
		self.board = board
		self.position = position
		self.size = size
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.board == other.board and self.position == other.position
	def __hash__(self):
		return hash(self.__class__) ^ hash(self.board) ^ hash(self.position)
	def __str__(self):
		str_board = list(self.board)
		for x in range(self.size * self.size):
			str_board[x] = str(str_board[x])+' '
			if x == self.position:
				str_board[x] = str_board[x][:-1]
				str_board[x] += 'R'
			if (x+1)%self.size == 0:
				str_board[x] += '\n'
		str_board[0] = ' ' + str_board[0]
		return ' '.join(str_board)

class Node:
	def __init__(self, state, history = cons('Start', None)):
		global memory
		global node_count
		global problem_time
		self.state = state
		self.history = history
		self.prior = 0
		problem_time += 1
		node_count += 1
		memory = max(node_count, memory)
	def __str__(self):
		display(reversell(self.history))
		# return ' -> '.join(self.history)
		return ''
	def __lt__(self, other):
		a = (self.prior, len(self.history))
		b = (other.prior, len(other.history))
		return a < b
	def __del__(self):
		global node_count
		node_count -= 1

#Algorytmy
def bfs(start_node):
	global memory
	global problem_time
	global node_count
	memory, problem_time, node_count = 0,0,0
	q = queue.Queue()
	q.put(start_node)
	counter = 0
	while not q.empty():
		counter += 1
		current = q.get()
		if goal(current):
			print('Loop repetitions:', counter)
			print('Result cost:', length(current.history)-1)
			print('PATH:', current)
			print(current.state)
			return current
		else:
			insert(q, expand(current))
	return 'queue is empty!'
def astar(start_node, revisit = False):
	global memory
	global problem_time
	global node_count
	memory, problem_time, node_count = 0,0,0
	q = queue.PriorityQueue()
	q.put(start_node)
	counter = 0
	visited = set()
	while not q.empty():
		current = q.get()
		if not revisit:
			if current.state in visited:
				continue
			visited.add(current.state)
		counter += 1
		if goal(current):
			print('Loop repetitions:', counter)
			print('Result cost:', length(current.history)-1)
			print('PATH:', current)
			print(current.state)
			return current
		else:
			insert(q, expand(current),visited, he1 = True)
	return 'queue is empty!'
def greedy(start_node, revisit = False):
	global memory
	global problem_time
	global node_count
	memory, problem_time, node_count = 0,0,0
	q = queue.PriorityQueue()
	q.put(start_node)
	counter = 0
	visited = set()
	while not q.empty():
		current = q.get()
		if not revisit:
			if current.state in visited:
				continue
			visited.add(current.state)
		counter += 1
		if goal(current):
			print('Loop repetitions:', counter)
			print('Result cost:', length(current.history)-1)
			print('PATH:', current)
			print(current.state)
			return current
		else:
			insert(q, expand(current), he2 = True)
	return 'queue is empty!'
def random_search(start_node):
	global memory
	global problem_time
	global node_count
	memory, problem_time, node_count = 0,0,0
	q = queue.Queue()
	q.put(start_node)
	counter = 0
	while not q.empty():
		counter += 1
		current = q.get()
		if goal(current):
			print('Loop repetitions:', counter)
			print('Result cost:', length(current.history)-1)
			print('PATH:', current)
			print(current.state)
			return current
		else:
			exp = expand(current)
			rand = random.randint(0, len(exp)-1)
			random.shuffle(exp)
			q.put(exp[rand])
	return 'queue is empty!'

#Funckje pomocnicze algorytmów
def expand(node):
	result = []
	state = node.state
	if state.board[state.position] == 0:
		pass
	else:
		new_board = list(state.board)
		new_board[state.position] = 0
		new_board = tuple(new_board)
		result.append(Node(State(state.size, new_board, state.position), cons('clean', node.history)))

	new_pos = state.position - state.size
	if new_pos > -1:	
		result.append(Node(State(state.size, state.board, new_pos), cons('up', node.history)))

	new_pos = state.position + state.size
	if new_pos < (state.size ** 2):	
		result.append(Node(State(state.size, state.board, new_pos), cons('down', node.history)))

	if state.position % state.size == 0:
		pass
	else:
		new_pos = state.position - 1 	
		result.append(Node(State(state.size, state.board, new_pos), cons('left', node.history)))

	new_pos = state.position + 1
	if new_pos % state.size == 0:
		pass
	else:		
		result.append(Node(State(state.size, state.board, new_pos), cons('right', node.history)))
	
	result.append(Node(state, cons('idle', node.history)))
	return result

def insert(q, list, visit = None, he1 = False, he2 = False):
	# shuffle(list)
	if he1:
		for item in list:
			item.prior =h1(item) + (length(item.history)-1)
			if item.state not in visit:
				q.put(item)
	elif he2:
		for item in list:
			item.prior = h2(item)
			q.put(item)
	else:
		for item in list:
			q.put(item)

def goal(node):
	return sum(node.state.board) == 0

#Heurystyki i ich funkcje pomocnicze
def h1(node):
	return sum(node.state.board)
def h2(node):
	return distance(node.state.position, nearest(node.state), node.state.size)/(2*node.state.size) + h1(node)

def nearest(state):
	positions = [x for x in range(state.size**2) if state.board[x]]
	positions.sort(key=lambda x: distance(state.position, x, state.size))
	return state.position if not positions else positions[0]

def distance(pos1, pos2, size):
	p1 = (int(pos1/size), pos1%size)
	p2 = (int(pos2/size), pos2%size)
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + 1

#Funkjca tworząca początkową tablicę
def board(n):
	board = []
	k = 0
	l = n*n
	while k < l:
		i = int(k/n)
		j = k % n
		board.append(int((i*13+j*23+i*j*19)%37 < 18))
		k += 1
	return tuple(board)



# MAIN
def main():
	print('RUN TESTY.py')

if __name__ == "__main__": main()
