import copy
import math
import queue

from DirectedGraph.exceptions import GraphException


class DirectedGraph:
    def __init__(self, n):
        self.__din = {}
        self.__dout = {}
        self.__dcost = {}

        for i in range(n):
            self.__din[i] = []
            self.__dout[i] = []

        self.__parent=[]

    def iterate_vertices(self):
        """
        Returns a list of all the vertices in the graph.
        :param
        """
        return list(self.__din.keys())

    def get_no_vertices(self):
        """
        Returns an integer that represents the number of vertices
        :param
        """
        return len(self.__din.keys())

    def get_no_edges(self):
        """
        Returns an integer that represents the number of edges.
        :param
        """
        return len(self.__dcost.keys())

    def exists_edge(self, vertex1, vertex2):
        """
        Returns True if the edge exists and False if it does not.
        :param vertex1:int
        :param vertex2:int
        """
        try:
            return vertex2 in self.__dout[vertex1]
        except KeyError:
            raise GraphException("This edge doesn't exist")

    def get_degree_in(self, vertex):
        """
        Return an integer that represents the in degree of a specified vertex.
        Raises exception if the vertex doesn’t exist.
        :param vertex: int
        """
        try:
            return len(self.__din[vertex])
        except KeyError:
            raise GraphException("Vertex doesn't exist")

    def get_degree_out(self, vertex):
        """
        Return an integer that represents the out degree of a specified vertex.
        Raises exception if the vertex doesn’t exist.
        :param vertex: int
        """
        try:
            return len(self.__dout[vertex])
        except KeyError:
            raise GraphException("Vertex doesn't exist")

    def iterate_outbound(self, vertex):
        """
        Returns a list of all the outbound neighbors of a specified vertex.
        Raises exception if the vertex doesn’t exist.
        :param vertex: int
        """
        try:
            return list(self.__dout[vertex])
        except KeyError:
            raise GraphException("This vertex doesn't have any outbound edges")

    def iterate_inbound(self, vertex):
        """
        Returns a list of all the inbound neighbors of a specified vertex.
        Raises exception if the vertex doesn’t exist.
        :param vertex: int
        """
        try:
            return list(self.__din[vertex])
        except KeyError:
            raise GraphException("This vertex doesn't have any inbound edges")

    def iterate_edges(self):
        """
        Returns a list of all the edges in the graph.Raises exception if the
        graph doesn’t have any edges.
        :param
        """
        try:
            return list(self.__dcost.keys())
        except KeyError:
            raise GraphException("The graph doesn't have edges")

    def modify_cost(self, vertex1, vertex2, new_cost):
        """
        Modifies the cost attached to the edge (vertex1, vertex2). If the
        edge does not exit it raises an exception.
        :param vertex1, vertex2, new_cost: int
        """
        if (vertex1, vertex2) in self.__dcost.keys():
            self.__dcost[(vertex1, vertex2)] = new_cost
        else:
            raise GraphException("This edge doesn't exist")

    def add_edge(self, vertex1, vertex2, cost):
        """
        Adds the edge (vertex1, vertex2) to the graph with the given cost.
        Raises an exception if this edge already exists.
        :param vertex1, vertex2, new_cost: int
        """
        if (vertex1, vertex2) in self.__dcost.keys():
            raise GraphException("This edge already exists")
        else:
            self.__dout[vertex1].append(vertex2)
            self.__din[vertex2].append(vertex1)
            self.__dcost[(vertex1, vertex2)] = cost

    def add_vertex(self, vertex):
        """
        Adds a new vertex to the graph. Raises an exception if this vertex
        already exists.
        :param vertex: int
        """
        if vertex in self.iterate_vertices():
            raise GraphException("This vertex already exists")
        else:
            self.__din[vertex] = []
            self.__dout[vertex] = []

    def remove_edge(self, vertex1, vertex2):
        """
        Removes the edge (vertex1, vertex2) from the graph. If this edge
        doesn’t exist then it raises an exception
        :param vertex1, vertex2 : int
        """
        if (vertex1, vertex2) not in self.__dcost.keys():
            raise GraphException("This edge doesn't exist")
        else:
            self.__dcost.pop((vertex1, vertex2))
            self.__dout[vertex1].remove(vertex2)
            self.__din[vertex2].remove(vertex1)

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph. If this vertex doesn’t exist then
        it raises an exception.
        :param vertex: int
        """
        if vertex not in self.iterate_vertices():
            raise GraphException("Vertex doesn't exist")
        for item in self.__dout[vertex]:
            self.__din[item].remove(vertex)
            del self.__dcost[(vertex, item)]
        for item in self.__din[vertex]:
            self.__dout[item].remove(vertex)
            del self.__dcost[(item, vertex)]
        del self.__din[vertex]
        del self.__dout[vertex]

    def __str__(self):
        graph_str = ""
        for key in self.__dcost:
            graph_str += "Vertex1: "
            graph_str += str(key[0])
            graph_str += " Vertex2: "
            graph_str += str(key[1])
            graph_str += " The cost: "
            graph_str += str(self.__dcost[key])
            graph_str += '\n'
        return graph_str


    def return_cost(self, vertex1, vertex2):
        """
        Returns an integer that represents the cost attached to the edge 		(vertex1, vertex2).
        Raises exception if this edge does not exist.
        :param vertex1, vertex2: int
        """
        if (vertex1, vertex2) in self.__dcost.keys():
            return self.__dcost[vertex1, vertex2]
        raise GraphException("This edge does not exist.")

    def copy_graph(self):
        """
        Returns a copy of the graph.
        :param
        """
        graph_copy = DirectedGraph(self.get_no_vertices())
        graph_copy.__din = copy.deepcopy(self.__din)
        graph_copy.__dout = copy.deepcopy(self.__dout)
        graph_copy.__dcost = copy.deepcopy(self.__dcost)
        return graph_copy

    def BFS(self,s,t):
        visited= {}
        for i in range(len(self.iterate_vertices())):
            visited[i]=0
        q=queue.Queue()
        prev={}
        for i in range(self.get_no_vertices()):
            prev[i]=None
        dist={}
        for i in range(self.get_no_vertices()):
            dist[i]=0
        q.put(s)
        visited[s]=1
        dist[s]=0
        found=False
        while not q.empty() and not found:
            x=q.get()
            for i in range(self.get_degree_out(x)):
                y=self.__dout[x][i]
                if visited[y]==0:
                    prev[y]=x
                    dist[y]=dist[x]+1
                    q.put(y)
                    visited[y]=1
                    if y==t:
                        found=True
        return dist[t],prev

    #LAB3


    def get_weight_matrix(self):
        matrix=[["inf" for i in range(self.get_no_vertices())] for j in range(self.get_no_vertices())]
        for i in range(self.get_no_vertices()):
            for j in range(self.get_no_vertices()):
                if(i==j):
                    matrix[i][j]=0
                elif(self.exists_edge(i,j)):
                    matrix[i][j]=self.__dcost[(i,j)]
                else:
                    matrix[i][j]=math.inf
        return matrix

    def matrix_multiplication(self,M1,M2):
        matrix=M1[:]
        for i in range(self.get_no_vertices()):
            for j in range(self.get_no_vertices()):
                for k in range(self.get_no_vertices()):
                    if (matrix[i][j] > matrix[i][k] + M2[k][j]):
                        matrix[i][j]=min(matrix[i][j],matrix[i][k]+M2[k][j])
                        self.next[i][j] = copy.deepcopy(self.next[i][k])
        return matrix

    def lowest_cost_walk(self,vertex1,vertex2):
        weight_matrix=self.get_weight_matrix()
        all_multiplications=[]
        self._next()
        all_multiplications.append(copy.deepcopy(weight_matrix))
        for i in range(1,self.get_no_vertices()-1):
            all_multiplications.append(copy.deepcopy(self.matrix_multiplication(all_multiplications[i-1],weight_matrix)))
            
        self.validate_negative_costs(all_multiplications[-1])
        """
        for i in range(len(weight_matrix)):
            print(weight_matrix[i])
            print()
        for i in range(len(all_multiplications)):
            for j in range(len(all_multiplications[i])):
                print(all_multiplications[i][j])

            print()
        """
        cost=all_multiplications[-1][vertex1][vertex2]
        path = self.get_path(vertex1,vertex2)

        return cost,path

    def _next(self):
        self.next = [[None for i in range(self.get_no_vertices())] for j in range(self.get_no_vertices())]
        for i in range(self.get_no_vertices()):
            for j in range(self.get_no_vertices()):
                if self.exists_edge(i, j):
                    self.next[i][j] = copy.deepcopy(j)
                elif i == j:
                    self.next[i][j] = copy.deepcopy(j)

    def get_path(self,v1,v2):
        if self.next[v1][v2]==None:
            return []
        path = [v1]
        while v1!=v2:
            v1 = self.next[v1][v2]
            path.append(copy.deepcopy(v1))
        return path

    def validate_negative_costs(self,matrix):
        for i in range(self.get_no_vertices()):
            for j in range(self.get_no_vertices()):
                if matrix[i][j]+matrix[j][i]<0:
                    raise GraphException("It has negative cost cycles!")

    ###################################################LAB4####################################################

    """4. Write a program that, given a graph with costs, does the following:

        verify if the corresponding graph is a DAG and performs a topological sorting of the activities using the 
        algorithm based on predecessor counters;
        if it is a DAG, finds a highest cost path between two given vertices, in O(m+n)."""

    def topological_sorting(self):
        sorted = []
        q=queue.Queue()
        count = {}
        for vertex in self.iterate_vertices():
            count[vertex] = self.get_degree_in(vertex)
            #we put the vertices with 0 inbound neighbours in the queue
            if(count[vertex]==0):
                q.put(vertex)
        while not q.empty():
            vertex = q.get()
            sorted.append(vertex)
            #for every neighbour of vertex we decrease the count(the edges) when the count is 0 then we add it in the queue
            for neighbour in self.iterate_outbound(vertex):
                count[neighbour]-=1
                if(count[neighbour]==0):
                    q.put(neighbour)

        #it the length of the list is < than the number of vertices then the graph is not a dag
        if len(sorted) < self.get_no_vertices():
            sorted = None

        return sorted


    def highest_cost_path(self,vertex1):
        sorted = self.topological_sorting()
        dist={}
        previous = {}
        ok=False
        #for every vertex in sorted
        for y in sorted:
            if ok:
                for x in self.__din[y]:
                    #if y is not already in the distance dictory or if the new cost of dist[x] and the cost of the edge is greated than dist[y]
                    if y not in dist or dist[x]+self.__dcost[(x,y)]>dist[y]:
                        #we change the distance
                        #we change the previous of y
                        dist[y]=dist[x] +self.__dcost[(x,y)]
                        previous[y]=x
            #if we didn't get yet to the starting vertex the distance will be infinite
            else:
                dist[y] = "inf"
                previous[y]=-1
            if y == vertex1:
                dist[y]=0
                previous[y]=-1
                ok=True

        return dist,previous

    def construct_path(self,path,s,t,prev):
        if prev[t] != prev[s]:
            self.construct_path(path, s, prev[t], prev)
            path.append(t)