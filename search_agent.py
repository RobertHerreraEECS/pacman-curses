import heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class searchAgent:
    def __init__(self, graph, nodes,costs, node, goal, type):
        self.nodes = nodes
        self.node = node
        self.goal = goal
        self.graph = graph
        self.nodes = nodes
        self.type = type
        self.costs = costs


    def cost(self, a,b):
        return self.costs[self.nodes[a]] + self.costs[self.nodes[b]]


    def heuristic(self,a,b,type):
        heuristic_type = {
            'manhattan' : self.manhattan_distance(a,b),
            'diagnol' : self.diagnol_distance(a,b),
            'simple' : self.simple_distance(a,b)
        }
        return heuristic_type[type]


    def manhattan_distance(self,a,b):
        (x1, y1) = a
        (x2, y2) = b
        return (self.cost(a,b) * (abs(x2 - x1) + abs(y1-y2)))

    def diagnol_distance(self,a,b):
        (x1, y1) = a
        (x2, y2) = b
        return (abs(x1+x2))**2 + (abs(y1+y2))**2

    def simple_distance(self,a,b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star(self):
        frontier = PriorityQueue()
        frontier.put(self.node, 0)
        came_from = {}
        cost_so_far = {}
        came_from[self.node] = None
        cost_so_far[self.node] = 0
        while not frontier.empty():
            current = frontier.get()
            if current == self.goal:
                break
            neighbors  = self.graph[current]
            for neighbor in neighbors:
                new_cost = cost_so_far[current] + self.cost(current,neighbor)
                if neighbor not in cost_so_far or new_cost  < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor,self.goal,self.type)
                    frontier.put(neighbor,priority)
                    came_from[neighbor] = current

        return came_from, cost_so_far

    #newmethod for PACMAN AI
    def dijktra_search(self):
        frontier = PriorityQueue()
        frontier.put(self.node,0)
        came_from = {}
        cost_so_far = {}
        came_from[self.node] = None
        cost_so_far[self.node] = 0
        while not frontier.empty():
            current = frontier.get()
            if current == self.goal:
                break
            neighbors = self.graph[current]
            for neighbor in neighbors:
                new_cost = cost_so_far[current] + self.cost(current,neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    frontier.put(neighbor,priority)
                    came_from[neighbor] = current
