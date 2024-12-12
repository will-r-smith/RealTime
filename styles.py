from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import ImageFont


def get_style(root, theme="awdark"):
    """
    configured themes:
    
      -  awdark
      -  ...

    """
    style = ttk.Style(root)
    try:

        theme_folder = "assets/themes/" + theme

        print(theme_folder)

        root.tk.call('lappend', 'auto_path', theme_folder)
        root.tk.call('package', 'require', theme)

        style.theme_use(theme)
        print("Theme loaded successfully.")

        font_path = "assets/fonts/TW Cen MT.ttf"
        custom_font = ImageFont.truetype(font_path, size=12)
        font_family = custom_font.getname()[0]



        # Configure font for all labels
        custom_font1 = (font_family, 14)
        custom_font2 = (font_family, 11)
        custom_font3 = (font_family, 10)



        style.configure('.', font=custom_font2)
        style.configure('TLabel', font=custom_font2)
        style.configure('TButton', font=custom_font2)
        style.configure('TFrame', font=custom_font2)

        bar_colour = "#40484a"

        background = style.lookup('.', 'background')
        button_background = style.lookup('TButton', 'background')
        accent = style.lookup('.', 'selectbackground')

        #make a custom style for title page
        style.configure("CustomTitlePage.TFrame", background=background)  # Change the color as desired
        style.configure("CustomTitlePage.TLabel", background=background, foreground="white", font=custom_font1)
        style.configure("CustomTitlePage.TMenubutton", background=background, foreground="white", font=custom_font1)
        style.configure("CustomTitlePage.TButton", background=button_background, foreground="white", font=custom_font1)


        style.configure("CustomTitleBar.TFrame", background=bar_colour)  # Change the color as desired
        style.configure("CustomTitleBar.TLabel", background=bar_colour, foreground="white", font=custom_font2)
        style.configure("CustomTitleBar.TMenubutton", background=bar_colour, foreground="white", font=custom_font2)
        style.configure("CustomTitleBar.TButton", background=bar_colour, foreground="white", font=custom_font2)

        
        style.configure("SmallButton.TButton", background=button_background, foreground="white", font=custom_font3)
        style.configure("SaveButton.TButton", background=accent, foreground="white", font=custom_font3)
        style.configure("CancelButton.TButton", background="#828282", foreground=button_background, font=custom_font3)

        style.configure("LargeFont.TLabel", background=background, foreground="white", font=custom_font1)
        style.configure("LargeFont.TButton", background=accent, foreground="white", font=custom_font1)
        
        style.configure("BorderFrame.TFrame", background=background, border="black")


        style.configure("ThinFrame.TFrame", background="#101112")


    except Exception as e:
        print(f"Failed to load theme. Using default theme. Error: {e}")
    return style


def extract_colours(style):
    colours = {
        "background": style.lookup('.', 'background'),
        "foreground": style.lookup('.', 'foreground'),
        "accent": style.lookup('.', 'selectbackground'),
        "buttonbackground": style.lookup('TButton', 'background'),
    }
    colours["manual-light"] = "#40484a"
    colours["manual-dark"] = "#141414"
    print(colours)
    return colours


def display_color_palette(colors):
    fig, ax = plt.subplots(figsize=(8, 2))
    for i, (color_name, color_value) in enumerate(colors.items()):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color_value))
        ax.text(i + 0.5, -0.3, color_name, ha='center', va='center', fontsize=12)
    ax.set_xlim(0, len(colors))
    ax.set_ylim(-1, 1)
    ax.axis('off')
    plt.show()


