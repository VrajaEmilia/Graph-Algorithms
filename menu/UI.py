from random import sample, choice

from DirectedGraph.directedGraph import DirectedGraph
from DirectedGraph.exceptions import GraphException


class Ui:
    def __init__(self):
        self._commands = {"1": self.load_from_file,
                          "2": self.write_to_file,
                          "3": self.print_graph_to_console,
                          "4": self.get_number_of_vertices,
                          "5": self.get_vertices,
                          "6": self.is_edge,
                          "7": self.get_in_degree,
                          "8": self.get_out_degree,
                          "9": self.return_outbound_list,
                          "10": self.return_inbound_list,
                          "11": self.add_edge,
                          "12": self.remove_edge,
                          "13": self.add_vertex,
                          "14": self.remove_vertex,
                          "15": self.modify_cost,
                          "16": self.copy_graph,
                          "17": self.create_random_graph,
                          "18": self.print_bfs,
                          "19": self.matrix_multiplication,
                          "20": self.dag
                          }

    @staticmethod
    def print_menu():
        print("1-Load graph from file")
        print("2-Print graph to file")
        print("3-Print graph to console")
        print("4-Get number of vertices")
        print("5-Get the list of vertices")
        print("6-Check if an edge exists or not")
        print("7-Get the in degree of a vertex")
        print("8-Get the out degree of a vertex")
        print("9-Get outbound edges of a vertex")
        print("10-Get inbound edges of a vertex")
        print("11-Add edge")
        print("12-Remove edge")
        print("13-Add vertex")
        print("14-Remove vertex")
        print("15-Modify cost of an edge")
        print("16-Copy graph to a file")
        print("17-Create a random graph and save it in a file")
        print("18-Print the shortest path from one vertex to another")
        print("19-Print the lowest cost path from one vertex to another")
        print("20-Verify if the graph is a DAG and perform topological sorting")

    def run_menu(self):
        while True:
            self.print_menu()
            option = input(">>")
            if option in self._commands:
               # try:
                try:
                    self._commands[option]()
                except GraphException as ex:
                    print(ex)
                except AttributeError:
                   print("Graph not loaded")

    def load_from_file(self):
        file_name = input(r"Enter the file:")
        try:
            with open(file_name, "r") as file:
                line = file.readline()
                line = line.strip().split()
                vertices, edges = int(line[0]), int(line[1])
                self.__graph = DirectedGraph(vertices)
                for edge in range(edges):
                    line = file.readline()
                    line = line.strip().split()
                    vertex1, vertex2, cost = int(line[0]), int(line[1]), int(line[2])
                    self.__graph.add_edge(vertex1, vertex2, cost)
            print("done loading")
        except IOError:
            raise GraphException("Wrong file name")

    def write_to_file(self):
        file_name = input(r"Enter the file:")
        with open(file_name, "w") as f:
            f.write(str(self.__graph.get_no_vertices()) + ' ' + str(self.__graph.get_no_edges()) + '\n')
            for k in self.__graph.iterate_edges():
                f.write(str(k[0]) + ' ' + str(k[1]) + ' ' + str(self.__graph.return_cost(k[0], k[1])) + '\n')
        print("done printing")

    def random_graph(self):
        pass

    def print_graph_to_console(self):
        print(self.__graph.get_no_vertices(), self.__graph.get_no_edges())
        for k in self.__graph.iterate_edges():
            print(k[0], k[1], self.__graph.return_cost(k[0], k[1]))

    def get_number_of_vertices(self):
        print(self.__graph.get_no_vertices())

    def is_edge(self):
        vertices = input("Enter the edge: ")
        vertices = vertices.split()
        vertex1 = int(vertices[0])
        vertex2 = int(vertices[1])
        print(self.__graph.exists_edge(vertex1, vertex2))

    def get_in_degree(self):
        try:
            vertex = int(input("Enter vertex:"))
            print(self.__graph.get_degree_in(vertex))
        except ValueError:
            print("Vertex should be an integer")

    def get_out_degree(self):
        try:
            vertex = int(input("Enter vertex:"))
            print(self.__graph.get_degree_out(vertex))
        except ValueError:
            print("Vertex should be an integer")

    def return_outbound_list(self):
        try:
            vertex = int(input("Enter vertex:"))
            print(self.__graph.iterate_outbound(vertex))
        except ValueError:
            print("Vertex should be an integer")

    def return_inbound_list(self):
        try:
            vertex = int(input("Enter vertex:"))
            print(self.__graph.iterate_inbound(vertex))
        except ValueError:
            print("Vertex should be an integer")

    def get_vertices(self):
        print(self.__graph.iterate_vertices())

    def add_edge(self):
        edge = input("Enter edge(vertex1, vertex2, cost):")
        edge = edge.split()
        try:
            self.__graph.add_edge(int(edge[0]), int(edge[1]), int(edge[2]))
            print("Edge added")
        except ValueError and IndexError:
            print("Invalid input")

    def remove_edge(self):
        edge = input("Enter edge(vertex1, vertex2):")
        edge = edge.split()
        try:
            self.__graph.remove_edge(int(edge[0]), int(edge[1]))
            print("Edge removed")
        except ValueError and IndexError:
            print("Invalid input")

    def add_vertex(self):
        try:
            vertex = int(input("Enter vertex:"))
            self.__graph.add_vertex(vertex)
            print("Vertex added")
        except ValueError:
            print("Vertex should be an integer")

    def remove_vertex(self):
        try:
            vertex = int(input("Enter vertex:"))
            self.__graph.remove_vertex(vertex)
            print("Vertex removed")
        except ValueError:
            print("Vertex should be an integer")

    def copy_graph(self):
        graph = self.__graph.copy_graph()
        self.write_any_graph_to_file(graph)

    def create_random_graph(self):
        try:
            n = int(input("Enter the number of vertices:"))
            e = int(input("Enter the number of edges:"))
            random_graph = DirectedGraph(n)
            vertices = list(range(n))
            if(e > n*(n-1)):
                raise GraphException("Too many edges")
            costs = sample(range(0, 100), e)
            index = 0
            while index < len(costs):
                try:
                    vertex1 = choice(vertices)
                    vertex2 = choice(vertices)
                    random_graph.add_edge(vertex1, vertex2, costs[index])
                    index+=1
                except GraphException:
                    pass
            self.write_any_graph_to_file(random_graph)
        except ValueError:
            print("The number of vertices and edges should be an integer")

    def write_any_graph_to_file(self, graph):
        try:
            file_name = input(r"Enter the file:")
            with open(file_name, "w") as f:
                f.write(str(graph.get_no_vertices()) + ' ' + str(graph.get_no_edges()) + '\n')
                for k in graph.iterate_edges():
                    f.write(str(k[0]) + ' ' + str(k[1]) + ' ' + str(graph.return_cost(k[0], k[1])) + '\n')
            print("done copying")
        except IOError:
            raise GraphException("Wrong file name")

    def modify_cost(self):
        edge = input("Enter the edge and a new cost(vertex1, vertex2, new cost):")
        edge = edge.split()
        try:
            self.__graph.modify_cost(int(edge[0]), int(edge[1]), int(edge[2]))
            print("Cost modified")
        except ValueError and IndexError:
            print("Invalid input")

    def print_bfs(self):
       vertex1 = int(input("enter first:"))
       vertex2 = int(input("enter second:"))
       dist,prev=self.__graph.BFS(vertex1,vertex2)
       path=[]
       if(dist==0):
           print("There is no path")
       else:
           print("The distance is:",dist)
           current = vertex2
           path.append(current)
           while prev[current]!=None:
               path.append(prev[current])
               current = prev[current]
           path.reverse()
           print(path)

    def matrix_multiplication(self):
        vertex1=int(input("v1:"))
        vertex2=int(input("v2:"))
        cost,path=self.__graph.lowest_cost_walk(vertex1,vertex2)
        print("cost = ",cost)
        print("path = ", path)

    def dag(self):
        sorted = self.__graph.topological_sorting()
        if(sorted==None):
            print("The graph is not a dag")
        else:
            print("The graph is a dag")
            print("Topological sorting: ", sorted)
            vertex1= int(input("vertex1:"))
            vertex2 = int(input("vertex2:"))
            dist,prev = self.__graph.highest_cost_path(vertex1)
            path = [vertex1]
            self.__graph.construct_path(path,vertex1,vertex2,prev)
            if(len(path)==1):
                print("No path")
            else:
                print("The path is:",path)