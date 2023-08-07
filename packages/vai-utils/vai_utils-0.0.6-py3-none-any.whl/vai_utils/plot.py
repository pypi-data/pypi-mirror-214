import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap
from PIL import Image
import random
import seaborn as sns
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.ticker as ticker

colors =["#1D2026","#393939","#666666","#BDBDBD","#E0E0E0","#F2F2F2","#FD93B1","#FC2964","#FEC9D8","#FD5F8B","#0095FF","#E6F5FF","#5C33F6","#8566F8",]

def bar_chart( categories, series, **optional_params):
    fig, ax = plt.subplots()
    bar_labels =[]
    if('bar_labels' in optional_params):
        bar_labels = optional_params['bar_labels']
    else:
        for i in range(0, len(categories)+ 1,1):
            bar_labels.append(i)
    colors=["#1D2026","#FC2964","#0095FF","#5C33F6","#393939","#FD93B1","#E6F5FF","#8566F8","#666666","#FEC9D8","#BDBDBD","#FD5F8B","#E0E0E0","#F2F2F2"]
    bar_colors =[]
    if('bar_colors' in optional_params):
        bar_colors = optional_params['bar_colors']
    else:
        for i in range(0, len(categories)+ 1,1):
            if(i <= len(colors) -1):
                bar_colors.append(colors[i])
    data = series
    data = list(map(lambda a, i: {'index': i, 'value': a}, data, range(len(data))))
    indexes = sorted(data, key=lambda x: x['value'])
    indexes = [a['index'] for a in indexes]
    values = [a['value'] for a in sorted(data, key=lambda x: x['value'])]
    cat = []
    labels =[]
    colors = []
    for d in indexes:
        cat.append(categories[d])
        labels.append(bar_labels[d])
        colors.append(bar_colors[d])
    ax.barh(cat, values,label=labels ,color=colors)
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png')
    print("Image saved: ", str(name) + '.png')
    im.show() 
  

def column_chart( categories, series, **optional_params):
    fig, ax = plt.subplots()
    bar_labels =[]
    if('bar_labels' in optional_params):
        bar_labels = optional_params['bar_labels']
    else:
        for i in range(0, len(categories)+ 1,1):
            bar_labels.append(i)

    colors=["#1D2026","#FC2964","#0095FF","#5C33F6","#393939","#FD93B1","#E6F5FF","#8566F8","#666666","#FEC9D8","#BDBDBD","#FD5F8B","#E0E0E0","#F2F2F2"]
    bar_colors =[]
    if('bar_colors' in optional_params):
        bar_colors = optional_params['bar_colors']
    else:
        for i in range(0, len(categories)+ 1,1):
            if(i <= len(colors) -1):
                bar_colors.append(colors[i])
    ax.bar(categories, series,label=bar_labels ,color=bar_colors)
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show() 
  
  

def stack_bar( categories, below,above, **optional_params):
    species = categories
    weight_counts = {
        "Below": np.array(below),
        "Above": np.array(above),
    }
    width = 0.5
    fig, ax = plt.subplots()
    bottom = np.zeros(3)
    index= 0
    color=["#0095FF","#E6F5FF"]
    if ('color' in optional_params):
        color= (optional_params['color'])
    for boolean, weight_count in weight_counts.items():
        p = ax.bar(species, weight_count, width, color = color[index], label=boolean, bottom=bottom)
        index = index+1
        bottom += weight_count
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show() 
  

def line_graph(categories, data, label,**optional_params):
    fig, ax = plt.subplots()
    colors=["#1D2026","#FC2964","#0095FF","#5C33F6","#393939","#FD93B1","#E6F5FF","#8566F8","#666666","#FEC9D8","#BDBDBD","#FD5F8B","#E0E0E0","#F2F2F2"]
    color = colors
    if ('color' in optional_params):
        color =(optional_params['color'])
    for i in range(0, len(data)):
        print(label[i])
        ax.plot(categories,data[i],color=  color[i] if i<len(color) else  colors[i], label=label[i])
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    ax.legend()
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show() 
  
