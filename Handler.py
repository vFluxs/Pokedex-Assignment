import pandas as pd
import customtkinter as ctk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

df = pd.read_csv("pokemon_data.csv")
df["Name"] = df["Name"].str.lower()
df["Type 1"] = df["Type 1"].fillna("None")
df["Type 2"] = df["Type 2"].fillna("None")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pokédex")
app.geometry("1200x750")

main_container = ctk.CTkFrame(app)
main_container.pack(fill="both", expand=True, padx=15, pady=15)
main_container.grid_columnconfigure(0, weight=3)
main_container.grid_columnconfigure(1, weight=1)
main_container.grid_rowconfigure(1, weight=1)

header_frame = ctk.CTkFrame(main_container, height=70)
header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

try:
    title_image = Image.open("Pokédex_image.png")
    title_image = title_image.resize((250, 70), Image.Resampling.LANCZOS)
    title_ctk_image = ctk.CTkImage(light_image=title_image, dark_image=title_image, size=(250, 70))
    title_label = ctk.CTkLabel(header_frame, text="", image=title_ctk_image)
    title_label.pack(expand=True, fill="both", pady=10)
except:
    title_label = ctk.CTkLabel(header_frame, text="Pokédex", font=("Arial", 32, "bold"))
    title_label.pack(expand=True, fill="both", pady=10)

right_panel = ctk.CTkFrame(main_container, corner_radius=10)
right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
right_panel.grid_rowconfigure(1, weight=1)
right_panel.grid_columnconfigure(0, weight=1)

filter_header = ctk.CTkFrame(right_panel, height=40)
filter_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
filter_label = ctk.CTkLabel(filter_header, text="Search & Filters", font=("Arial", 16, "bold"))
filter_label.pack(side="left", padx=10, pady=5)

filter_container = ctk.CTkFrame(right_panel)
filter_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
filter_container.grid_columnconfigure(0, weight=1)

search_label = ctk.CTkLabel(filter_container, text="Search Pokémon:", font=("Arial", 12))
search_label.grid(row=0, column=0, sticky="w", padx=5, pady=(10, 5))
search_entry = ctk.CTkEntry(filter_container, placeholder_text="Type Pokémon name...", height=35)
search_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))

type_label = ctk.CTkLabel(filter_container, text="Filter by Type:", font=("Arial", 12))
type_label.grid(row=2, column=0, sticky="w", padx=5, pady=(5, 5))
types = ["All"] + sorted(df["Type 1"].unique().tolist())
type_menu = ctk.CTkOptionMenu(filter_container, values=types, height=35)
type_menu.set("All")
type_menu.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 10))

gen_label = ctk.CTkLabel(filter_container, text="Filter by Generation:", font=("Arial", 12))
gen_label.grid(row=4, column=0, sticky="w", padx=5, pady=(5, 5))
gens = ["All"] + sorted(df["Generation"].unique().astype(str).tolist())
gen_menu = ctk.CTkOptionMenu(filter_container, values=gens, height=35)
gen_menu.set("All")
gen_menu.grid(row=5, column=0, sticky="ew", padx=5, pady=(0, 15))

list_header = ctk.CTkFrame(right_panel, height=40)
list_header.grid(row=2, column=0, sticky="ew", padx=10, pady=(10, 5))
list_label = ctk.CTkLabel(list_header, text="Pokémon List", font=("Arial", 16, "bold"))
list_label.pack(side="left", padx=10, pady=5)

list_container = ctk.CTkFrame(right_panel)
list_container.grid(row=3, column=0, sticky="nsew", padx=15, pady=(0, 15))
list_container.grid_rowconfigure(0, weight=1)
list_container.grid_columnconfigure(0, weight=1)

pokemon_list = ctk.CTkTextbox(list_container, font=("Arial", 13), wrap="none")
pokemon_list.grid(row=0, column=0, sticky="nsew", pady=(0, 5))

left_panel = ctk.CTkFrame(main_container, corner_radius=10)
left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
left_panel.grid_rowconfigure(1, weight=1)
left_panel.grid_columnconfigure(0, weight=1)

chart_header = ctk.CTkFrame(left_panel, height=50)
chart_header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
chart_header_label = ctk.CTkLabel(chart_header, text="Stats Visualization", font=("Arial", 18, "bold"))
chart_header_label.pack(side="left", padx=10, pady=5)

chart_controls = ctk.CTkFrame(chart_header)
chart_controls.pack(side="right", padx=10, pady=5)
chart_type_label = ctk.CTkLabel(chart_controls, text="Chart Type:", font=("Arial", 12))
chart_type_label.pack(side="left", padx=(0, 10), pady=5)

chart_types = ["Bar Chart", "Line Graph", "Pie Chart"]
chart_type_var = ctk.StringVar(value="Bar Chart")
chart_type_menu = ctk.CTkOptionMenu(chart_controls, values=chart_types, variable=chart_type_var, width=130, height=35)
chart_type_menu.pack(side="left", padx=(0, 10), pady=5)

chart_display = ctk.CTkFrame(left_panel)
chart_display.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
chart_frame = ctk.CTkFrame(chart_display)
chart_frame.pack(fill="both", expand=True)


