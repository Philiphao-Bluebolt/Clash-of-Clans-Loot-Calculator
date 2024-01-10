#### Clash of Clans Lootable Resource Calculator ####
### 2023/07/03 (Verified)

""" Abbreviation --------------------------------------
g = Gold; e = Elixir; d_e = Dark Elixir
st = Storage; cl = Collector; tr = Treasury
t_h = TH = Town Hall
cap = capacity; num = number; lvl = level
"""

### Packages Import -----------------------------------

from tkinter import *
import xlrd
import numpy as np
from matplotlib import pyplot as plt
from prettytable import PrettyTable

### Parameters ----------------------------------------

# Display Settings
DATA_PLOT = True
NOW_PLOT = True

# Town Hall Level and Difference
town_hall_level = 1
town_hall_level_lower = 0

# Storage Resource Value
gold_storage_now = 0
elixir_storage_now = 0
dark_elixir_storage_now = 0

# SINGLE Collector Resource Value
# (Assume level equals and max amount)
gold_collector_now_single = 0
elixir_collector_now_single = 0
dark_elixir_collector_now_single = 0

# Treasury Resource Value
gold_treasury_now = 0
elixir_treasury_now = 0
dark_elixir_treasury_now = 0

# Lootable Storage Resource
lootable_storage_gold = 0
lootable_storage_elixir = 0
lootable_storage_dark_elixir = 0

# Lootable Collector Resource (Total)
lootable_collector_gold = 0
lootable_collector_elixir = 0
lootable_collector_dark_elixir = 0

# Lootable Treasury Resource
lootable_treasury_gold = 0
lootable_treasury_elixir = 0
lootable_treasury_dark_elixir = 0

# Lootable Resource in total
lootable_gold_total = 0
lootable_elixir_total = 0
lootable_dark_elixir_total = 0

### Data -----------------------------------------------

## Import Excel
data_set = xlrd.open_workbook(r'coc_resource_building_data.xlsx')

### Function -------------------------------------------

## str --> float
def str_to_float(input_str):
    if isinstance(input_str, float) is True or isinstance(input_str, int) is True:
        return input_str

    good_str = ""
    for i in range(len(input_str)):
        if input_str[i] == "," or input_str[i] == "*":
            continue
        if input_str[i] == "%":
            return float(good_str) * 0.01
        else:
            good_str += input_str[i]
    return float(good_str)


## Calculate Storage Maximum Capacity for one resource
def storage_capacity_sum(town_hall_level, resource):
    if resource == "dark_elixir":
        if town_hall_level < 7: #No Dark Elixir for TH < 7
            return 0
        else:
            storage_number_sheet = data_set.sheet_by_name("dark_elixir_storage_number")
            storage_level_sheet = data_set.sheet_by_name("dark_elixir_storage")
            i = 10
            town_hall_capacity_sheet_column = 3 #Select certain column

    elif resource == "gold" or resource == "elixir":
        storage_number_sheet = data_set.sheet_by_name("elixir_storage_number")
        storage_level_sheet = data_set.sheet_by_name("elixir_storage")
        i = 16
        town_hall_capacity_sheet_column = 2

    storage_number = storage_number_sheet.cell_value(1, town_hall_level)

    while i > 0:
        if storage_level_sheet.cell_value(i, 6) <= town_hall_level: #Use less or equal in case the storage cannot be upgraded on this TH lvl
            storage_capacity = storage_level_sheet.cell_value(i, 1) * storage_number
            break
        else:
            i -= 1

    if town_hall_level > 10: #Same cell shared for TH > 10
        town_hall_capacity = str_to_float(data_set.sheet_by_name("town_hall_capacity").cell_value(12, town_hall_capacity_sheet_column))
    else:
        town_hall_capacity = str_to_float(data_set.sheet_by_name("town_hall_capacity").cell_value(town_hall_level + 1, town_hall_capacity_sheet_column))

    return town_hall_capacity + storage_capacity