def heat_graph( data,  **optional_params):
    fig, ax = plt.subplots()
    data= np.array(data)
    color = colors[0]
    if ('color' in optional_params):
        color =(optional_params['color'])
    cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', [color, color])
    sns.heatmap(data, annot=True, cmap=cmap, alpha=data)
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()                  
    
def histogram_graph(data , bins ,**optional_params):
    fig, ax = plt.subplots()
    color = colors[10]
    if ('color' in optional_params):
        color =(optional_params['color'])
    plt.hist(data, bins, alpha=0.7, edgecolor='black',color=color)
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    values, counts = np.unique(data, return_counts=True)
    plot_color = colors[9]
    if ('plot_color' in optional_params):
        plot_color =(optional_params['plot_color'])
    plt.plot(values, counts, 'bo', markersize=8, color= plot_color)
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()        
  

# def waterfall_graph(categories,values ,   **optional_params):
#     fig, ax = plt.subplots()
#     cumulative_values = [sum(values[:i+1]) for i in range(len(values))]
#     color = colors[0]
#     if ('color' in optional_params):
#         color =(optional_params['color'])
#     plt.bar(categories, values, color=color, align='center', width=0.5)
#     plt.plot(categories, cumulative_values, marker='o', color=color, linestyle='--')
#     if ('xlabel' in optional_params):
#         ax.set_xlabel(optional_params['xlabel'])
#     if ('ylabel' in optional_params):
#         ax.set_ylabel(optional_params['ylabel'])
#     if ('title' in optional_params):
#         ax.set_title(optional_params['title'])
#     if ('legend' in optional_params):
#         ax.legend(title=optional_params['legend'])
#     name = random.random()
#     plt.savefig(str(name) + '.png')
#     im = Image.open(str(name) + '.png') 
#     print("Image saved: ", str(name) + '.png')
#     im.show()        

  
def dot_graph(categories, data,**optional_params):
    fig, ax = plt.subplots() 
    color = colors[0]
    data = data
    data = list(map(lambda a, i: {'index': i, 'value': a}, data, range(len(data))))
    indexes = sorted(data, key=lambda x: x['value'])
    indexes = [a['index'] for a in indexes]
    values = [a['value'] for a in sorted(data, key=lambda x: x['value'])]
    cat = []
    for d in indexes:
        cat.append(categories[d])
    if ('color' in optional_params):
        color =(optional_params['color'])
    plt.scatter(cat,values,color=color)
    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()  

def waterfall_graph(categories, values, **optional_params):
    fig, ax = plt.subplots() 
    categories = [c for c, v in zip(categories, values) if v is not None]
    values = [v for v in values if v is not None]
    if 'title' in optional_params:
        ax.set_title(optional_params['title'])
    cumulative_sum = [sum(values[:i+1]) for i in range(len(values))]
    bars = ax.bar(categories, values, align='center', alpha=0.5)  
    ax.set_xlabel('Categories') 
    ax.set_ylabel('Value') 
    ax.set_title('Waterfall Chart')  
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.8) 
    ax.set_xticklabels(categories, rotation=45) 
    for bar, value in zip(bars, values):
        if value < 0:
            bar.set_color('red')
        else:
            bar.set_color(random.choice(colors))  # Random color selection

    name = str(random.random())
    plt.savefig(name + '.png')
    im = Image.open(name + '.png') 
    print("Image saved:", name + '.png')
    im.show()  


# categories = ['W1', 'W3', 'W5', 'W7', 'W9', 'W10']
# values = [10, 5, 4, -4, -5, -10]
# title = 'Secondary text'
# colors = ["#1D2026", "#393939", "#666666"]
# waterfall_graph(categories, values, title=title)


def baseline_graph(baseline, x_labels,colors, *series_data):
    fig, ax = plt.subplots()
    
    for i, series in enumerate(series_data):
        percentage_change_series = [(value - baseline[j]) / baseline[j] * 100 for j, value in enumerate(series)]
        ax.plot(x_labels, percentage_change_series, label=f'Product {i+1}', marker='o', color=random.choice(colors))

    ax.set_title('Chg. from Baseline')
    ax.legend()
    name = str(random.random())
    plt.savefig(name + '.png')
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()

