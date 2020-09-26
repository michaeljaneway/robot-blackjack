from graphics import *

"""
Rules for room designing
- all sprite images must be relatively rectangular

"""

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
    room_num = 2

    room_img = Image(Point(250, 250), "rooms_img/{}.gif".format(room_num))
    room_img.draw(win)

    room_objs = create_room(room_num)

    for obj in room_objs:
        if isinstance(obj, Rectangle):
            obj.setOutline('red')
            obj.setWidth(1)
            obj.draw(win)

    new_rect_but = Button(win, Point(550, 100), 50, 30, 'New Rect')
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