## Get Storage Lootable Limit
def loot_storage_limit(town_hall_level, resource):
    if resource == "dark_elixir":
        if town_hall_level < 7: #No Dark Elixir for TH < 7
            return 0
        else:
            return str_to_float(data_set.sheet_by_name("dark_elixir_storage_loot").cell_value(town_hall_level - 6, 2))

    elif resource == "gold" or resource == "elixir":
        if town_hall_level < 6: #TH 5/6 share same cell
            return str_to_float(data_set.sheet_by_name("elixir_storage_loot").cell_value(town_hall_level, 2))
        else:
            return str_to_float(data_set.sheet_by_name("elixir_storage_loot").cell_value(town_hall_level - 1, 2))


## Get Treasury Maximum Capacity for one resource (which is also the Lootable limit)
def treasury_capacity(town_hall_level, resource):
    if resource == "dark_elixir":
        if town_hall_level < 7: #No Dark Elixir for TH < 7
            return 0
        else:
            return str_to_float(data_set.sheet_by_name("treasury_loot").cell_value(town_hall_level - 2, 5))

    elif resource == "gold" or resource == "elixir":
        if town_hall_level < 3: #No Treasury for TH < 3
            return 0
        else:
            return str_to_float(data_set.sheet_by_name("treasury_loot").cell_value(town_hall_level - 2, 3))


## Get Collector Maximum Capacity for one resource (which is also the Lootable limit)
def collector_capacity(town_hall_level, resource):
    if resource == "dark_elixir":
        if town_hall_level < 7: #No Dark Elixir for TH < 7
            return 0
        elif town_hall_level > 11:
            return data_set.sheet_by_name("dark_elixir_drill_loot").cell_value(6, 3)
        else:
            return data_set.sheet_by_name("dark_elixir_drill_loot").cell_value(town_hall_level - 6, 3)

    elif resource == "gold" or resource == "elixir":
        if town_hall_level > 11:
            return data_set.sheet_by_name("elixir_collector_loot").cell_value(12, 3)
        else:
            return data_set.sheet_by_name("elixir_collector_loot").cell_value(town_hall_level, 3)


## Get Single Collector Maximum Capacity for one resource (Use in current mode)
def collector_single_capacity(town_hall_level, resource):
    if resource == "dark_elixir":
        if town_hall_level < 7: #No Dark Elixir for TH < 7
            return 0
        else:
            collector_sheet = data_set.sheet_by_name("dark_elixir_drill")
            i = 9
    elif resource == "gold" or resource == "elixir":
        collector_sheet = data_set.sheet_by_name("elixir_collector")
        i = 15

    while i > 0:
        if collector_sheet.cell_value(i, 10) <= town_hall_level: #Use less or equal in case the storage cannot be upgraded on this TH lvl
            return collector_sheet.cell_value(i, 1)
        else:
            i -= 1


## Get Collector Number for every TH
def collector_number(town_hall_level, resource):
    if resource == "dark_elixir":
        return data_set.sheet_by_name("dark_elixir_drill_number").cell_value(1, town_hall_level)
    elif resource == "gold" or resource == "elixir":
        return data_set.sheet_by_name("elixir_collector_number").cell_value(1, town_hall_level)


## Get Lootable Percentage
def loot_percentage(town_hall_level, loot_from, resource):
    if loot_from == "storage":
        if resource == "dark_elixir":
            if town_hall_level < 7: #No Dark Elixir for TH < 7
                return 0
            else:
                return str_to_float(data_set.sheet_by_name("dark_elixir_storage_loot").cell_value(town_hall_level - 6, 1))
        elif resource == "gold" or resource == "elixir":
            if town_hall_level < 6: #TH 5/6 share same cell
                return str_to_float(data_set.sheet_by_name("elixir_storage_loot").cell_value(town_hall_level, 1))
            else:
                return str_to_float(data_set.sheet_by_name("elixir_storage_loot").cell_value(town_hall_level - 1, 1))

    elif loot_from == "collector":
        if resource == "dark_elixir":
            if town_hall_level < 7: #No Dark Elixir for TH < 7
                return 0
            else:
                return 0.75
        elif resource == "gold" or resource == "elixir":
            return 0.5

    elif loot_from == "treasury":
        return 0.03


