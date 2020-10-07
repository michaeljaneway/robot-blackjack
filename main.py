from graphics import *
from time import sleep, perf_counter
from random import randint

"""
CC0 (Public domain) background assets are from https://opengameart.org/content/colony-sim-extended-version
CC0 (Public domain) character assets are from https://opengameart.org/content/pixel-robot
CC0 (Public domain) main menu terminal assets are from https://opengameart.org/content/communication-terminal-32x32
MIT Liscensed Pure Python library "Playsound" is used as to play sound effects
"""

"""
Changes to graphics library:
    + Added change_frame method to Image class to allow indexing of gif images

"""

# Imports the playsound module (Can play both .wav and .mp3 files, as well as
# multiple sounds at the same time, but cannot stop them)

import playsound

# Imports all of the graphics objects in the various rooms
from rooms import create_room

# Imports the keyboard module
import keyboard

# Imports the winsound module, which is to play longer soundfiles such as music
# (Can only play one .wav sound file at a time, but can stop using None as its filename
import winsound

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

class Encounter:
    def __init__(self, encounter_num):
        if encounter_num == 1:
            pass


class AudioSystem:
    def __init__(self):
        self.mute = False

    def play_music(self, filename):
        if not self.mute:
            winsound.PlaySound(filename, A_SYNC)

    def play_effect(self, filename):
        if not self.mute:
            playsound(filename)

    def mute(self, is_mute=True):
        self.mute = is_mute

class StartMenu:
    def __init__(self, win):
        background = overground("white")
        background.draw(win)

        titletext = Text(Point(250, 40), "BlackJack")
        titletext.setSize(32)
        titletext.draw(win)

        spacetext = Text(Point(250, 340), "Press Space to Start")
        spacetext.setSize(22)
        spacetext.draw(win)

        jakeface = Image(Point(250, 200), "assets/Main Menu.gif")
        jakeface.draw(win)

        while True:
            update()
            if keyboard.is_pressed('space'):
                background.undraw()
                titletext.undraw()
                spacetext.undraw()
                jakeface.undraw()
                break

            elif keyboard.is_pressed('esc'):
                ExitMenu(win)


class Character:
    def __init__(self, win):
        # Sprite for Character
        self.sprite1 = Rectangle(Point(235, 235), Point(265, 265))
        self.sprite1.setWidth(0)

        self.sprite2 = Image(self.sprite1.getCenter(), "assets/pixel-robot/right-robot-idle.gif")
        self.sprite2.draw(win)

        self.frame_num = 0

        self.timer = time.time_ns()


        self.m_left = False
        self.m_right = False

        self.f_left = False
        self.f_right = True

    def updateplayer(self, collidable_objs, win):
        self.wasdmove(self.sprite1, self.sprite2)
        self.sprite2.undraw()

        self.sprite2.anchor = self.sprite1.getCenter()
        self.sprite2.draw(win)

        # Makes the player collide with every solid object in the collidable_obj list
        for s_obj in collidable_objs:
            move_from_collide(self.sprite1, s_obj)

    def wasdmove(self, obj, sprite):
        # Moves player approximately the same length in all directions
        # Diagonal movement would be quicker if there was only one speed option
        # Origionally was .07 and .045
        reg_move_spd = 0.1
        diag_move_spd = 0.07


        # North-West
        if keyboard.is_pressed("w") and keyboard.is_pressed("a"):
            obj.move(-diag_move_spd, -diag_move_spd)

            self.m_left = True
            self.m_right = False

            self.f_left = True
            self.f_right = False

        # North-East
        elif keyboard.is_pressed("w") and keyboard.is_pressed("d"):
            obj.move(diag_move_spd, -diag_move_spd)

            self.m_left = False
            self.m_right = True

            self.f_left = False
            self.f_right = True

        # South-West
        elif keyboard.is_pressed("s") and keyboard.is_pressed("a"):
            obj.move(-diag_move_spd, diag_move_spd)

            self.m_left = True
            self.m_right = False

            self.f_left = True
            self.f_right = False

        # South-East
        elif keyboard.is_pressed("s") and keyboard.is_pressed("d"):
            obj.move(diag_move_spd, diag_move_spd)

            self.m_left = False
            self.m_right = True

            self.f_left = False
            self.f_right = True

        # North
        elif keyboard.is_pressed("w"):
            obj.move(0, -reg_move_spd)

            if self.f_left:
                self.m_left = True
                self.m_right = False
            else:
                self.m_left = False
                self.m_right = True


        # West
        elif keyboard.is_pressed("a"):
            obj.move(-reg_move_spd, 0)

            self.m_left = True
            self.m_right = False

            self.f_left = True
            self.f_right = False

        # South
        elif keyboard.is_pressed("s"):
            obj.move(0, reg_move_spd)

            if self.f_left:
                self.m_left = True
                self.m_right = False
            else:
                self.m_left = False
                self.m_right = True

        # East
        elif keyboard.is_pressed("d"):
            obj.move(reg_move_spd, 0)

            self.m_left = False
            self.m_right = True

            self.f_left = False
            self.f_right = True

        else:
            self.m_left = False
            self.m_right = False

        # Animation Section
        if self.m_left:
            self.sprite2.change_frame("assets/pixel-robot/left-robot-run.gif", self.frame_num)

        elif self.m_right:
            self.sprite2.change_frame("assets/pixel-robot/right-robot-run.gif", self.frame_num)

        elif self.f_left:
            self.sprite2.change_frame("assets/pixel-robot/left-robot-idle.gif", self.frame_num)

        elif self.f_right:
            self.sprite2.change_frame("assets/pixel-robot/right-robot-idle.gif", self.frame_num)


        if self.frame_num <= 5 and time.time_ns() - self.timer >= 90000000:
            self.frame_num += 1
            self.timer = time.time_ns()

        elif time.time_ns() - self.timer >= 90000000:
            self.frame_num = 0
            self.timer = time.time_ns()