# baseline = [10, 12, 14, 16, 18]
# series1 = [11, 15, 12, 13, 20]
# series2 = [9, 11, 13, 15, 17]
# series3 = [13, 14, 10, 12, 11]
# x_labels = ['W1', 'W3', 'W5', 'W7', 'W9']
# colors = ["#FC2964","#0095FF","#5C33F6"]
# baseline_graph(baseline, x_labels,colors, series1, series2, series3)


def scatter_plot_graph(marker_shapes, x_values, series_data, colors):
    np.random.seed(19680801)
    sizes = np.random.rand(len(x_values[0])) * 100 + 100

    fig, ax = plt.subplots()

    for i, marker in enumerate(marker_shapes):
        x = x_values[i]
        y = series_data[i]
        color = colors[i % len(colors)]  # Cycle through the available colors
        ax.scatter(x, y, s=sizes, alpha=0.5, marker=marker, color=color, label="Group {}".format(i+1))

    ax.set_title('Scatter Plot')
    ax.set_xlabel("Title")
    ax.set_ylabel("Title")
    ax.legend()

    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png')
    print("Image saved: ", str(name) + '.png')
    im.show()

# marker_shapes = ['s', 'o', 'D']
# x_values = [np.arange(0.15, 50.0, 2.0), np.arange(0.15, 50.0, 2.0), np.arange(0.15, 50.0, 2.0)]
# series_data = [
#     x_values[0] ** 1.3 + np.random.rand(*x_values[0].shape) * 30.0,
#     x_values[1] ** 1.5 + np.random.rand(*x_values[1].shape) * 40.0,
#     x_values[2] ** 1.2 + np.random.rand(*x_values[2].shape) * 20.0
# ]

# colors = ["#FC2964","#0095FF","#5C33F6"]

# scatter_plot_graph(marker_shapes, x_values, series_data, colors)


def stacked_bar(categories, below, above,**optional_params):
    species = categories
    weight_counts = {
        "Below": np.array(below),
        "Above": np.array(above),
    }
    width = 0.5

    fig, ax = plt.subplots()
    bottom = np.zeros(len(categories))

    index= 0
    color=["#0095FF","#1D2026"]

    if ('color' in optional_params):
        color= (optional_params['color'])
    
    print('BOTTOM: ',bottom)

    for boolean, weight_count in weight_counts.items():
        p = ax.bar(species, weight_count, width, color = color[index], label=boolean, bottom=bottom)
        index = index+1
        bottom += weight_count

    if ('xlabel' in optional_params):
        ax.set_xlabel(optional_params['xlabel'])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(loc='upper left',title=optional_params['legend'],bbox_to_anchor= (0.0, 1.010), ncol = 2)
        
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show() 

# categories = ('2010','2012','2014','2016','2018','2020')
# below=[30,35,40,45,50,55]
# above=[70,70,45,50,55,60]
# title = 'Stacked bar chart'
# ylabel='Title'
# legend='legends'
# stacked_bar(categories,below,above,title=title,ylabel=ylabel,legend=legend)

# series_data = [[ 50,  80, 20,  0,  20,  50], [ -10, -30, -10,  -80,  -30,  -10], [ -100, -60, -100,  -20,  0,  -100]]
# categories= ['Jan','Feb','Mar','Apr','May','Jun'] 
# title ='Popular items'
# ylabel ='In $'
# xlabel ='Month' # represent x axis title 
# label=[ 'Product 1', 'Product 2' , 'Product 3']
# line_graph(categories,series_data,label,title=title,ylabel = ylabel,xlabel = xlabel )


def heatmap_graph(y_axis_data, x_axis_data, colors,title):
    data = np.random.rand(len(y_axis_data), len(x_axis_data))
    cmap = ListedColormap(colors)
    plt.imshow(data, cmap=cmap)
    plt.yticks(range(len(y_axis_data)), y_axis_data)
    plt.xticks(range(len(x_axis_data)), x_axis_data)
    plt.colorbar()
    plt.title(title)
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()

