

#TO DO: Fix the visualization of Dijkstra


import pygame,math,time,sys
from collections import deque

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 18)
WHITE =     (255, 255, 255)
GRAY = (30,30,30)
RED =       (255,   40,   40)
BLACK = (  0,   0,  0)
Highlight_green = (152,251,152,40)
Highlight_red = (251,152,152,40)
Highlight_blue = (152,152,251,40)
(width, height) = (500, 500)
button = pygame.Rect(350, 420, 100, 50)

button_kruskal = pygame.Rect(200, 420, 100, 50)
button_dijkstra = pygame.Rect(40, 420, 100, 50)

running = True


class Node:
    def __init__(self,name,x,y):
        self.position = x,y
        self.name = name
    def __repr__(self):
        return str((self.name,self.position))
    def collides(self,pos):
        return (pos[0]-self.position[0])**2+(pos[1]-self.position[1])**2<=100

class Graph(Node):
    def __init__(self):
        self.nodes = []
        self.edges = {}
        
    def add_node(self,name,x,y):
        self.nodes.append(Node(name,x,y))
        
    def add_edge(self,node1,node2):
        self.edges[frozenset([node1.name,node2.name])] = ((node1.position[0]-node2.position[0])**2+(node1.position[1]-node2.position[1])**2)**0.5


    def neighbors(self,node):
        nb = deque()
        for v in self.nodes:
            print(frozenset([node,v]))
            if frozenset([node.name,v.name]) in self.edges:
                nb.append(v)
        return nb

def main():
    global running, win, G
    G = Graph()
    i = 0
    flag = 0    
    win = pygame.display.set_mode((width, height))
    win.fill(WHITE)
    pygame.draw.rect(win, GRAY, button)
    pygame.draw.rect(win, GRAY, button_kruskal)
    pygame.draw.rect(win, GRAY, button_dijkstra)
    
    text_button1 = font.render("ADD NODE", True, WHITE)
    text_button2 = font.render("ADD EDGE", True, WHITE)
    text_display1 = text_button1.get_rect(center=(400, 450))
    win.blit(text_button1, text_display1)


    text_button3 = font.render("KRUSKAL", True, WHITE)
    text_button4 = font.render("DIJKSTRA", True, WHITE)
    text_display3 = text_button3.get_rect(center=(250, 450))
    text_display4 = text_button4.get_rect(center=(90, 450))
    win.blit(text_button3, text_display3)
    win.blit(text_button4, text_display4)
    
    pygame.display.update()
    selected_nodes = []
    
    while running:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                pygame.draw.rect(win, RED, button)
                pygame.display.update()
                
            if event.type == pygame.MOUSEBUTTONUP:
                if button_kruskal.collidepoint(event.pos):
                    kruskal()
                if button_dijkstra.collidepoint(event.pos):
                    dijkstra(G.nodes[0],G.nodes[1])
                if button.collidepoint(event.pos):
                    flag+=1
                    pygame.draw.rect(win, GRAY, button)
                    if not flag%2:
                        win.blit(text_button1, text_display1)
                    else:
                        win.blit(text_button2, text_display1)
                    pygame.display.update()
                else:
                    if not flag%2:
                        pos = getPos()
                        time.sleep(0.1)
                        G.add_node(i,pos[0],pos[1])
                        i+=1
                        drawNode()
                    else:
                        for node in G.nodes:
                            if node.collides(event.pos):
                                if len(selected_nodes)<2:
                                    if node not in selected_nodes: selected_nodes.append(node)
                                print(selected_nodes)
                                if len(selected_nodes)==2 and frozenset([selected_nodes[0],selected_nodes[1]]) not in G.edges:
                                    G.add_edge(selected_nodes[0],selected_nodes[1])
                                    pygame.draw.line(win,RED,selected_nodes[0].position,selected_nodes[1].position)
                                    selected_nodes = []
                                    print(G.edges)
                                elif len(selected_nodes)<2:
                                    pass
                                else:
                                    selected_nodes.pop()
                                    

                    pygame.display.update()

            if event.type == pygame.QUIT:
                running = False


def dijkstra(initial,final):
    d = {}
    for v in G.nodes:
        d[v] = sys.maxsize
    d[initial] = 0
    visited = {initial}
    current = initial
    
    pygame.draw.circle(win,Highlight_green,current.position,13)
    pygame.display.update()
    time.sleep(0.5)
    while 1:
        if current == final:
            return d[final]
        minimum = sys.maxsize
        next_node = None
        for v in G.neighbors(current):
            if v not in visited:
                pygame.draw.circle(win,Highlight_blue,v.position,13)
                pygame.display.update()
                time.sleep(0.5)
                d[v] = min(G.edges[frozenset({current.name,v.name})]+d[current],d[v])
                pygame.draw.circle(win,BLACK,v.position,13)
                pygame.display.update()
        for i in G.nodes:
            if d[i]<=minimum and i not in visited:
                minimum = d[i]
                next_node = i
                #FIX THISSSS!!!!
        pygame.draw.line(win,BLACK,current.position,next_node.position,10)
        print(visited)
        pygame.draw.circle(win,Highlight_red,current.position,13)
        current = next_node
        pygame.draw.circle(win,Highlight_green,current.position,13)
        pygame.display.update()
        time.sleep(0.5)
        visited.add(current)



def kruskal():
    edges = deque(sorted(G.edges,key = lambda x: G.edges[x]))
    tree = []
    
    connected_components = list(set([i.name]) for i in G.nodes)
    
    vertices = set()
    while len(tree) < len(G.nodes)-1:
        edges[0] = list(edges[0])
        new_component = []
        for i in connected_components:
            if edges[0][0] in i or edges[0][1] in i:
                new_component.append(i)
        if new_component[0]!=new_component[1] and len(new_component)==2:
            connected_components.remove(new_component[0])
            connected_components.remove(new_component[1])
            connected_components.append(new_component[0].union(new_component[1]))
            selected_nodes = []
            for i in G.nodes:
                if i.name == edges[0][0] or i.name == edges[0][1]:
                    selected_nodes.append(i)
            #print(selected_nodes)
            pygame.draw.line(win,Highlight_red,selected_nodes[0].position,selected_nodes[1].position,10)
            pygame.display.update()
            time.sleep(1)
            tree.append(edges[0])
        edges.popleft()
    for i in G.nodes:
        pygame.draw.circle(win,Highlight_green,i.position,13)
    pygame.display.update()
    return tree
        

    
def getPos():
    pos = pygame.mouse.get_pos()
    return (pos)

def drawNode():
    pos=getPos()
    pygame.draw.circle(win, BLACK, pos, 10)


if __name__ == '__main__':
    main()
