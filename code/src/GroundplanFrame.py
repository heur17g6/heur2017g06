from Tkinter import *


class GroundplanFrame(object):

    extra = 11

    MARGINLEFT = 25
    MARGINTOP = 25

    COLOR_WATER = "blue"
    COLOR_PLAYGROUND = "green"

    def __init__(self, plan):
        self.SCALE = 3
        self.root = Tk()
        self.plan = plan

        self.frame = Frame(self.root, width=1024, height=768, colormap="new")
        self.frame.pack(fill=BOTH, expand=1)

        self.label = Label(self.frame, text="Heuristics 2016 - Amstelhaege!")
        self.label.pack(fill=X, expand=1)

        self.canvas = Canvas(self.frame,
                             bg="white",
                             width=self.plan.getWidth() * self.SCALE,
                             height=self.plan.getHeight() * self.SCALE)

        self.canvas.bind("<Button-1>", self.processMouseEvent)
        self.canvas.focus_set()

        self.text = Text(self.root, bd=4, width=80, height=2)

    def draw_circumference(self, o, r, col):


        print r

        self.line(o.x1, o.y1 - r, o.x2, o.y1 - r, col)
        self.line(o.x2 + r, o.y1, o.x2 + r, o.y2, col)
        self.line(o.x1 - r, o.y1, o.x1 - r, o.y2, col)
        self.line(o.x1, o.y2 + r, o.x2, o.y2 + r, col)
        self.circular_edge(o.x1, o.y1, r, -1.0, -1.0)
        self.circular_edge(o.x1, o.y2, r, -1.0, 1.0)
        self.circular_edge(o.x2, o.y1, r, 1.0, -1.0)
        self.circular_edge(o.x2, o.y2, r, 1.0, 1.0)


    def setPlan(self):
        for residence in self.plan.getResidences():
            self.canvas.create_rectangle(residence.getX() * self.SCALE,
                                         residence.getY() * self.SCALE,
                                         (residence.getX() + residence.getWidth()) *
                                         self.SCALE,
                                         (residence.getY() + residence.getHeight()) *
                                         self.SCALE,
                                         fill=residence.getColor())
            self.draw_circumference(residence,residence.minimumClearance,'black')

        for waterbody in self.plan.getWaterbodies():
            self.canvas.create_rectangle(waterbody.getX() * self.SCALE,
                                         waterbody.getY() * self.SCALE,
                                         (waterbody.getX() + waterbody.getWidth()) *
                                         self.SCALE,
                                         (waterbody.getY() + waterbody.getHeight()) *
                                         self.SCALE,
                                         fill=self.COLOR_WATER)


        for playground in self.plan.getPlaygrounds():
            self.canvas.create_rectangle(playground.getX() * self.SCALE,
                                         playground.getY() * self.SCALE,
                                         (playground.getX() + playground.getWidth()) *
                                         self.SCALE,
                                         (playground.getY() + playground.getHeight()) *
                                         self.SCALE,
                                         fill=self.COLOR_PLAYGROUND)

            self.draw_circumference(playground,self.plan.MAXIMUM_PLAYGROUND_DISTANCE ,'green')


        self.text.insert(INSERT, "Value of plan is: ")
        self.text.insert(INSERT, self.plan.getPlanValue())
        self.text.insert(INSERT, "\nis valid: ")
        isval = self.plan.isValid()
        # print isval
        self.text.insert(INSERT, isval)

        self.canvas.pack()
        self.text.pack(fill=BOTH, expand=1)

        self.root.update()

    def mark(self, x, y, c):

        self.canvas.create_line(
            x * self.SCALE, y * self.SCALE, x * self.SCALE, y * self.SCALE, fill=c)

    def circular_edge(self,x,y,distance,x_dir,y_dir):

        def compute_y(x,distance):

            x = float(x)
            distance = float(distance)
            assert x >= 0
            assert distance > 0

            y = abs((distance**2 - x**2))**0.5
            return y

        x_dist = 0.5
        while x_dist < distance:
            y_dist = compute_y(x_dist,int(distance))
            self.mark(x+x_dist*x_dir,y+y_dist*y_dir,'green')
            x_dist+=0.5

    def line(self,x1,y1,x2,y2,c):
        self.canvas.create_line(
            x1 * self.SCALE, y1 * self.SCALE, x2 * self.SCALE, y2 * self.SCALE, fill=c)

    def updateit(self):

        self.canvas.pack()
        self.root.update()

    def repaint(self, newPlan):
        self.text.delete(1.0, END)
        self.canvas.delete("all")
        self.plan = newPlan
        self.setPlan()

    def processMouseEvent(self, event):
        coordinates = ((event.x / self.SCALE), ",", (event.y / self.SCALE))
        self.canvas.create_text(event.x, event.y, text=coordinates)