# title='Heatmap'
# y_axis_data = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# x_axis_data = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2017, 2019, 2021, 2023]
# colors = ["#1D2026", "#393939", "#666666", "#BDBDBD", "#E0E0E0", "#F2F2F2", "#FD93B1",
#           "#FC2964", "#FEC9D8", "#FD5F8B", "#0095FF", "#E6F5FF", "#5C33F6", "#8566F8"]
# heatmap_graph(y_axis_data, x_axis_data, colors,title)



def heatmap2_graph(y_axis_data, x_axis_data, colors,title,dataFrom,dataTo):
    data = np.random.randint(dataFrom, dataTo, size=(len(y_axis_data), len(x_axis_data)))
    cmap = ListedColormap(colors)
    plt.imshow(data, cmap=cmap, interpolation='nearest')
    plt.yticks(range(len(y_axis_data)), y_axis_data)
    plt.xticks(range(len(x_axis_data)), x_axis_data)
    plt.colorbar()
    for i in range(len(y_axis_data)):
        for j in range(len(x_axis_data)):
            plt.text(j, i, str(data[i, j]), ha='center', va='center', color='white')
    plt.title(title)
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()


# title='Heatmap'
# dataFrom=1
# dataTo=100
# y_axis_data = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# x_axis_data = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2017, 2019, 2021, 2023]
# colors = ["#1D2026", "#393939", "#666666", "#BDBDBD", "#E0E0E0", "#F2F2F2", "#FD93B1",
#           "#FC2964", "#FEC9D8", "#FD5F8B", "#0095FF", "#E6F5FF", "#5C33F6", "#8566F8"]
# heatmap2_graph(y_axis_data, x_axis_data, colors,title,dataFrom,dataTo)

def boxPlot_graph(data, titles, colors,xAxisTitle,yAxisTitle):
    fig, ax = plt.subplots()
    box_plot = ax.boxplot(data, patch_artist=True)
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_linewidth(1)  # Set the linewidth for solid color style
    ax.set_xticklabels(titles)
    ax.legend().remove()
    ax.set_ylabel(yAxisTitle, fontsize=12)
    ax.set_xlabel(xAxisTitle, fontsize=12)
    plt.title('Box Plot')
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()

# data = [[25, 26, 27, 28, 29],
#         [20, 21, 22, 23, 24],
#         [10, 12, 14, 16, 18],
#         [10, 15, 20, 25, 30],
#         [20, 23, 26, 29, 32],
#         [22, 26, 29, 33, 36]]

# colors = ["#1D2026", "#393939", "#666666", "#BDBDBD", "#E0E0E0", "#F2F2F2", "#FD93B1",
#           "#FC2964", "#FEC9D8", "#FD5F8B", "#0095FF", "#E6F5FF", "#5C33F6", "#8566F8"]
# titles = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5', 'Group 6']
# xAxisTitle='Title'
# yAxisTitle='Title'
# boxPlot_graph(data, titles, colors,xAxisTitle,yAxisTitle)

def boxPlot2_graph(data, titles, colors, xAxisTitle, yAxisTitle):
    fig, ax = plt.subplots()
    box_plot = ax.boxplot(data, patch_artist=True)
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set(facecolor=color, alpha=0.5, edgecolor=color)
        patch.set_linewidth(1)  
    ax.set_xticklabels(titles)
    ax.legend().remove()
    ax.set_ylabel(yAxisTitle, fontsize=12)
    ax.set_xlabel(xAxisTitle, fontsize=12)
    plt.title('Box Plot')
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()

# data = [[25, 26, 27, 28, 29],
#         [20, 21, 22, 23, 24],
#         [10, 12, 14, 16, 18],
#         [10, 15, 20, 25, 30],
#         [20, 23, 26, 29, 32],
#         [22, 26, 29, 33, 36]]

# colors = ["#FEC9D8","#FD5F8B","#0095FF","#1D2026","#5C33F6","#8566F8"]
# titles = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5', 'Group 6']
# xAxisTitle = 'Title'
# yAxisTitle = 'Title'
# boxPlot2_graph(data, titles, colors, xAxisTitle, yAxisTitle)



