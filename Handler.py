import pandas as pd
import customtkinter as ctk
import matplotlib.animation as animation
from matplotlib import pyplot as plt


#x_values = [1,2,3,4]
#y_values = [2,4,6,8]
#plt.bar(x_values, y_values)
#plt.xlabel("x")
#plt.ylabel("y")
#plt.show() Matplotlib (shows bar chart of random values)

#csvFile = pd.read_csv('pokemon_data.csv')
#new = pd.DataFrame(csvFile)
#print(new.head(10)) pandas (gets the first 10 from the csv)

# Set Window
NewWindow = ctk.CTk()
NewWindow.geometry("550x700")
NewWindow.title("Example")
ctk.set_appearance_mode("dark")

import random
# Set Buttons
def button1interact():
    colour_list = ["red", "blue", "green", "yellow"]
    rcolour = random.choice(colour_list)
    Button1.configure(hover_color = rcolour)

Button1 = ctk.CTkButton(NewWindow,
                        text="Button1",
                        command = button1interact)
Button1.grid(row = 0, column = 0, padx = 205, pady = 20)

Button2 = ctk.CTkButton(NewWindow,
                        text="Button2",
                        width=75,
                        height=75)
Button2.grid(row = 1, column = 0, padx = 205, pady = 20)

NewWindow.mainloop()