## Town Hall Level Penalty
def penalty(town_hall_level_lower_):
    if town_hall_level_lower_ > 4:
        return data_set.sheet_by_name("town_hall_level_penalty").cell_value(5, 1) # > 4 lvls lower
    else:
        return data_set.sheet_by_name("town_hall_level_penalty").cell_value(town_hall_level_lower_ + 1, 1)


## Saturation Function
def saturation(x, k, b):
    if x*k <= b:
        return x*k
    else:
        return b
saturation_elementwise = np.frompyfunc(saturation, 3, 1)


## The "Resource Value - Lootable Value" Plotting Function
def lootable_curve(town_hall_level, loot_from, resource):
    if resource == "dark_elixir":
        x_step = 10
    elif resource == "gold" or resource == "elixir":
        x_step = 100

    if loot_from == "storage":
        loot_limit = loot_storage_limit(town_hall_level, resource)
        x_value = np.arange(0, storage_capacity_sum(town_hall_level, resource), x_step)

    elif loot_from == "collector":
        loot_limit = collector_capacity(town_hall_level, resource)
        x_value = np.arange(0, loot_limit, x_step)

    elif loot_from == "treasury":
        loot_limit = treasury_capacity(town_hall_level, resource)
        x_value = np.arange(0, loot_limit, x_step)

    percentage = loot_percentage(town_hall_level, loot_from, resource)

    y_lootable = saturation_elementwise(x_value, percentage, loot_limit)
    if loot_from != "treasury":
        y_lootable *= penalty(town_hall_level_lower)

    plt.plot(x_value, y_lootable, label = "TH lvl " + str(town_hall_level))


## Current Lootable Resource Function
def lootable_current(town_hall_level, loot_from, resource, x_current_value, if_plot):
    if loot_from == "storage":
        loot_limit = loot_storage_limit(town_hall_level, resource)

    elif loot_from == "collector":
        loot_limit = collector_capacity(town_hall_level, resource)
        # Calculate Total Resource in collectors
        x_current_value = x_current_value * collector_number(town_hall_level, resource)

    elif loot_from == "treasury":
        loot_limit = treasury_capacity(town_hall_level, resource)

    percentage = loot_percentage(town_hall_level, loot_from, resource)

    y_current_lootable = saturation(x_current_value, percentage, loot_limit)
    if loot_from != "treasury":
        y_current_lootable *= penalty(town_hall_level_lower)

    if if_plot is True:
        if resource == "dark_elixir":
            plt.plot(x_current_value, y_current_lootable, color = "black", marker = "8", markersize = 10, label = resource)
        elif resource == "elixir":
            plt.plot(x_current_value, y_current_lootable, color = "magenta", marker = "H", markersize = 10, label = resource)
        elif resource == "gold":
            plt.plot(x_current_value, y_current_lootable, color = "blue", marker = "D", markersize = 10, label = resource)
    return y_current_lootable


## Get Input Town Hall Level from GUI
def get_input_town_hall_level():

    global town_hall_level
    global town_hall_level_lower
    town_hall_level = town_hall_level_scale.get()
    town_hall_level_lower = town_hall_level_lower_scale.get()

## Get Input Resource Value from GUI
def get_input_resource_value():

    # Storage Resource Value
    global gold_storage_now
    global elixir_storage_now
    global dark_elixir_storage_now
    gold_storage_now = storage_gold_scale.get()
    elixir_storage_now = storage_elixir_scale.get()
    dark_elixir_storage_now = storage_dark_elixir_scale.get()

    # SINGLE Collector Resource Value
    # (Assume level equals and max amount)
    global gold_collector_now_single
    global elixir_collector_now_single
    global dark_elixir_collector_now_single
    gold_collector_now_single = collector_gold_scale.get()
    elixir_collector_now_single = collector_elixir_scale.get()
    dark_elixir_collector_now_single = collector_dark_elixir_scale.get()

    # Treasury Resource Value
    global gold_treasury_now
    global elixir_treasury_now
    global dark_elixir_treasury_now
    gold_treasury_now = treasury_gold_scale.get()
    elixir_treasury_now = treasury_elixir_scale.get()
    dark_elixir_treasury_now = treasury_dark_elixir_scale.get()


