from graphics import *

"""
Rules for room designing
- all sprite images must be relatively rectangular

"""

class Button:
    """A button is a labeled rectangle in a window. It is activated or
    deactivated with the activate() and deactivate() methods. The clicked(p)
    method returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg: quit_b = Button(myWin, centerPoint,
        width, height, 'Quit') """
        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        """Returns true if button active and p is inside"""
        if not p == None:
            return (self.active and
            self.xmin <= p.getX() <= self.xmax and
            self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        """Returns the label string of this button."""
        return self.label.getText()

    def activate(self):
        """Sets this button to 'active'."""
        self.label.setFill('black')
        self.rect.setWidth(1)
        self.active = True

    def deactivate(self):
        """Sets this button to 'inactive'."""
        self.label.setFill('darkgrey')
        self.rect.setWidth(0)
        self.active = False

    def delete(self):
        """Undraws the button"""
        self.deactivate()
        self.label.undraw()
        self.rect.undraw()

def create_room(room_num):
    room_objs = []
    encounter_objs = []

    if room_num == 1:
        cRectangles = [Rectangle(Point(65, 95), Point(405, 102)),
                       Rectangle(Point(65, 95), Point(70, 400)),
                       Rectangle(Point(405, 390), Point(70, 400)),
                       Rectangle(Point(405, 390), Point(70, 400)),
                       Rectangle(Point(396.0, 96.0), Point(404.0, 194.0)),
                       Rectangle(Point(404.0, 188.0), Point(498.0, 196.0)),
                       Rectangle(Point(396.0, 296.0), Point(403.0, 397.0)),
                       Rectangle(Point(401.0, 295.0), Point(497.0, 309.0))
                       ]

        for rect in cRectangles:
            rect.setWidth(0)
            room_objs.append(rect)

    elif room_num == 2:
        cRectangles = [Rectangle(Point(0.0, 197.0), Point(499.0, 188.0)),
                       Rectangle(Point(0.0, 296.0), Point(499.0, 308.0))]

        for rect in cRectangles:
            rect.setWidth(0)
            room_objs.append(rect)

    return room_objs, encounter_objs

# Previews a room based on number entered in roomnum

def testroom():
    win = GraphWin("Test Window", 600, 500)
    win.setBackground('slate blue')

    # Change num to change test room
    room_num = 1

    room_img = Image(Point(250, 250), "assets/rooms_img/{}.gif".format(room_num))
    room_img.draw(win)

    room_objs, encounter_objs = create_room(room_num)

    for obj in room_objs:
        if isinstance(obj, Rectangle):
            obj.setOutline('red')
            obj.setWidth(1)
            obj.draw(win)

    new_rect_but = Button(win, Point(550, 100), 80, 30, 'New Rect')
    finish = Button(win, Point(550, 400), 50, 30, 'Done')

    new_rect_but.activate()
    finish.activate()

    RectList = []

    while True:

        mouseClick = win.getMouse()

        if new_rect_but.clicked(mouseClick):
            P1 = win.getMouse()
            P2 = win.getMouse()

            new_rect = Rectangle(P1, P2)
            new_rect.setOutline('red')
            new_rect.setWidth(1)
            new_rect.draw(win)

            RectList.append(new_rect)

        elif finish.clicked(mouseClick):
            print(RectList)
            win.close()
            exit()


    win.getMouse()
    win.close()

# Only runs testroom if this script is run
if __name__ == "__main__":
    testroom()
