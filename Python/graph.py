import copy
import random

"""
    The graph is represented with two dictionaries, dictIn and dictOut for
    the inbound and outbound edges connected to each vertex.
    The keys of the dictionary are the vertices.

    dictCosts is a dictionary with the keys being edges and the values being
    the costs of the edges.

    Name: Şut George
    Group: 917
"""

class DoubleDictGraph:

    def __init__(self, number_of_nodes):
        self._dictOut = {}
        self._dictIn = {}
        self._dictCosts = {}

        for i in range(number_of_nodes):
            self._dictOut[i] = []
            self._dictIn[i] = []

    """
    def get_dict_out(self):
        return self._dictOut


    def get_dict_in(self):
        return self._dictIn

    """


    def get_vertices(self):
        """
            Returns an iterable containing all the vertices
        """
        return self._dictOut.keys()


    def get_number_of_vertices(self):
        """
            Returns the number of vertices in the graph
        """
        return len(self.get_vertices())


    def get_outbound_neighbours_of_vertex_X(self, x):
        """
            Returns a list containing the outbound neighbours of x
        """
        return self._dictOut[x]


    def get_inbound_neighbours_of_vertex_X(self, x):
        """
            Returns a list containing the inbound neighbours of x
        """
        return self._dictIn[x]


    def is_edge(self, x, y):
        """
            Returns True if there is an edge from x to y, False otherwise
        """
        try:
            return y in self._dictOut[x]
        except KeyError:
            return False


    def add_edge(self, x, y, cost):
        """
            Adds an edge from x to y with the cost "cost".
            Precondition: there is no edge from x to y
        """
        if self.is_edge(x, y):
            print("There is already an edge from {} to {}!\n".format(x, y))
            return

        self._dictOut[x].append(y)
        self._dictIn[y].append(x)
        self._dictCosts[(x, y)] = cost


    def remove_edge(self, x, y):
        """
            Removes the edge from x to y.
            Precondition: there is an edge from x to y.
        """

        if not self.is_edge(x, y):
            print("There is no edge between x and y!")
            return

        for node_index in range(0, len(self._dictOut[x])):
            if self._dictOut[x][node_index] == y:
                del self._dictOut[x][node_index]
                break

        for node_index in range(0, len(self._dictIn[y])):
            if self._dictIn[y][node_index] == x:
                del self._dictIn[y][node_index]
                break

        del self._dictCosts[(x, y)]


    def get_in_and_out_degree(self, vertex_number):
        """
            Returns the in degree and out degree of a vertex in a tuple.
        """
        return (len(self._dictIn[vertex_number]), len(self._dictOut[vertex_number]))


    def get_iterator_for_outbound_edges_of_vertex_x(self, vertex_number):
        """
            Returns an iterator for the outbound edges of vertex "vertex_number".
        """
        return iter(self._dictOut[vertex_number])


    def get_iterator_for_inbound_edges_of_vertex_x(self, vertex_number):
        """
            Returns an iterator for the outbound edges of vertex "vertex_number".
        """
        return iter(self._dictIn[vertex_number])


    def parse_outbound_edges_of_vertex_x(self, vertex_x):
        """
            Returns a list with all the outbound edges starting from the
            vertex x.
        """
        iterator = self.get_iterator_for_outbound_edges_of_vertex_x(vertex_x)
        outbound_edges_endpoints = []

        try:
            while True:
                outbound_edges_endpoints.append(next(iterator))
        except StopIteration:
            pass

        return outbound_edges_endpoints


    def parse_inbound_edges_of_vertex_x(self, vertex_x):
        """
            Returns a list with all the inbound edges startpoints which end
            in the vertex x.
        """
        iterator = self.get_iterator_for_inbound_edges_of_vertex_x(vertex_x)
        inbound_edges_startpoints = []

        try:
            while True:
                inbound_edges_startpoints.append(next(iterator))
        except StopIteration:
            pass

        return inbound_edges_startpoints


    def retrieve_edge_cost(self, vertex_x, vertex_y):
        """
            Returns the cost of an edge.
        """
        return self._dictCosts[(vertex_x, vertex_y)]


    def modify_edge_cost(self, vertex_x, vertex_y, new_cost):
        """
            Modifies the cost of an edge which is stored in the
            dictCosts dictionary of edges.
        """
        self._dictCosts[(vertex_x, vertex_y)] = new_cost


    def add_vertex(self, vertex_x):
        """
            Adds a vertex to the graph.
        """

        if vertex_x in self.get_vertices():
            print("The vertex already exists!\n")
            return

        self._dictOut[vertex_x] = []
        self._dictIn[vertex_x] = []


    def remove_vertex(self, vertex_x):
        """
            Removes a vertex from the graph and all the edges associated
            with it.
        """
        # Removing inbound edges of vertex x from the neighbouring vertices
        for node_index in range(0, len(self._dictIn[vertex_x])):
            for node_index_2 in range(0, len(self._dictOut[self._dictIn[vertex_x][node_index]])):
                if self._dictOut[self._dictIn[vertex_x][node_index]][node_index_2] == vertex_x:
                    removed_edge = (self._dictIn[vertex_x][node_index], vertex_x)
                    del self._dictCosts[removed_edge]
                    del self._dictOut[self._dictIn[vertex_x][node_index]][node_index_2]
                    break

        # Removing outbound edges of vertex x from the neighbouring vertices
        for node_index in range(0, len(self._dictOut[vertex_x])):
            for node_index_2 in range(0, len(self._dictIn[self._dictOut[vertex_x][node_index]])):
                if self._dictIn[self._dictOut[vertex_x][node_index]][node_index_2] == vertex_x:
                    removed_edge = (vertex_x, self._dictOut[vertex_x][node_index])
                    del self._dictCosts[removed_edge]
                    del self._dictIn[self._dictOut[vertex_x][node_index]][node_index_2]
                    break

        del self._dictOut[vertex_x]
        del self._dictIn[vertex_x]


    def copy(self):
        """
            Creates a copy of the graph and returns it.
        """
        copy_of_the_graph = copy.deepcopy(self)
        return copy_of_the_graph


    @staticmethod
    def read_graph_from_text_file(filename):
        """
            A static method which reads from a file a graph,
            creates it and returns it.
        """
        f = open(filename, "r");
        lines = f.readlines();

        number_of_nodes = int(lines[0].split()[0])
        number_of_edges = int(lines[0].split()[1])

        graph = DoubleDictGraph(number_of_nodes)
        index = 0 

        for line_index in range(1, len(lines)):
            split_line = lines[line_index].strip().split()
            first_node = int(split_line[0])
            second_node = int(split_line[1])
            cost = int(split_line[2])
            graph.add_edge(first_node, second_node, cost)

        return graph


    def write_graph_to_text_file(self, file_name):
        """
            A method which writes to a text file the graph on which
            it is applied.
        """
        number_of_nodes = self.get_number_of_vertices()
        number_of_edges = 0

        for node in self.get_vertices():
            number_of_edges += len(self._dictOut[node]) 

        f = open(file_name, "w")

        f.write(str(number_of_nodes))
        f.write(" ")
        f.write(str(number_of_edges))
        f.write("\n")

        for node in range(0, self.get_number_of_vertices()):
            for neighbour_of_node in self._dictOut[node]:
                f.write(str(node))
                f.write(" ")
                f.write(str(neighbour_of_node))
                f.write(" ")
                f.write(str(self._dictCosts[(node, neighbour_of_node)]))
                f.write("\n")
        


    @staticmethod
    def create_random_graph(number_of_vertices, number_of_edges):
        """
            Creates a random graph with a certain number of vertices and
            edges and returns it
        """

        graph = DoubleDictGraph(number_of_vertices) 
        
        for edge in range(0, number_of_edges):
            first_node = random.randrange(0, number_of_vertices)
            second_node = random.randrange(0, number_of_vertices)  

            while graph.is_edge(first_node, second_node):       
                first_node = random.randrange(0, number_of_vertices)
                second_node = random.randrange(0, number_of_vertices)  
            
            cost = random.randrange(-3, 9)
            graph.add_edge(first_node, second_node, cost)


        return graph