## Update Resource Input Maximum
def callback_update_input_max(event):
    get_input_town_hall_level()

    global town_hall_level

    storage_gold_scale.config(to = storage_capacity_sum(town_hall_level, "gold"))
    storage_elixir_scale.config(to = storage_capacity_sum(town_hall_level, "elixir"))
    storage_dark_elixir_scale.config(to = storage_capacity_sum(town_hall_level, "dark_elixir"))

    collector_gold_scale.config(to = collector_single_capacity(town_hall_level, "gold"))
    collector_elixir_scale.config(to = collector_single_capacity(town_hall_level, "elixir"))
    collector_dark_elixir_scale.config(to = collector_single_capacity(town_hall_level, "dark_elixir"))

    treasury_gold_scale.config(to = treasury_capacity(town_hall_level, "gold"))
    treasury_elixir_scale.config(to = treasury_capacity(town_hall_level, "elixir"))
    treasury_dark_elixir_scale.config(to = treasury_capacity(town_hall_level, "dark_elixir"))

    scale_color_town_hall_level_list = ["#f9c648", "#f9c648", "#f9c648", "#f9c648", "#f9c648",\
                                        "#9fb253", "#9fb253", "#9fb253",\
                                        "#113250", "#d11010", "#f1f3f4", "#0696f4",\
                                        "#94ecf9", "#a7d510", "#652791"]
    town_hall_level_scale.config(troughcolor = scale_color_town_hall_level_list[town_hall_level - 1])

    callback_update_loot_display(event)


## Update Loot Display
def callback_update_loot_display(event):
    get_input_resource_value()

    global lootable_storage_gold
    lootable_storage_gold = lootable_current(town_hall_level, "storage", "gold", gold_storage_now, False)
    storage_gold_lootable_label.config(text = str(int(lootable_storage_gold)))
    global lootable_storage_elixir
    lootable_storage_elixir = lootable_current(town_hall_level, "storage", "elixir", elixir_storage_now, False)
    storage_elixir_lootable_label.config(text = str(int(lootable_storage_elixir)))
    global lootable_storage_dark_elixir
    lootable_storage_dark_elixir = lootable_current(town_hall_level, "storage", "dark_elixir", dark_elixir_storage_now, False)
    storage_dark_elixir_lootable_label.config(text = str(int(lootable_storage_dark_elixir)))

    global lootable_collector_gold
    lootable_collector_gold = lootable_current(town_hall_level, "collector", "gold", gold_collector_now_single, False)
    collector_gold_lootable_label.config(text = str(int(lootable_collector_gold)))
    global lootable_collector_elixir
    lootable_collector_elixir = lootable_current(town_hall_level, "collector", "elixir", elixir_collector_now_single, False)
    collector_elixir_lootable_label.config(text = str(int(lootable_collector_elixir)))
    global lootable_collector_dark_elixir
    lootable_collector_dark_elixir = lootable_current(town_hall_level, "collector", "dark_elixir", dark_elixir_collector_now_single, False)
    collector_dark_elixir_lootable_label.config(text = str(int(lootable_collector_dark_elixir)))

    global lootable_treasury_gold
    lootable_treasury_gold = lootable_current(town_hall_level, "treasury", "gold", gold_treasury_now, False)
    treasury_gold_lootable_label.config(text = str(int(lootable_treasury_gold)))
    global lootable_treasury_elixir
    lootable_treasury_elixir = lootable_current(town_hall_level, "treasury", "elixir", elixir_treasury_now, False)
    treasury_elixir_lootable_label.config(text = str(int(lootable_treasury_elixir)))
    global lootable_treasury_dark_elixir
    lootable_treasury_dark_elixir = lootable_current(town_hall_level, "treasury", "dark_elixir", dark_elixir_treasury_now, False)
    treasury_dark_elixir_lootable_label.config(text = str(int(lootable_treasury_dark_elixir)))

    global lootable_gold_total
    lootable_gold_total = int(lootable_storage_gold + lootable_collector_gold + lootable_treasury_gold)
    total_gold_lootable_label.config(text = str(lootable_gold_total))
    global lootable_elixir_total
    lootable_elixir_total = int(lootable_storage_elixir + lootable_collector_elixir + lootable_treasury_elixir)
    total_elixir_lootable_label.config(text = str(lootable_elixir_total))
    global lootable_dark_elixir_total
    lootable_dark_elixir_total = int(lootable_storage_dark_elixir + lootable_collector_dark_elixir + lootable_treasury_dark_elixir)
    total_dark_elixir_lootable_label.config(text = str(lootable_dark_elixir_total))