class ExitMenu:
    def __init__(self, win):
        win.setCoords(0, 0, 500, 500)
        background = overground('lightgrey')
        background.draw(win)

        title = Text(Point(250, 190), "Are you sure that you would like to Exit?")
        title.draw(win)

        title1 = Text(Point(250, 240), "Press Esc to Exit")
        title1.draw(win)

        title2 = Text(Point(250, 290), "Press Space to Continue")
        title2.draw(win)

        update()

        # Must sleep, otherwise will register initial esc press as full exit
        sleep(0.3)

        while True:

            update()

            if keyboard.is_pressed("space"):
                background.undraw()
                title.undraw()
                title1.undraw()
                title2.undraw()
                break

            elif keyboard.is_pressed("esc"):
                win.close()
                exit()


class roomsystem:
    def __init__(self, win, room_map, pcollide_obj):
        y = 0
        x = 0
        self.room_map = room_map

        # Sets the initial position to whichever room is marked 1
        for column in room_map:
            for row in column:
                if row == 1:
                    self.current_position = [x, y, row]

                x += 1

            x = 0
            y += 1

        # These are the four rectangles that make up the doors to each room
        self.doors = [[Rectangle(Point(230, 0), Point(270, 20)), 0, False],
                      [Rectangle(Point(480, 230), Point(500, 270)), 1, False],
                      [Rectangle(Point(230, 480), Point(270, 500)), 2, False],
                      [Rectangle(Point(0, 230), Point(20, 270)), 3, False]]

        # Makes the 4 doors graphically appealing
        for doorgroup in self.doors:
            doorgroup[0].setFill(color_rgb(179,153,191))
            doorgroup[0].setOutline(color_rgb(134,129,171))
            doorgroup[0].setWidth(4)

        self.draw_room(win, pcollide_obj)

    def draw_room(self, win, pcollide_obj):
        # Draws the contents of the room
        room_num = self.room_map[self.current_position[1]][self.current_position[0]]

        self.room_img = Image(Point(250, 250), "assets/rooms_img/{}.gif".format(room_num))
        self.room_img.draw(win)

        # Logic to draw doors
        # Try-except used as easy fix for program trying to find rooms outside the array boundries
        try:
            if self.room_map[self.current_position[1] - 1][self.current_position[0]] > 0:
                self.doors[0][0].draw(win)
                self.doors[0][2] = True

            else:
                self.doors[0][2] = False

            if self.room_map[self.current_position[1]][self.current_position[0] + 1] > 0:
                self.doors[1][0].draw(win)
                self.doors[1][2] = True

            else:
                self.doors[1][2] = False

            if self.room_map[self.current_position[1] + 1][self.current_position[0]] > 0:
                self.doors[2][0].draw(win)
                self.doors[2][2] = True

            else:
                self.doors[2][2] = False

            if self.room_map[self.current_position[1]][self.current_position[0] - 1] > 0:
                self.doors[3][0].draw(win)
                self.doors[3][2] = True

            else:
                self.doors[3][2] = False

        except:
            pass

        # Gets the list of objects in the room from the creat_room func
        self.room_objs, self.encounter_objs = create_room(room_num)

        # Draws the objects in the room and appends them to the p_collide list
        for obj in self.room_objs:
            obj.draw(win)

            # Adds all rectangles in the room_obj list to pcollide_obj
            if isinstance(obj, Rectangle):
                pcollide_obj.append(obj)

            # Creates a rectangle around an image, allowing the character to collide with it
            elif isinstance(obj, Image):
                x = Rectangle(Point(obj.getAnchor().getX() - obj.getWidth()/2, obj.getAnchor().getY() - obj.getHeight()/2),
                              Point(obj.getAnchor().getX() + obj.getWidth()/2, obj.getAnchor().getY() + obj.getHeight()/2))
                x.setWidth(0)
                self.room_objs.append(x)


    def room_sys_cycle(self, player, win, pcollide_obj):
        for doorgroup in self.doors:
            if doorgroup[2]:
                if check_if_over(player.sprite1, doorgroup[0]):

                    # Undraw player and Doors
                    player.sprite1.undraw()
                    self.room_img.undraw()
                    for undraw_door in self.doors:
                        undraw_door[0].undraw()

                        # Undraws and removes from collision objects from previous room
                        for obj in self.room_objs:
                            obj.undraw()
                            if obj in pcollide_obj:
                                pcollide_obj.remove(obj)

                    # Going through up door
                    if doorgroup[1] == 0:
                        player.sprite1.move(0, 450)
                        self.current_position[1] -= 1
                        self.draw_room(win, pcollide_obj)
                        player.sprite1.draw(win)

                    # Going through right door
                    elif doorgroup[1] == 1:
                        player.sprite1.move(-450, 0)
                        self.current_position[0] += 1
                        self.draw_room(win, pcollide_obj)
                        player.sprite1.draw(win)

                    # Going through bottom door
                    elif doorgroup[1] == 2:
                        player.sprite1.move(0, -450)
                        self.current_position[1] += 1
                        self.draw_room(win, pcollide_obj)
                        player.sprite1.draw(win)

                    # Going through left door
                    elif doorgroup[1] == 3:
                        player.sprite1.move(450, 0)
                        self.current_position[0] -= 1
                        self.draw_room(win, pcollide_obj)
                        player.sprite1.draw(win)





