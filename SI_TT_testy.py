from time import time
import SI_TT_robot

def test(x, y, revisit = False):
	if y>4:
		print("Second variable should be:\n 1 - BFS, 2 - A*, 3 - Greedy, 4 - Random")
		return 0
	n = x
	m = int(n**2/2)
	pla = SI_TT_robot.board(n)
	state = SI_TT_robot.State(n, pla, m)
	node = SI_TT_robot.Node(state)
	print("INITIAL STATE:")
	print(state)
	# print('rooms to clean:', SI_TT_robot.h1(node))
	# nr_of_verticies = 5*(n**2-4*n)+4*(4*n-4)+12+SI_TT_robot.h1(node)
	# average_nr_of_actions = nr_of_verticies / n**2
	if y == 1:
		print('Searching for solution with BFS algorithm, board size =', n)
		t1 = time()
		SI_TT_robot.bfs(node)
		t2 = time()
		print ('time complexity:', SI_TT_robot.problem_time)
		print ('memory complexity:', SI_TT_robot.memory)
		print ('time of computation:', t2-t1)
	elif y == 2:
		print('Searching for solution with A* algorithm, board size =', n)
		t1 = time()
		SI_TT_robot.astar(node, revisit)
		t2 = time()
		print ('time complexity:', SI_TT_robot.problem_time)
		print ('memory complexity:', SI_TT_robot.memory)
		print ('time of computation:', t2-t1)
	elif y == 3:
		print('Searching for solution with Greedy algorithm, board size =', n)
		t1 = time()
		SI_TT_robot.greedy(node, revisit)
		t2 = time()
		print ('time complexity:', SI_TT_robot.problem_time)
		print ('memory complexity:', SI_TT_robot.memory)
		print ('time of computation:', t2-t1, '\n')
	elif y == 4:
		print('Searching for solution with Random algorithm, board size =', n)
		t1 = time()
		SI_TT_robot.random_search(node)
		t2 = time()
		print ('time complexity:', SI_TT_robot.problem_time)
		print ('memory complexity:', SI_TT_robot.memory)
		print ('time of computation:', t2-t1, '\n')

def main():
	n = 3

	# test(n,1)
	test(n,2)
	test(n,3)
	test(n,4)
if __name__ == "__main__": main()