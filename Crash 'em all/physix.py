import tkinter as tk
from random import randint

plt = []

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400, bg='black')
canvas.pack()

def gravity():
    for c_plt in range(len(plt)):
        dx = 0
        dy = 0
        for s_plt in plt:
            if s_plt != plt[c_plt]:
                c_plt_r = ((((canvas.coords(plt[c_plt][0])[2] - canvas.coords(plt[c_plt][0])[0])**2)+((canvas.coords(plt[c_plt][0])[3] - canvas.coords(plt[c_plt][0])[1])**2))**0.5)/2
                s_plt_r = ((((canvas.coords(s_plt[0])[0] - canvas.coords(s_plt[0])[2])**2)+((canvas.coords(s_plt[0])[1] - canvas.coords(s_plt[0])[3])**2))**0.5)/2
                c_plt_c = [canvas.coords(plt[c_plt][0])[0] - c_plt_r, canvas.coords(plt[c_plt][0])[1] - c_plt_r]
                s_plt_c = [canvas.coords(s_plt[0])[0] - s_plt_r, canvas.coords(s_plt[0])[1] - s_plt_r]
                dist = (((s_plt_c[0] - c_plt_c[0])**2)+((s_plt_c[1] - c_plt_c[1])**2))**0.5
                grav = (6.7*10**-11)*plt[c_plt][1]*s_plt[1]/dist**2
                print(grav, dist, plt[c_plt][1], s_plt[1])
                if c_plt_c[0] < s_plt_c[0]:
                    dx += grav
                else:
                    dx -= grav
                if c_plt_c[1] < s_plt_c[1]:
                    dy += grav
                else:
                    dy -= grav
        canvas.move(plt[c_plt][0], dx, dy)
    canvas.after(40, gravity)

def placeP(eventorigin):
      Px = eventorigin.x
      Py = eventorigin.y
      np = randint(5, 10)
      plt.append([canvas.create_oval(Px-np,Py-np,Px+np,Py+np ,width = 1,fill = "white"), round(3.14*((((np*2)**0.5)**2)/2)**2)**3])
      canvas.pack()
      return None

root.bind("<Button 1>" ,placeP)
gravity()

root.mainloop()