# A background rectangle that will overlay everything in frame
def overground(color):
    background = Rectangle(Point(0, 0), Point(500, 500))
    background.setFill(color)
    background.setWidth(0)
    return(background)


# Moves a moving rectangle back from a static object, creating a collision effect
def move_from_collide(movobj, statobj):
    # Top Left
    P11 = movobj.getP1()

    # Bottom Right
    P12 = movobj.getP2()

    # Bottom Left
    P13 = Point(P11.x, P12.y)

    # Top Right
    P14 = Point(P12.x, P11.y)

    # Translates any rectangle points into its top left and bottom right points
    statobjx = [statobj.getP1().getX(), statobj.getP2().getX()]
    statobjx.sort()

    statobjy = [statobj.getP1().getY(), statobj.getP2().getY()]
    statobjy.sort()

    P21 = Point(statobjx[0], statobjy[0])
    P22 = Point(statobjx[1], statobjy[1])

    # Bottom Edge Collision Detection
    if (P21.x < P11.x < P22.x or P21.x < P14.x < P22.x) and P22.y - 0.1 < P11.y < P22.y:
        movobj.move(0, 0.1)

    # Right Edge Collision Detection
    elif P22.x - 0.1 < P11.x < P22.x and (P21.y < P11.y < P22.y or P21.y < P13.y < P22.y):
        movobj.move(0.1, 0)

    # Top Edge Collision Detection
    elif (P21.x < P12.x < P22.x or P21.x < P13.x < P22.x) and P21.y > P12.y > P21.y - 0.1:
        movobj.move(0, -0.1)

    # Left Edge Collision Detection
    elif P21.x - 0.1 < P14.x < P21.x and (P21.y < P14.y < P22.y or P21.y < P12.y < P22.y):
        movobj.move(-0.1, 0)

# Checks if the character rectangle is over a point
def check_if_over(character, point):
    if point.getP1().getX() <= character.getCenter().getX() <= point.getP2().getX() and point.getP1().getY() <= character.getCenter().getY() <= point.getP2().getY():
        return True


def main():
    # Creates the main window
    win = GraphWin("Michael Janeway's Blackjack Project", 500, 500, False)
    win.setBackground(color_rgb(98,105,141))

    # Create the audio system
    au_sys = AudioSystem()

    # Creates the start menu
    StartMenu(win)

    # The map that the player has to go through
    room_map = [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [1, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]

    # List of invisible rectangles that make up the walls around the frame
    outer_wall = [Rectangle(Point(0, 0), Point(500, 0)),
                  Rectangle(Point(0, 0), Point(0, 500)),
                  Rectangle(Point(500, 0), Point(500, 500)),
                  Rectangle(Point(0, 500), Point(500, 500))]

    # Coords
    x1, y1 = 0, 500
    x2, y2 = 500, 0
    win.setCoords(x1, y1, x2, y2)

    # List of all objects that the player will collide with
    pcollide_obj = []

    # Adds the outer wall to the list of obj that the player will collide with
    pcollide_obj += outer_wall

    # Creates the room system
    winroomsystem = roomsystem(win, room_map, pcollide_obj)

    # Creates the player obj
    player = Character(win)

    # Main Loop
    while True:
        winroomsystem.room_sys_cycle(player, win, pcollide_obj)
        player.updateplayer(pcollide_obj, win)
        update()

        x1 = player.sprite1.getCenter().getX() - 250
        x2 = player.sprite1.getCenter().getX() + 250
        y1 = player.sprite1.getCenter().getY() + 250
        y2 = player.sprite1.getCenter().getY() - 250
        win.setCoords(x1, y1, x2, y2)

        if keyboard.is_pressed("esc"):
            ExitMenu(win)

if __name__ == "__main__":
    main()