### GUI---------------------------------------------------

root = Tk()
root.title("Clash of Clans Loot Calculator")
root.iconbitmap("loot_cart_logo.ico")
root.geometry("1200x780")
root.resizable(False, False)

## Title
title_label = Label(root,
                    text = "Clash of Clans Loot Calculator",
                    relief = "raised",
                    font = ("Times New Roman", 20),
                    padx = 150,
                    pady = 20)
title_label.pack()


## Town Hall Level Frame

# Define the scales Trigger Event and Color
update_event_town_hall = "<ButtonRelease-1>"

town_hall_level_frame = LabelFrame(root,
                        text = "Town Hall Settings")
town_hall_level_frame.pack(fill = "x", padx = 4, pady = 14)

town_hall_level_scale = Scale(town_hall_level_frame,
                        label = "Town Hall Level",
                        orient = "horizontal",
                        length = 500,
                        width = 30,
                        from_ = 1,
                        to = 15,
                        resolution = 1,
                        showvalue = False,
                        troughcolor = "#f9c648",
                        tickinterval = True)
town_hall_level_scale.pack(side = "left", padx = 40)
town_hall_level_scale.bind(update_event_town_hall, callback_update_input_max)

town_hall_level_lower_scale = Scale(town_hall_level_frame,
                        label = "Town Hall Level Lower",
                        orient = "horizontal",
                        length = 500,
                        width = 30,
                        from_ = 0,
                        to = 14,
                        resolution = 1,
                        showvalue = False,
                        tickinterval = True)
town_hall_level_lower_scale.pack(side = "right", padx = 40)
town_hall_level_lower_scale.bind(update_event_town_hall, callback_update_input_max)

## Current Resource Input Frame

# Define the scales Trigger Event and Color
update_event_resource_value = "<ButtonRelease-1>"
scale_color_gold = "#FFD700"
scale_color_elixir = "#FF00FF"
scale_color_dark_elixir = "#1C1C1C"

current_resource_input_frame = LabelFrame(root,
                                          text = "Resource")
current_resource_input_frame.pack(fill = "x", padx = 4, pady = 20)

resource_input_left_padx = 10
resource_input_up_pady = 5
resource_input_padx = 50
resource_input_pady = 10
resource_input_label_relief = "flat"

resource_input_scale_length = 260
resource_input_scale_width = 20

empty_label = Label(current_resource_input_frame,
                    text = "      ",
                    relief = resource_input_label_relief)
empty_label.grid(row = 0, column = 0, padx = resource_input_left_padx, pady = resource_input_up_pady)
gold_label = Label(current_resource_input_frame,
                    text = "Gold",
                    relief = resource_input_label_relief)
gold_label.grid(row = 0, column = 1, padx = resource_input_padx, pady = resource_input_up_pady)
elixir_label = Label(current_resource_input_frame,
                    text = "Elixir",
                    relief = resource_input_label_relief)
elixir_label.grid(row = 0, column = 2, padx = resource_input_padx, pady = resource_input_up_pady)
dark_elixir_label = Label(current_resource_input_frame,
                    text = "Dark Elixir",
                    relief = resource_input_label_relief)
dark_elixir_label.grid(row = 0, column = 3, padx = resource_input_padx, pady = resource_input_up_pady)

