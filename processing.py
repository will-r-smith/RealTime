import pandas as pd
from variables import *
import numpy as np

from scipy import interpolate
from PIL import ImageTk, Image

from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os
from datetime import datetime
import matplotlib.pyplot as plt



global param, metric1, metric2, param_plot, metric3

param = []
metric1 = []
metric2 = []
param_plot = []
metric3 = []


def observe_param_change(root):
    global param, metric1, metric2, param_plot, metric3

    def callback(*args):
        global param, metric1, metric2, param_plot, metric3
        param = []
        metric1 = []
        metric2 = []
        param_plot = []
        metric3 = []
        # wait 3 seconds before updating the plots
        create_plots()

    strTVISparam.trace_add("write", callback)
    intChannel.trace_add("write", callback)
    strTVISlocation.trace_add("write", callback)
    
    intPlotLen.trace_add("write", callback)

    intAnalysisLen.trace_add("write", callback)



def load_data():
    global param, metric1, metric2, param_plot, metric3

    location = strTVISlocation.get()
    TVIS_param = strTVISparam.get()
    channel = intChannel.get()

    # Get the list of folders in the selected location
    folders = [f for f in os.listdir(location) if os.path.isdir(os.path.join(location, f))]

    # Get the last modified datetime for each folder
    folder_dates = {folder: datetime.fromtimestamp(os.path.getmtime(os.path.join(location, folder))) for folder in folders}

    # Sort folders by their last modified datetime
    sorted_folders = sorted(folder_dates, key=folder_dates.get)

    # Initialize an empty DataFrame to concatenate data
    all_data = pd.DataFrame()
    cumulative_time = 0

    # Loop through each folder and load data from each channel*.csv file
    for folder in sorted_folders:
        file = f"{location}/{folder}/channel{channel}.dat"

        data = pd.read_csv(file, skiprows=9)
        data['Time'] = data['Time'] / 60  # Convert time to minutes
        
        # Adjust the time to be cumulative
        if not all_data.empty:
            data['Time'] += cumulative_time + 1
            data['Scan'] += all_data['Scan'].max()
        
        cumulative_time = data['Time'].iloc[-1]

        
        all_data = pd.concat([all_data, data], ignore_index=True)

    # Use the concatenated data for further processing
    data = all_data

    num_scans = len(data["Scan"].unique())

    print(f"Number of scans: {num_scans}")
    print(len(param))
    num = num_scans - len(param)
    print(num)

    if TVIS_param == 'Max_real':
        max_freq = data['Freq'].max()
        
        f_data = data[data['Freq'] == max_freq]
        param = list(f_data["C1'F"])

        
    elif TVIS_param == 'Min_real':
        min_freq = data['Freq'].min()
        
        f_data = data[data['Freq'] == min_freq]
        param = list(f_data["C1'F"])

    elif TVIS_param == 'C_img_Peak':
        x_peaks, y_peaks = find_peaks(data)
        param.extend(y_peaks)
    elif TVIS_param == 'log_F_peak':
        x_peaks, y_peaks = find_peaks(data)

        print(f"x_peaks dimensions: {np.array(x_peaks).shape}")
        print(f"y_peaks dimensions: {np.array(y_peaks).shape}")

        param.extend(x_peaks)

    print(len(param))
    print(len(data["Time"].unique()))
    print(len(data["Scan"].unique()))
    param_data = pd.DataFrame({"Time": data["Time"].unique(), "Scan": data["Scan"].unique(), "param": param})


    return param_data, num