def update_list(data):
    pokemon_list.configure(state="normal")
    pokemon_list.delete("1.0", "end")
    for name in sorted(data["Name"].tolist()):
        pokemon_list.insert("end", f"• {name.title()}\n")
    pokemon_list.configure(state="disabled")


def apply_filters():
    data = df.copy()
    query = search_entry.get().lower()
    if query:
        data = data[data["Name"].str.contains(query)]
    if type_menu.get() != "All":
        data = data[data["Type 1"] == type_menu.get()]
    if gen_menu.get() != "All":
        data = data[data["Generation"] == int(gen_menu.get())]
    update_list(data)


def update_chart():
    try:
        index = pokemon_list.index("insert")
        line = pokemon_list.get(f"{index} linestart", f"{index} lineend")
        name = line.strip().lower()
        if name.startswith("• "):
            name = name[2:]
        if not name or name.isspace():
            return
        show_stats(name)
    except:
        return


def show_stats(event=None):
    try:
        index = pokemon_list.index("insert")
        line = pokemon_list.get(f"{index} linestart", f"{index} lineend")
        name = line.strip().lower()
        if name.startswith("• "):
            name = name[2:]
    except:
        if len(df) > 0:
            name = df.iloc[0]["Name"]
        else:
            for widget in chart_frame.winfo_children():
                widget.destroy()
            error_label = ctk.CTkLabel(chart_frame, text="No Pokémon data available!", font=("Arial", 16))
            error_label.pack(expand=True)
            return

    if not name or name.isspace():
        return

    pokemon_match = df[df["Name"] == name]
    if pokemon_match.empty:
        for widget in chart_frame.winfo_children():
            widget.destroy()
        error_label = ctk.CTkLabel(chart_frame, text="Pokémon not found!", font=("Arial", 16))
        error_label.pack(expand=True)
        return

    pokemon = pokemon_match.iloc[0]
    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    values = [pokemon[s] for s in stats]
    chart_type = chart_type_var.get()

    for widget in chart_frame.winfo_children():
        widget.destroy()

    plt.style.use('dark_background')
    fig = plt.Figure(figsize=(7, 5), facecolor='#2b2b2b')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#2b2b2b')

    if chart_type == "Bar Chart":
        colors = ['#4da6ff', '#66b3ff', '#80c1ff', '#99ceff', '#b3dbff', '#cce8ff']
        bars = ax.bar(stats, values, color=colors, edgecolor='white', linewidth=1.5)
        ax.set_title(f"{name.title()} - Base Stats", fontsize=16, fontweight='bold', pad=20, color='white')
        ax.set_ylabel("Stat Value", fontsize=12, color='white')
        ax.set_xlabel("Stat", fontsize=12, color='white')
        ax.tick_params(colors='white')
        ax.grid(axis='y', alpha=0.2, linestyle='--', color='white')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.5, f'{int(height)}', ha='center', va='bottom',
                    fontsize=11, color='white', fontweight='bold')

    elif chart_type == "Line Graph":
        ax.plot(stats, values, marker='o', linewidth=3, markersize=10, color='#4da6ff')
        ax.fill_between(stats, values, alpha=0.2, color='#4da6ff')
        ax.set_title(f"{name.title()} - Stats Trend", fontsize=16, fontweight='bold', pad=20, color='white')
        ax.set_ylabel("Stat Value", fontsize=12, color='white')
        ax.set_xlabel("Stat", fontsize=12, color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, linestyle='--', color='white')
        for i, (stat, val) in enumerate(zip(stats, values)):
            ax.text(i, val + 1, f'{int(val)}', ha='center', va='bottom', fontsize=11, color='white', fontweight='bold')

    elif chart_type == "Pie Chart":
        filtered_stats, filtered_values, filtered_colors = [], [], []
        colors = ['#4da6ff', '#66b3ff', '#80c1ff', '#99ceff', '#b3dbff', '#cce8ff']
        for i, (stat, val) in enumerate(zip(stats, values)):
            if val > 0:
                filtered_stats.append(stat)
                filtered_values.append(val)
                filtered_colors.append(colors[i % len(colors)])

        if filtered_values:
            def make_autopct(values):
                total = sum(values)
                return lambda pct: f'{int(pct * total / 100.0)}'

            wedges, texts, autotexts = ax.pie(filtered_values, labels=filtered_stats, colors=filtered_colors,
                                              autopct=make_autopct(filtered_values), startangle=90,
                                              textprops={'fontsize': 11, 'color': 'white'})
            ax.set_title(f"{name.title()} - Stat Distribution", fontsize=16, fontweight='bold', pad=20, color='white')
            ax.axis('equal')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        else:
            ax.text(0.5, 0.5, "No valid data for pie chart", ha='center', va='center', fontsize=14, color='white')
            ax.set_title(f"{name.title()} - Stat Distribution", fontsize=16, fontweight='bold', pad=20, color='white')

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


search_entry.bind("<KeyRelease>", lambda e: apply_filters())
type_menu.configure(command=lambda _: apply_filters())
gen_menu.configure(command=lambda _: apply_filters())
chart_type_menu.configure(command=lambda _: update_chart())
pokemon_list.bind("<Double-Button-1>", show_stats)

apply_filters()
if len(df) > 0:
    show_stats()

app.mainloop()