storage_label = Label(current_resource_input_frame,
                      text = "Storage",
                      relief = resource_input_label_relief)
storage_label.grid(row = 1, column = 0, padx = resource_input_left_padx, pady = resource_input_pady)
collector_label = Label(current_resource_input_frame,
                      text = "Collector",
                      relief = resource_input_label_relief)
collector_label.grid(row = 2, column = 0, padx = resource_input_left_padx, pady = resource_input_pady)
treasury_label = Label(current_resource_input_frame,
                      text = "Treasury",
                      relief = resource_input_label_relief)
treasury_label.grid(row = 3, column = 0, padx = resource_input_left_padx, pady = resource_input_pady)


storage_gold_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 1500,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_gold,
                        tickinterval = False)
storage_gold_scale.grid(row = 1, column = 1, padx = resource_input_padx, pady = resource_input_pady)
storage_gold_scale.bind(update_event_resource_value, callback_update_loot_display)

storage_elixir_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 1500,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_elixir,
                        tickinterval = False)
storage_elixir_scale.grid(row = 1, column = 2, padx = resource_input_padx, pady = resource_input_pady)
storage_elixir_scale.bind(update_event_resource_value, callback_update_loot_display)

storage_dark_elixir_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 0,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_dark_elixir,
                        tickinterval = False)
storage_dark_elixir_scale.grid(row = 1, column = 3, padx = resource_input_padx, pady = resource_input_pady)
storage_dark_elixir_scale.bind(update_event_resource_value, callback_update_loot_display)

collector_gold_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 1000,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_gold,
                        tickinterval = False)
collector_gold_scale.grid(row = 2, column = 1, padx = resource_input_padx, pady = resource_input_pady)
collector_gold_scale.bind(update_event_resource_value, callback_update_loot_display)

collector_elixir_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 1000,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_elixir,
                        tickinterval = False)
collector_elixir_scale.grid(row = 2, column = 2, padx = resource_input_padx, pady = resource_input_pady)
collector_elixir_scale.bind(update_event_resource_value, callback_update_loot_display)

collector_dark_elixir_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 0,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_dark_elixir,
                        tickinterval = False)
collector_dark_elixir_scale.grid(row = 2, column = 3, padx = resource_input_padx, pady = resource_input_pady)
collector_dark_elixir_scale.bind(update_event_resource_value, callback_update_loot_display)

treasury_gold_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 75000,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_gold,
                        tickinterval = False)
treasury_gold_scale.grid(row = 3, column = 1, padx = resource_input_padx, pady = resource_input_pady)
treasury_gold_scale.bind(update_event_resource_value, callback_update_loot_display)

treasury_elixir_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 75000,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_elixir,
                        tickinterval = False)
treasury_elixir_scale.grid(row = 3, column = 2, padx = resource_input_padx, pady = resource_input_pady)
treasury_elixir_scale.bind(update_event_resource_value, callback_update_loot_display)

treasury_dark_elixir_scale = Scale(current_resource_input_frame,
                        orient = "horizontal",
                        length = resource_input_scale_length,
                        width = resource_input_scale_width,
                        from_ = 0,
                        to = 0,
                        resolution = 1,
                        showvalue = True,
                        troughcolor = scale_color_dark_elixir,
                        tickinterval = False)
treasury_dark_elixir_scale.grid(row = 3, column = 3, padx = resource_input_padx, pady = resource_input_pady)
treasury_dark_elixir_scale.bind(update_event_resource_value, callback_update_loot_display)


## Loot Display Frame
loot_display_frame = LabelFrame(root,
                                text = "Loot")
loot_display_frame.pack(fill = "x", padx = 4, pady = 14)

loot_display_left_padx = 10
loot_display_up_pady = 5
loot_display_padx = 164
loot_display_pady = 12
loot_display_label_relief = "flat"
loot_display_value_label_relief = "flat"

empty_label = Label(loot_display_frame,
                    text = "      ",
                    relief = loot_display_label_relief)
empty_label.grid(row = 0, column = 0, padx = loot_display_left_padx, pady = loot_display_up_pady)
storage_label = Label(loot_display_frame,
                      text = "Storage",
                      relief = loot_display_label_relief)