def create_plots():
    global param, metric1, metric2, param_plot, metric3

    data, num = load_data()

    print("creating plots")

    metric1_new, metric2_new, param_plot_new, metric3_new = perform_analysis(data, num)



    metric1.extend(metric1_new)
    metric2.extend(metric2_new)
    #if len(param_plot_new) > 0:
    #    param_plot.extend(param_plot_new)
    metric3.extend(metric3_new)


    #param_plot_new = param_plot[-1]


    # Plot param
    fig1, ax = plt.subplots(figsize=(12, 4))
    ax.plot(data['Time'][len(data['Time']) - intPlotLen.get():], param[len(data['Time']) - intPlotLen.get():], label='Param')
    ax.plot(data['Time'][len(data['Time']) - len(param_plot_new):], param_plot_new, label='Linear Regression', linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('Param')
    plt.title('Param vs Time')
    plt.legend()

    plt.savefig("temp_saves/plot1.png")
    plt.close()

    """# Create the figure and axes
    fig, ax = plt.subplots(figsize=(12, 4), dpi=200)

    # Customize the grid and background
    ax.set_facecolor("#f9f9f9")  # Light grey background
    ax.grid(color="white", linestyle="--", linewidth=1, alpha=0.7)
    ax.set_axisbelow(True)  # Ensure gridlines are behind the plot

    # Plot the data
    ax.plot(data['Time'][len(data['Time']) - intPlotLen.get():], param[len(data['Time']) - intPlotLen.get():], color="#007ACC", linewidth=2, label="Spline Derivative", alpha=0.8)
    ax.plot(data['Time'][len(data['Time']) - len(param_plot_new):], param_plot_new, color="#FF5733", linewidth=2, label="Regression", alpha=0.8)


    # Add annotations
    ax.annotate(
        "Max Point", xy=(1.57, np.sin(1.57) * np.exp(-1.57 * 0.1)),
        xytext=(3, 0.8), arrowprops=dict(facecolor="#007ACC", arrowstyle="->"),
        fontsize=12, color="#333333"
    )


    # Customize axes
    ax.set_title("Spline Derivative vs Time", fontsize=18, weight="bold", pad=20)

    ax.set_xlabel("Time", fontsize=14, labelpad=15)
    ax.set_ylabel('d/dt Param', fontsize=14, labelpad=15)
    ax.tick_params(axis="both", which="major", labelsize=12, colors="#555555")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")

    # Add legend with customization
    legend = ax.legend(
        loc="upper right", fontsize=12, frameon=True, borderpad=1,
        edgecolor="#CCCCCC", facecolor="white", shadow=True
    )
    for text in legend.get_texts():
        text.set_color("#333333")

    # Add a watermark
    fig.text(0.95, 0.05, "© LyosenZ", fontsize=12, color="#CCCCCC",
            ha="right", va="bottom", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.savefig("temp_saves/plot1.png")
    """

    # Plot metric1
    fig, ax = plt.subplots(figsize=(8, 4))
    plt.plot(data['Time'][len(data['Time']) - intPlotLen.get():], metric1[len(data['Time']) - intPlotLen.get():], label='Spline Derivative')
    plt.xlabel('Time')
    plt.ylabel('d/dt Param')
    plt.title('Spline Derivative vs Time')
    plt.legend()

    plt.savefig("temp_saves/plot2.png")

    plt.close()

    # Plot metric2
    fig, ax = plt.subplots(figsize=(8, 4))
    plt.plot(data['Time'][len(data['Time']) - intPlotLen.get():], metric2[len(data['Time']) - intPlotLen.get():], label='Spline Second Derivative')
    plt.xlabel('Time')
    plt.ylabel('d^2/dt^2 Param')
    plt.title('Spline Second Derivative vs Time')
    plt.legend()

    plt.savefig("temp_saves/plot3.png")
    plt.close()


    # Plot metric3
    fig, ax = plt.subplots(figsize=(8, 4))
    display_data = data['Time'][len(data['Time']) - len(metric3):]
    plt.plot(display_data[len(display_data) - intPlotLen.get():], metric3[len(display_data) - intPlotLen.get():], label='Regression Error')
    plt.xlabel('Time')
    plt.ylabel('Error')
    plt.title('Error vs Time')
    plt.legend()

    plt.savefig("temp_saves/plot4.png")
    plt.close()




def perform_analysis(data, num):
    global param

    for analysis_type in ["spline", "regression"]:
        if analysis_type == "spline":
            d, d2 = spline_analysis(data, num)
        elif analysis_type == "regression":
            reg_plot, errors = regression_analysis(data, num)

    return d, d2, reg_plot, errors




def find_peaks(data):
    global param
    """Use a cubic spline to find the peak of the data."""

    y_peaks = []
    x_peaks = []

    print(len(param))

    for s in range(len(param), len(data["Scan"].unique())+1):

        data_slice = data[data["Scan"] == s]

        x = data_slice["Freq"]
        y = data_slice["param"]

        # Create a cubic spline
        peak_x, peak_y = peak(x, y)

        y_peaks.append(peak_y)
        x_peaks.append(peak_x)

        return x_peaks, y_peaks





def peak(freq, Z1):


        x = np.array(np.log10(freq))[::-1]
        y = np.array(Z1)


        # Create a cubic spline
        cs = CubicSpline(x, y, bc_type='natural')  # 'natural' cubic spline

        # Derivatives of the spline
        cs_derivative = cs.derivative()
        cs_second_derivative = cs.derivative(2)

        # Step 1: Find potential peak by minimizing the negative of the spline
        result = minimize_scalar(lambda x_val: -cs(x_val), bounds=(x.min(), x.max()), method='bounded')

        # Get the potential peak position and value
        peak_x = result.x
        peak_y = cs(peak_x)

        # Step 2: Check if it's a true local peak using derivative tests
        if x.min() < peak_x < x.max():  # Ensure the peak is not at the boundary
            slope = cs_derivative(peak_x)
            curvature = cs_second_derivative(peak_x)


            if np.isclose(slope, 0, atol=1e-3) and curvature < 0:
                return peak_y, peak_x
            else:
                return np.nan, np.nan
        else:
            np.nan, np.nan




def spline_analysis(data, num):
    global param

    if len(data)>len(metric1):

        derivatives = []
        second_derivatives = []

        x = data["Time"].values.reshape(-1, 1)[:,0]
        y = data["param"].values.reshape(-1, 1)[:,0]

        # Create a cubic spline
        cs = CubicSpline(x, y, bc_type='natural')

        # Derivatives of the spline
        cs_derivative = cs.derivative()
        cs_second_derivative = cs.derivative(2)

        val = data["Scan"].max() - num

        for s in data[data["Scan"] > val]["Scan"].unique():

            data_slice = data[(data["Scan"]) == s]

            t = data_slice["Time"].values[0]


            # Calculate the derivative and second derivative of the spline
            d = cs_derivative(t)
            d2 = cs_second_derivative(t)


            derivatives.append(d)
            second_derivatives.append(d2)

        return derivatives, second_derivatives
    else:
        return [], []





def regression_analysis(data, num):
    global param

    regression_error = []
    y_pred = []

    val = len(data['Scan'].unique()) - num


    print(len(data))
    print(num)
    print(val)


    for s in data[data["Scan"] > val-1]["Scan"].unique():
        
        data_slice = data[data["Scan"] <= s].tail(intAnalysisLen.get())

        if len(data_slice) < intAnalysisLen.get():
            continue

        x = data_slice["Time"].values.reshape(-1, 1)
        y = data_slice["param"].values.reshape(-1, 1)


        model = LinearRegression()
        model.fit(x, y)

        y_pred = model.predict(x)
        if s != data["Scan"].unique()[-1]:
            error = mean_squared_error(y, y_pred)
            regression_error.append(error)

    return y_pred, regression_error











