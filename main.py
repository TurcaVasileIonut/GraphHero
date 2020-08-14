import os
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import tkinter.filedialog
import networkx as nx
import matplotlib.pyplot as plt
import algorithms

matplotlib.use('TkAgg')


class GraphEditor:
    def __init__(self):

        # create a GUI
        self.window = Tk()
        # set his size
        self.window.geometry("600x700+400+10")
        # set his title
        self.window.title("Graph Editor")
        # set his icon
        self.window.wm_iconbitmap('Graph_Hero_Icon.ico')
        # set his background color
        self.window.configure(bg='#424242')
        # disable width changing
        self.window.resizable(False, True)

        # initialize the graph
        self.G = nx.Graph()

        # initialize the tree
        # this will be used to display the partial tree of minimum cost
        self.Tree = nx.Graph()

        # this is the button that will draw the graph
        # if a graph is introduced in the text box, the program will read it and display
        # else a standard graph will be displayed
        self.draw_button = Button(self.window, text="Draw", font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                  activebackground='#FFFFFF', bg='#716C6A',
                                  activeforeground='darkblue', command=self.draw_button_function).place(x=0, y=0)

        # this button will make the graph oriented
        self.directed_button = Button(self.window, text="Directed", font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                      activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                      command=self.directed).place(x=39, y=0)

        # this button will make the graph unoriented
        self.undirected_button = Button(self.window, text="Undirected", font=('consolas', 10, 'bold'),
                                        foreground='#FFFFFF', activebackground='#FFFFFF', activeforeground='darkblue',
                                        bg='#716C6A', command=self.undirected).place(x=106, y=0)

        # this button will make the graph weighted
        self.weighted_button = Button(self.window, text="Weighted", font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                      activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                      command=self.weighted).place(x=187, y=0)

        # this button will make the graph unweighted
        self.unweighted_button = Button(self.window, text="Unweighted", font=('consolas', 10, 'bold'),
                                        foreground='#FFFFFF',
                                        activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                        command=self.unweighted).place(x=254, y=0)

        # this button will display the minimum cost partial tree
        # the tree will be displayed in a new window
        self.minimum_cost_partial_tree_button = Button(self.window, text="Partial tree",
                                                       font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                                       activebackground='#FFFFFF', activeforeground='darkblue',
                                                       bg='#716C6A',
                                                       command=self.minimum_cost_partial_tree).place(x=335, y=0)

        # this will delete the plotted graph and the contents of the lower text boxes
        self.clear_button = Button(self.window, text="Clear", font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                   activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                   command=self.clear).place(x=430, y=0)

        # this will close the program
        self.close_button = Button(self.window, text="Close", font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                   activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                   command=quit).place(x=476, y=0)

        # this will save the plotted tree with a unused name
        self.save_image_button = Button(self.window, text="Save image", font=('consolas', 10, 'bold'),
                                        foreground='#FFFFFF', activebackground='#FFFFFF', activeforeground='darkblue',
                                        bg='#716C6A', command=self.save_image).place(x=0, y=500)

        # this will save the list of edges of the plotted graph
        self.save_the_graph_button = Button(self.window, text="Save the graph", font=('consolas', 10, 'bold'),
                                            foreground='#FFFFFF',
                                            activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                            command=self.save_the_graph).place(x=82, y=500)

        # this will open and plot an older graph or a list of edges
        self.open_a_graph_button = Button(self.window, text="Open a graph", font=('consolas', 10, 'bold'),
                                          foreground='#FFFFFF',
                                          activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                          command=self.open_an_older_graph).place(x=192, y=500)

        # in this text box will appear if the graph is eulerian (has an eulerian cycle)
        # or if it is not
        self.euler_text = Text(self.window, width=800, height=1.2, font=('consolas', 10, 'bold'), bg='#424242',
                               foreground='#FFFFFF')
        self.euler_text.place(x=0, y=550)

        # in this text box will appear the number of connected components if the graph is undirected
        # or the number of strong connected components if the graph is directed
        self.components = Text(self.window, width=800, height=1.2, font=('consolas', 10, 'bold'), bg='#424242',
                               foreground='#FFFFFF')
        self.components.place(x=0, y=575)

        # here the user will introduce the first selected node
        self.dijkstra1 = Text(self.window, width=5, height=1.2, font=('consolas', 10, 'bold'), bg='#424242',
                              foreground='#FFFFFF')
        # here the user will introduce the second selected node
        self.dijkstra2 = Text(self.window, width=5, height=1.2, font=('consolas', 10, 'bold'), bg='#424242',
                              foreground='#FFFFFF')
        # here the optimum meeting point between selected nodes  will appear
        self.dijkstra_answer = Text(self.window, width=800, height=1.2, font=('consolas', 10, 'bold'), bg='#424242',
                                    foreground='#FFFFFF')
        # here the distance from the first node to second and the distance
        # from second node to first will appear;
        # if the graph is directed, there will be displayed 2 different distances
        self.dijkstra_answer2 = Text(self.window, width=800, height=1.2, font=('consolas', 10, 'bold'), bg='#424242',
                                     foreground='#FFFFFF')
        self.dijkstra1.place(x=320, y=600)
        self.dijkstra2.place(x=365, y=600)
        self.dijkstra_answer.place(x=0, y=625)
        self.dijkstra_answer2.place(x=0, y=650)
        self.dijkstra_answer.configure(state='disabled')  # this box is read only for user
        self.dijkstra_answer2.configure(state='disabled')  # this box is read only for the user
        # this button will start the meeting point and distances finding
        self.dijkstra_button = Button(self.window, text="Distance between and optimal meeting point",
                                      font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                      activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                      command=self.dijkstra_function).place(x=0, y=597)

        # if something is read, that will be displayed when the buttons are pressed
        # else will be displayed a standard graph
        self.something_is_read = False

        # initially the graph is unweighted and undirected
        # if a specific button is pressed, this variable will store the new type of graph
        self.is_weighted = False
        self.is_directed = False

        # this is if the specific error for introducing strings as weights need to be displayed
        self.cant_be_string = False

        # this is if is introduced an uppercase
        self.cant_be_uppercase = False

        # here are initialized the parts where the graph is plotted
        self.figure = plt.figure(figsize=(3, 4.5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        self.a = self.figure.add_subplot(111)

        # in self.edges and self.weighted_edges are memorized the edges of the graph
        # at the start of the program, standards graphs are memorized
        self.edges_tree = list()
        self.edges = [(str(5), str(4))]
        self.weighted_edges = [(str(5), str(4), str(2))]
        for node1 in range(1, 4):
            for node2 in range(node1 + 1, 6):
                self.edges.append((str(node1), str(node2)))
                self.weighted_edges.append((str(node1), str(node2), int(4)))

        # create a Frame for the Text and Scrollbar
        txt_frm = Frame(self.window, width=200, height=450)
        txt_frm.place(x=0, y=40)

        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)

        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

        # create a Text widget
        self.txt = Text(txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # add the components of the graph to the text box
        # this will help users to understand how to use the editor
        # this command will plot the graph
        # this is for how to use reasons
        self.draw_the_network()

        # create a Scrollbar and associate it with txt
        scrollb = Scrollbar(txt_frm, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

        self.window.mainloop()

    # in this function will be an older graph will be chosen to be plotted
    def open_an_older_graph(self):
        # this is the supported types
        ftypes = [('Text Document', "*.txt")]
        # this will open the window
        dlg = tkinter.filedialog.Open(filetypes=ftypes)
        # this will take the name of the chosen file
        fl = dlg.show()

        if fl != '':
            # when is opened an older graph is like a graph is introduced in the text box
            self.something_is_read = True
            # this opens and read the txt file
            f = open(fl, "r")
            text = f.read()
            # this ends the process (now the graph is in the program)
            self.txt.delete(1.0, END)
            self.txt.insert(END, text)
            self.draw_button_function()

    # this function will save the image of plotted graph
    def save_image(self):
        # this is for being sure that the graph from the text box is plotted and saved
        self.draw()
        # in the path will be the name of saved file
        path = str("Graph_")
        if self.is_weighted:
            path = path + "W_"
        else:
            path = path + "U_"

        if self.is_directed:
            path = path + "D_"
        else:
            path = path + "U_"

        # this is for chosing a file name that is not in the directory
        for i in range(0, 999999999999999999999999999999999999999999999):
            number = str(i)
            filename = path + number + ".png"
            if not os.path.isfile(filename):
                plt.savefig(filename)
                break

    # this will save the list of edges of the plotted graph
    def save_the_graph(self):
        # this is for chosing the name of the saved file
        path = str("Graph_")
        if self.is_weighted:
            path = path + "W_"
        else:
            path = path + "U_"

        if self.is_directed:
            path = path + "D_"
        else:
            path = path + "U_"

        # this is for finding a name that is not in the directory
        for i in range(0, 999999999999999999999999999999999999999999999):
            number = str(i)
            filename = path + number + ".txt"
            if not os.path.isfile(filename):
                with open(path + number + ".txt", 'w') as f:
                    if self.is_weighted:
                        for edge in self.weighted_edges:
                            f.write(edge[0])
                            f.write(" ")
                            f.write(edge[1])
                            f.write(" ")
                            f.write(str(edge[2]))
                            f.write("\n")
                    else:
                        for edge in self.edges:
                            f.write(edge[0])
                            f.write(" ")
                            f.write(edge[1])
                            f.write("\n")
                break

    # this will save the plot of the partial tree of minimum cost
    def save_tree_image(self):
        # in path will be the name of the saved tree image
        path = str("Tree_")
        if self.is_weighted:
            path = path + "W_"
        else:
            path = path + "U_"

        if self.is_directed:
            path = path + "D_"
        else:
            path = path + "U_"

        # this if for finding a name that is not in the directory
        for i in range(0, 999999999999999999999999999999999999999999999):
            number = str(i)
            filename = path + number + ".png"
            if not os.path.isfile(filename):
                plt.savefig(filename)
                break

    # this will save the list of edges of the partial tree of minimum cost
    def save_the_tree(self):
        # in path will be the name of the saved list of tree edges
        path = str("Tree_")
        if self.is_weighted:
            path = path + "W_"
        else:
            path = path + "U_"

        if self.is_directed:
            path = path + "D_"
        else:
            path = path + "U_"

        # this is for finding a name that is not in the directory
        for i in range(0, 999999999999999999999999999999999999999999999):
            number = str(i)
            filename = path + number + ".png"
            if not os.path.isfile(filename):
                with open(path + number + ".txt", 'w') as f:
                    if self.is_weighted:
                        for edge in self.edges_tree:
                            f.write(edge[0])
                            f.write(" ")
                            f.write(edge[1])
                            f.write(" ")
                            f.write(str(edge[2]))
                            f.write("\n")
                    else:
                        for edge in self.edges_tree:
                            f.write(edge[0])
                            f.write(" ")
                            f.write(edge[1])
                            f.write("\n")
                break

    # this will find and plot the minimum cost partial tree
    def minimum_cost_partial_tree(self):
        # a new window where the tree is plotted is created here
        root = Tk()
        root.geometry("300x450+400+50")
        root.title("Graph Editor")
        root.wm_iconbitmap('Graph_Hero_Icon.ico')
        root.configure(bg='#424242')

        if self.is_directed:
            # if the graph is directed, the minimum cost partial tree can't be found by the program
            # a message will be displayed, it is written that it can't be found
            text_box = Text(root, width=500, height=1.2, font=('consolas', 10, 'bold'), bg='#424242',
                            foreground='#FFFFFF')
            text_box.place(x=0, y=0)
            text_box2 = Text(root, width=500, height=1.2, font=('consolas', 10, 'bold'), bg='#424242',
                             foreground='#FFFFFF')
            text_box2.place(x=0, y=20)
            text_box.insert(END, "This option is not available")
            text_box.configure(state='disable')
            text_box2.insert(END, "for directed graph")
            text_box2.configure(state='disable')
            return

        # in the edges_tree are the edges of the tree
        self.edges_tree = algorithms.partial_tree(self.G, self.is_weighted)

        self.prepare_the_canvas()
        figure2 = self.figure
        a = self.a

        plt.axis('off')

        if not self.is_weighted:
            # the edges are added to the Tree(graph)
            # and it is displayed
            self.Tree.clear()
            self.Tree.add_edges_from(self.edges_tree)
            nx.draw_networkx(self.Tree, pos=nx.spring_layout(self.Tree), ax=a)
        else:
            # the edges are added to the Tree
            self.Tree.clear()
            for i in self.edges_tree:
                self.Tree.add_edge(i[0], i[1], weight=i[2])

            # and it is displayed
            pos = nx.spring_layout(self.Tree)
            nx.draw(self.Tree, pos)
            edge_labels = dict([((u, v,), d['weight'])
                                for u, v, d in self.Tree.edges(data=True)])
            nx.draw_networkx_edge_labels(self.Tree, pos, edge_labels=edge_labels)
            nx.draw_networkx(self.Tree, pos, edge_labels=edge_labels)

        canvas = FigureCanvasTkAgg(figure2, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=30)

        # when this button is pressed, the image of the tree will be saved
        save_tree_image_button = Button(root, text="Save image",
                                        font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                        activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                        command=self.save_tree_image).place(x=0, y=0)

        # this save the list of edges of the tree
        save_tree_button = Button(root, text="Save tree",
                                  font=('consolas', 10, 'bold'), foreground='#FFFFFF',
                                  activebackground='#FFFFFF', activeforeground='darkblue', bg='#716C6A',
                                  command=self.save_the_tree).place(x=81, y=0)

        root.mainloop()

    # this function insert messages on read only text boxes
    def insert_in_textbox(self, box, txt):
        box.configure(state='normal')
        box.delete(1.0, END)
        box.insert(END, txt)
        box.configure(state='disabled')

    # this take 2 nodes from dijkstra1 and dijkstra2
    # and calculate the distance between them and the optimal meeting point
    def dijkstra_function(self):
        self.draw_button_function()  # this is to be sure that the plotted graph and the graph from memory are same
        node1 = self.dijkstra1.get(1.0, 'end-1c')  # this take first node
        node2 = self.dijkstra2.get(1.0, 'end-1c')  # this take second node
        node1 = str(node1)
        node2 = str(node2)

        not_found = False  # this for error if one of the nodes in not in the graph
        if node1 not in self.G:
            # this check if first node is in the graph
            self.insert_in_textbox(self.dijkstra_answer, "First node is not in the graph")
            self.insert_in_textbox(self.dijkstra_answer2, '')
            not_found = True

        if node2 not in self.G:
            # this check if the second node is in the graph
            if node1 in self.G:
                self.insert_in_textbox(self.dijkstra_answer, '')
            txt = "Second node is not in the graph"
            self.insert_in_textbox(self.dijkstra_answer2, txt)
            not_found = True

        # if first node is not in the graph, this will be displayed in dijkstra_answer
        # if second node is not in the graph, this will be displayed in dijkstra_answer2

        if not_found:
            return

        # this take the meeting point and distances between (calculated in algorithm)
        meeting_node, distance1, distance2 = algorithms.dijkstra(self.G, node1, node2, self.is_weighted)

        # here is the display process
        txt = str()
        if not meeting_node == '-1':
            txt = "One of the optimal meeting points is " + meeting_node + "."
        else:
            txt = "There is no meeting point."
        self.insert_in_textbox(self.dijkstra_answer, txt)

        txt = str()
        if distance1 < 999999999999999999999:
            txt = "Distance from first node to second is " + str(distance1) + "."
        else:
            txt = "There is no way from first node to second."
        if distance2 < 999999999999999999999:
            txt = txt + " Distance from second node to first is " + str(distance2) + "."
        else:
            txt = txt + " There is no way from second node to first."
        self.insert_in_textbox(self.dijkstra_answer2, txt)
        # if a node cannot be reached from another, a related message is displayed

    # this take the number of components calculated in algorithm and display the number
    def write_the_components_number(self):
        txt = str()
        txt = "You have "
        # this if select if the number is the number of connected components or it is the
        # number of strong connected components
        if not self.is_directed:
            cnt = algorithms.number_connected_components(self.G)
            txt = txt + str(cnt)
            if cnt == 1:
                txt = txt + " component"
            else:
                txt = txt + " components"
        else:
            cnt = algorithms.number_strong_connected_components(self.G)
            txt = txt + str(cnt)
            if cnt == 1:
                txt = txt + " strong connected component"
            else:
                txt = txt + " strong connected components"
        self.insert_in_textbox(self.components, txt)

    def write_is_eulerian(self):
        self.insert_in_textbox(self.euler_text, "Your graph is Eulerian")

    def write_is_not_eulerian(self):
        self.insert_in_textbox(self.euler_text, "Your graph is not Eulerian")

    # this prepare the canvas for a new plot
    def prepare_the_canvas(self):
        self.canvas.get_tk_widget().pack_forget()
        self.a.clear()

    # this plot the graph if it is unweighted
    def draw_the_network(self):
        # the canvas must pe prepared
        self.prepare_the_canvas()
        plt.axis('off')

        # take the edges from the list
        self.G.add_edges_from(self.edges)
        self.txt.delete(1.0, END)
        for edge in self.edges:
            self.txt.insert(END, edge[0])
            self.txt.insert(END, " ")
            self.txt.insert(END, edge[1])
            self.txt.insert(END, "\n")

        # write the number of connected components in the relative box
        self.write_the_components_number()

        # the drawing function run when a new graph is introduced, so this is the best moment to
        # check if the graph is eulerian and display the correct message

        graph_is_not_empty = False
        if any(self.G.adj.values()):
            graph_is_not_empty = True

        if graph_is_not_empty:
            if algorithms.is_eulerian(self.G):
                self.write_is_eulerian()
            else:
                self.write_is_not_eulerian()
        else:
            self.write_is_not_eulerian()

        # draw the graph on canvas
        nx.draw_networkx(self.G, pos=nx.spring_layout(self.G), ax=self.a)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        self.canvas.draw()
        # put the canvas in window
        self.canvas.get_tk_widget().place(x=250, y=40)

    def unweighted(self):
        # transform the graph in a unweighted graph
        self.is_weighted = False
        if self.something_is_read:
            # if something is read, draw the graph from memory
            self.draw_button_function()
        else:
            # if nothing has been introduced yet, the standard unweighted graph is plotted
            # and the list of edges is displayed for a better understanding of how it works
            self.txt.delete(1.0, END)
            for edge in self.edges:
                self.txt.insert(END, edge[0])
                self.txt.insert(END, " ")
                self.txt.insert(END, edge[1])
                self.txt.insert(END, "\n")
            self.draw()

    # this plot the graph if it is weighted
    def draw_the_network_weighted(self):
        # prepare the canvas for drawing the network
        self.prepare_the_canvas()
        plt.axis('off')

        # take the nodes and edges from list of weighted edges
        nodes = {0}
        for i in self.weighted_edges:
            if i[0] not in nodes:
                nodes.add(i[0])
                self.G.add_node(i[0])
            if i[1] not in nodes:
                nodes.add(i[1])
                self.G.add_node(i[1])

        for i in self.weighted_edges:
            self.G.add_edge(i[0], i[1], weight=i[2])

        self.txt.delete(1.0, END)
        for edge in self.weighted_edges:
            self.txt.insert(END, edge[0])
            self.txt.insert(END, " ")
            self.txt.insert(END, edge[1])
            self.txt.insert(END, " ")
            self.txt.insert(END, edge[2])
            self.txt.insert(END, "\n")

        # display the number of strong connected components
        self.write_the_components_number()

        # the drawing function run when a new graph is introduced, so this is the best moment to
        # check if the graph is eulerian and display the correct message

        graph_is_not_empty = False
        if any(self.G.adj.values()):
            graph_is_not_empty = True

        if graph_is_not_empty:
            if algorithms.is_eulerian(self.G):
                self.write_is_eulerian()
            else:
                self.write_is_not_eulerian()
        else:
            self.write_is_not_eulerian()

        # plot the graph on canvas and put the canvas on window
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos)
        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in self.G.edges(data=True)])
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        nx.draw_networkx(self.G, pos, edge_labels=edge_labels)
        self.canvas.draw()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        self.canvas.get_tk_widget().place(x=250, y=40)

    # transform the graph in a weighted graph
    def weighted(self):
        self.is_weighted = True
        if self.something_is_read:
            # if something is read, plot the new graph
            self.draw_button_function()
        else:
            # else plot the standard weighted graph
            # and display the list of edges for a better understanding of how it works
            self.txt.delete(1.0, END)
            for edge in self.weighted_edges:
                self.txt.insert(END, edge[0])
                self.txt.insert(END, " ")
                self.txt.insert(END, edge[1])
                self.txt.insert(END, " ")
                self.txt.insert(END, edge[2])
                self.txt.insert(END, "\n")
            self.draw()

    # this draw the relative graph
    def draw(self):
        if not self.is_weighted:
            self.draw_the_network()
        else:
            self.draw_the_network_weighted()

    # this take the input and draw the graph
    def draw_button_function(self):
        self.retrieve_input()
        if self.cant_be_string:
            self.clear()
            self.insert_in_textbox(self.euler_text, "I am very sorry, but the weights cannot be strings")
            self.dijkstra1.configure(state='disable')
            self.dijkstra2.configure(state='disable')
        elif self.cant_be_uppercase:
            self.clear()
            self.insert_in_textbox(self.euler_text,
                                   "I am very sorry, but the nodes and the weights cannot be uppercase letter")
            self.dijkstra1.configure(state='disable')
            self.dijkstra2.configure(state='disable')
        else:
            self.dijkstra1.configure(state='normal')
            self.dijkstra2.configure(state='normal')
            self.draw()

    # this transform the graph in a directed graph
    def directed(self):
        # to be sure that is displayed the graph from text box
        self.retrieve_input()
        self.G = nx.DiGraph()
        self.is_directed = True
        if self.something_is_read:
            self.draw_button_function()
        else:
            self.draw()

    # this transform the graph in a non-directed graph
    def undirected(self):
        # to be sure that is displayed the graph from text box
        self.retrieve_input()
        self.G = nx.Graph()
        self.is_directed = False
        if self.something_is_read:
            self.draw_button_function()
        else:
            self.draw()

    # this take the input from the relative text box
    def retrieve_input(self):
        lines = self.txt.get("1.0", END).splitlines()
        numbers = []
        self.cant_be_uppercase = False
        for i in lines:
            number = ''
            for j in i:
                if 'A' <= j <= 'Z':
                    self.cant_be_uppercase = True

                if ('0' <= j <= '9') or ('a' <= j <= 'z'):
                    number = number + j
                else:
                    numbers.append(number)
                    number = ''
            if number != '':
                numbers.append(number)

        # this put the read lines in the correct list of edges
        if not self.is_weighted:
            self.edges.clear()
            self.cant_be_string = False

            was_introduced = False
            if len(numbers):
                was_introduced = True

            # if there are more numbers in the input than there are needed,
            # the surplus is deleted
            if len(numbers) % 2:
                numbers.pop()

            if was_introduced and not len(numbers):
                self.something_is_read = True
                self.G.clear()

            # when hat_to_pas is True means that current number is from an edge added before
            has_to_pass = False
            for i in range(len(numbers) - 1):
                if has_to_pass:
                    has_to_pass = False
                else:
                    self.edges.append((numbers[i], numbers[i + 1]))
                    has_to_pass = True
            if len(self.edges) > 0:
                self.G.clear()
                self.something_is_read = True
        else:
            self.weighted_edges.clear()
            self.cant_be_string = False

            was_introduced = False
            if len(numbers):
                was_introduced = True

            # if there are more numbers in the input than there are needed,
            # the surplus is deleted
            while len(numbers) % 3:
                numbers.pop()

            if was_introduced and not len(numbers):
                self.something_is_read = True
                self.G.clear()

            # when has_to_pas is not 0, current number is from an edge added before
            has_to_pass = 0
            for i in range(len(numbers) - 2):
                if has_to_pass != 0:
                    has_to_pass = has_to_pass - 1
                else:
                    self.weighted_edges.append((numbers[i], numbers[i + 1], numbers[i + 2]))
                    for digit in str(numbers[i + 2]):
                        # if the user try to introduce a string as a weight, an error message will be diplayed
                        if not '0' <= digit <= '9':
                            self.cant_be_string = True
                            break
                    has_to_pass = 2

            # if was something in the text box means that something was introduced
            if len(self.weighted_edges) > 0:
                self.G.clear()
                self.something_is_read = True

    # this clear all
    def clear(self):

        # this clear the canvas
        self.prepare_the_canvas()
        plt.axis('off')
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=250, y=40)

        # this clear the text box where is displayed the number of components
        self.insert_in_textbox(self.components, '')
        # this clear the text box where is displayed if the graph is eulerian
        self.insert_in_textbox(self.euler_text, '')
        # this clear the text box where is displayed the meeting point
        self.insert_in_textbox(self.dijkstra_answer, '')
        # this clear the text box where is displayed the distance between nodes
        self.insert_in_textbox(self.dijkstra_answer2, '')

        # this delete the first introduced node
        self.dijkstra1.delete(1.0, END)
        # this delete the second introduced node
        self.dijkstra2.delete(1.0, END)


if __name__ == '__main__':
    app = GraphEditor()