storage_label.grid(row = 1, column = 0, padx = loot_display_left_padx, pady = loot_display_pady)
collector_label = Label(loot_display_frame,
                      text = "Collector",
                      relief = loot_display_label_relief)
collector_label.grid(row = 2, column = 0, padx = loot_display_left_padx, pady = loot_display_pady)
treasury_label = Label(loot_display_frame,
                      text = "Treasury",
                      relief = loot_display_label_relief)
treasury_label.grid(row = 3, column = 0, padx = loot_display_left_padx, pady = loot_display_pady)
total_label = Label(loot_display_frame,
                      text = "Total",
                      relief = loot_display_label_relief)
total_label.grid(row = 4, column = 0, padx = loot_display_left_padx, pady = loot_display_pady)
gold_lootable_label = Label(loot_display_frame,
                    text = "Gold",
                    relief = loot_display_label_relief)
gold_lootable_label.grid(row = 0, column = 1, padx = loot_display_padx, pady = loot_display_up_pady)
elixir_lootable_label = Label(loot_display_frame,
                    text = "Elixir",
                    relief = loot_display_label_relief)
elixir_lootable_label.grid(row = 0, column = 2, padx = loot_display_padx, pady = loot_display_up_pady)
dark_elixir_lootable_label = Label(loot_display_frame,
                    text = "Dark Elixir",
                    relief = loot_display_label_relief)
dark_elixir_lootable_label.grid(row = 0, column = 3, padx = loot_display_padx, pady = loot_display_up_pady)

storage_gold_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
storage_gold_lootable_label.grid(row = 1, column = 1, padx = loot_display_padx, pady = loot_display_pady)
storage_elixir_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
storage_elixir_lootable_label.grid(row = 1, column = 2, padx = loot_display_padx, pady = loot_display_pady)
storage_dark_elixir_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
storage_dark_elixir_lootable_label.grid(row = 1, column = 3, padx = loot_display_padx, pady = loot_display_pady)

collector_gold_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
collector_gold_lootable_label.grid(row = 2, column = 1, padx = loot_display_padx, pady = loot_display_pady)
collector_elixir_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
collector_elixir_lootable_label.grid(row = 2, column = 2, padx = loot_display_padx, pady = loot_display_pady)
collector_dark_elixir_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
collector_dark_elixir_lootable_label.grid(row = 2, column = 3, padx = loot_display_padx, pady = loot_display_pady)

treasury_gold_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
treasury_gold_lootable_label.grid(row = 3, column = 1, padx = loot_display_padx, pady = loot_display_pady)
treasury_elixir_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
treasury_elixir_lootable_label.grid(row = 3, column = 2, padx = loot_display_padx, pady = loot_display_pady)
treasury_dark_elixir_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
treasury_dark_elixir_lootable_label.grid(row = 3, column = 3, padx = loot_display_padx, pady = loot_display_pady)

total_gold_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
total_gold_lootable_label.grid(row = 4, column = 1, padx = loot_display_padx, pady = loot_display_pady)
total_elixir_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
total_elixir_lootable_label.grid(row = 4, column = 2, padx = loot_display_padx, pady = loot_display_pady)
total_dark_elixir_lootable_label = Label(loot_display_frame,
                                    text = "0",
                                    relief = loot_display_value_label_relief)
total_dark_elixir_lootable_label.grid(row = 4, column = 3, padx = loot_display_padx, pady = loot_display_pady)


root.mainloop()


### Plot -------------------------------------------

plt.figure("Storage Lootable Resource")
plt.subplot(121)
for i in range(15, 0, -1):
    lootable_curve(i, "storage", "elixir")
lootable_storage_elixir = lootable_current(town_hall_level, "storage", "elixir", elixir_storage_now, NOW_PLOT)
lootable_storage_gold = lootable_current(town_hall_level, "storage", "gold", gold_storage_now, NOW_PLOT)
plt.legend(prop = {'size':10}, loc = "lower right")
plt.title("Lootable Gold / Elixir in Storage")
plt.xlabel("Current Gold / Elixir")
plt.ylabel("Lootable Gold / Elixir")
plt.grid()

