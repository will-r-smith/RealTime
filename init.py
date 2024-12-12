import tkinter as tk
from tkinter import ttk
from variables import *
from tkinter import filedialog

from processing import create_plots, observe_param_change
from PIL import ImageTk, Image


def initialise_app(root):
    
    mainframe = ttk.Frame(root)
    mainframe.pack(fill=tk.BOTH, expand=True)

    top_frame = ttk.Frame(mainframe)
    top_frame.pack(side="top", fill="x")

    bottom_frame = ttk.Frame(mainframe)
    bottom_frame.pack(side="top", fill="x", padx=10, pady=10)

    variables_frame = ttk.Frame(top_frame)
    variables_frame.pack(side="left", fill="y", padx=10, pady=10)

    plot1_frame = ttk.Frame(top_frame)
    plot1_frame.pack(side="left", fill="y", padx=10, pady=10)



    # Button to open file explorer to select strTVISlocation
    def open_file_explorer():
        base_folder = filedialog.askdirectory(title="Select Base Folder for Experiment")
        if base_folder:
            strTVISlocation.set(base_folder)

    def update_plots():
        # Clear existing plots
        for widget in plot1_frame.winfo_children():
            widget.destroy()
        for widget in plot2_frame.winfo_children():
            widget.destroy()


        create_plots()

        images = []
        img = Image.open(f"temp_saves/plot1.png")
        img = img.resize((900, 300), Image.LANCZOS)
        images.append(ImageTk.PhotoImage(img))
        frame = ttk.Label(plot1_frame, image=images[0])
        frame.image = images[0]
        frame.pack(side="left")

        for i in range(2, 5):
            img = Image.open(f"temp_saves/plot{i}.png")
            img = img.resize((360, 270), Image.LANCZOS)
            images.append(ImageTk.PhotoImage(img))
            frame = ttk.Label(plot2_frame, image=images[i-1])
            frame.image = images[i-1]
            frame.pack(side="left")

        # create the images for each of the frames and then pack them 
        """ttk.Label(plot1_frame, image=images[1]).pack()
        ttk.Label(plot2_frame, image=metric1_img).pack(side="left")
        ttk.Label(plot2_frame, image=metric2_img).pack(side="left")
        ttk.Label(plot2_frame, image=metric3_img).pack(side="left")
        """
        # Schedule the function to run again after 1 minute (60000 milliseconds)
        root.after(5000, update_plots)

    pad_y1 = (1, 3)
    pad_y2 = (1, 6)

    ttk.Button(variables_frame, text="Select TVIS Location", command=open_file_explorer).pack(side="top", anchor="w", pady=3)
    ttk.Entry(variables_frame, textvariable=strTVISlocation).pack(side="top", anchor="w", pady=pad_y2)

    ttk.Label(variables_frame, text="Select TVIS Param:").pack(side="top", anchor="w", pady=pad_y1)
    ttk.Combobox(variables_frame, textvariable=strTVISparam, values=["Max_real", "Min_real", "C_img_Peak", "log_F_peak"]).pack(side="top", anchor="w", pady=pad_y2)

    ttk.Label(variables_frame, text="Select Channel:").pack(pady=pad_y1, side="top", anchor="w")
    ttk.Combobox(variables_frame, textvariable=intChannel, values=[1, 2, 3, 4, 5]).pack(side="top", anchor="w", pady=pad_y2)

    ttk.Label(variables_frame, text="Set Analysis Length:").pack(side="top", anchor="w", pady=pad_y1)
    ttk.Spinbox(variables_frame, from_=1, to=500, textvariable=intAnalysisLen).pack(side="top", anchor="w", pady=pad_y2)

    ttk.Label(variables_frame, text="Set Plot Length:").pack(side="top", anchor="w", pady=pad_y1)
    ttk.Spinbox(variables_frame, from_=1, to=100000, textvariable=intPlotLen).pack(side="top", anchor="w", pady=pad_y2)

    ttk.Button(variables_frame, text="Start", command=update_plots).pack(side="top", anchor="w", pady=pad_y1)

    plot2_frame = ttk.Frame(bottom_frame)
    plot2_frame.pack(side="left", fill="y")

    observe_param_change(root)


    