def boxPlot3_graph(data, colors,title, xAxisTitle, yAxisTitle):
    fig, ax = plt.subplots()
    box_plots = ax.boxplot(data, patch_artist=True, vert=True, widths=0.5)
    for patch, color in zip(box_plots['boxes'], colors[:len(data)]):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors[:len(data)]]
    legend_labels = [f'{i+1}' for i in range(len(data))]
    ax.legend(legend_handles, legend_labels, loc='upper right')
    ax.set_title(title)
    ax.set_xlabel(xAxisTitle)
    ax.set_ylabel(yAxisTitle)
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    print("Image saved: ", str(name) + '.png')
    im.show()


# title="Box Plot"
# xAxisTitle="Legend"
# yAxisTitle="Title"
# title="Box Plot"
# colors = ["#1D2026", "#393939", "#666666", "#BDBDBD", "#E0E0E0", "#F2F2F2",
#           "#FD93B1", "#FC2964", "#FEC9D8"]
# data = [[25, 26, 27, 28, 29],
#         [20, 25, 29, 33, 35],
#         [20, 21, 22, 23, 24],
#         [10, 12, 14, 16, 18],
#         [10, 15, 20, 25, 30],
#         [20, 23, 26, 29, 32],
#         [22, 26, 29, 33, 36],
#         [22, 26, 29, 33, 36],
#         [20, 21, 22, 23, 24],
#         [20, 23, 26, 29, 32],
#         [22, 26, 29, 33, 36]]
# boxPlot3_graph(data, colors,title, xAxisTitle, yAxisTitle)



def next_item_predictions(categories, values, **optional_params):
    fig, ax = plt.subplots()
    categories = [c for c, v in zip(categories, values) if v is not None]
    values = [v for v in values if v is not None]
    if 'title' in optional_params:
        ax.set_title(optional_params['title'])
    cumulative_sum = [sum(values[:i + 1]) for i in range(len(values))]
    
    colors = [ "#FC2964", "#5C33F6"]
    
    bars = ax.barh(categories, values, align='center', alpha=0.5)
    ax.set_xlabel('Value')
    ax.set_ylabel('Categories')
    ax.set_title('Next Item Predications')
    ax.grid(True)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_yticklabels(categories)
    
    for bar, value in zip(bars, values):
        if value < 0:
            bar.set_color('red')
        else:
            bar.set_color('blue')
    
    name = str(random.random())
    plt.savefig(name + '.png')
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()


# categories = ['Burger', 'Pizza', 'sandwitch', 'pasta', 'momos', 'garlic']
# values = [10, 5, 4, -4, -5, -10]
# title = 'Secondary text'

# next_item_predictions(categories, values, title=title)



def table_count(xAxisvalue, predicatedLine, actualLine):
    x = np.arange(len(xAxisvalue))
    x_smooth = np.linspace(0, len(xAxisvalue) - 1, 100)
    f_actual = interp1d(x, actualLine, kind='cubic')
    f_predicted = interp1d(x, predicatedLine, kind='cubic')
    actualLine_smooth = f_actual(x_smooth)
    predicatedLine_smooth = f_predicted(x_smooth)
    fig, ax = plt.subplots(figsize=(16, 9))  # Set maximum size
    
    ax.plot(x_smooth, actualLine_smooth, color="#FC2964", label='Actual')
    ax.plot(x_smooth, predicatedLine_smooth, color="#5C33F6", label='Predicted')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Table Count')
    ax.legend()
    ax.xaxis.set_major_locator(ticker.IndexLocator(base=1, offset=0))
    ax.set_xticklabels(xAxisvalue)
    
    name = str(random.random())
    plt.savefig(name + '.png', dpi=300)  # Set higher dpi for better image quality
    im = Image.open(name + '.png')
    print("Image saved:", name + '.png')
    im.show()

# xAxisvalue = ['8:00 PM', '9:00 PM', '10:00 PM', '12:00 PM', '1:00 AM', '3:00 AM', '3:00 AM', '4:00 AM', '5:00 AM','3:00 AM', '3:00 AM', '4:00 AM', '5:00 AM']
# predicatedLine = [30,30, 33, 28,34,29, 33, 28,34,29,28,33,32]
# actualLine = [30,30,29, 33,32,29,29, 33,32,29,30,31,37]
# table_count(xAxisvalue, predicatedLine, actualLine)