plt.subplot(122)
for i in range(15, 6, -1):
    lootable_curve(i, "storage", "dark_elixir")
lootable_storage_dark_elixir = lootable_current(town_hall_level, "storage", "dark_elixir", dark_elixir_storage_now, NOW_PLOT)
plt.legend(prop = {'size':10}, loc = "lower right")
plt.title("Lootable Dark Elixir in Storage")
plt.xlabel("Current Dark Elixir")
plt.ylabel("Lootable Dark Elixir")
plt.grid()

plt.figure("Collector Lootable Resource")
plt.subplot(121)
for i in range(15, 0, -1):
    lootable_curve(i, "collector", "elixir")
lootable_collector_elixir = lootable_current(town_hall_level, "collector", "elixir", elixir_collector_now_single, NOW_PLOT)
lootable_collector_gold = lootable_current(town_hall_level, "collector", "gold", gold_collector_now_single, NOW_PLOT)
plt.legend(prop = {'size':10}, loc = "lower right")
plt.title("Lootable Gold / Elixir in Mines / Collectors")
plt.xlabel("Current Gold / Elixir")
plt.ylabel("Lootable Gold / Elixir")
plt.grid()

plt.subplot(122)
for i in range(15, 6, -1):
    lootable_curve(i, "collector", "dark_elixir")
lootable_collector_dark_elixir = lootable_current(town_hall_level, "collector", "dark_elixir", dark_elixir_collector_now_single, NOW_PLOT)
plt.legend(prop = {'size':10}, loc = "lower right")
plt.title("Lootable Dark Elixir in Drills")
plt.xlabel("Current Dark Elixir")
plt.ylabel("Lootable Dark Elixir")
plt.grid()

plt.figure("Treasury Lootable Resource")
plt.subplot(121)
for i in range(15, 0, -1):
    lootable_curve(i, "treasury", "elixir")
lootable_treasury_elixir = lootable_current(town_hall_level, "treasury", "elixir", elixir_treasury_now, NOW_PLOT)
lootable_treasury_gold = lootable_current(town_hall_level, "treasury", "gold", gold_treasury_now, NOW_PLOT)
plt.legend(prop = {'size':10}, loc = "lower right")
plt.title("Lootable Gold / Elixir in Treasury")
plt.xlabel("Current Gold / Elixir")
plt.ylabel("Lootable Gold / Elixir")
plt.grid()

plt.subplot(122)
for i in range(15, 6, -1):
    lootable_curve(i, "treasury", "dark_elixir")
lootable_treasury_dark_elixir = lootable_current(town_hall_level, "treasury", "dark_elixir", dark_elixir_treasury_now, NOW_PLOT)
plt.legend(prop = {'size':10}, loc = "lower right")
plt.title("Lootable Dark Elixir in Treasury")
plt.xlabel("Current Dark Elixir")
plt.ylabel("Lootable Dark Elixir")
plt.grid()

## Display your current lootable resource in terminal
output_table = PrettyTable()
output_table.title = "Lootable Analysis Table"
output_table.field_names = [" ", "Gold", "Elixir", "Dark Elixir"]
output_table.add_row(["Storage", lootable_storage_gold, lootable_storage_elixir, lootable_storage_dark_elixir])
output_table.add_row(["Collector", lootable_collector_gold, lootable_collector_elixir, lootable_collector_dark_elixir])
output_table.add_row(["Treasury", lootable_treasury_gold, lootable_treasury_elixir, lootable_treasury_dark_elixir])
output_table.add_row(["Total"\
                       , lootable_storage_gold + lootable_collector_gold + lootable_treasury_gold\
                       , lootable_storage_elixir + lootable_collector_elixir + lootable_treasury_elixir\
                       , lootable_storage_dark_elixir + lootable_collector_dark_elixir + lootable_treasury_dark_elixir])

print(output_table)

## Plot Data
if DATA_PLOT is True:
    plt.show()