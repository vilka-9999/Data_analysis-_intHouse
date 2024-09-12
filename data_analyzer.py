import csv
import numpy
import pandas
import matplotlib.pyplot as plt
import os
import math



    
# function to display percent if it is larger then 2
def my_autopct(x):
    return ('%.2f%%' % x) if x >= 3 else ''


# display labels when value is more then 8
def disp_labels(values, labels):
    display_labels = []
    all_values = values.sum()
    for value, label in zip(values, labels):
        if value >= 8 or value/all_values >= 0.03: 
            display_labels.append(label)
        else:
            display_labels.append('')
    return display_labels



def plot(df):
    
    columns = df.columns.tolist()
    colors = plt.get_cmap('tab20').colors

    os.makedirs(f'plots', exist_ok=True)

    # plot pie charsbased on one column values
    for column in columns:
        # get values and labels
        values = df[column].value_counts()
        labels = values.index
        display_labels = disp_labels(values, labels)

        # plot the figure
        plt.figure(figsize=(12, 10))
        plt.title(column)
        plt.pie(values, labels=display_labels, autopct=my_autopct, colors=colors)
        legend_labels = [f'{l}, {s:.0f}' for l, s in zip(labels, values)] # dispaly values in the legend
        plt.legend(bbox_to_anchor=(-0.25, 0.2), loc='upper left', labels=legend_labels)
        plt.savefig(f'plots/pie_chart_{column}')


    # plot graphs for analysis between races

    ethnicity_counts = df['ETHNICITY'].value_counts()
    ethnicities = ethnicity_counts.index
    columns_num = 4
    rows_num = math.ceil(len(ethnicities) / columns_num) 
    columns.remove('ETHNICITY')

    for column in columns:
        fig, axs = plt.subplots(rows_num, columns_num, figsize=(22, 12))
        plt.suptitle(f'{column} charts for different ethnicities', fontsize=30)

        # create a dictionary for colors and maps to make one legend
        all_labels = df[column].unique()
        label_to_color = {name: color for name, color in zip(all_labels, colors)}

        for ax, ethnicity in zip(axs.flat, ethnicities): # flat flats axs ndarray to 1d array so it can be looped through
            ethn_df = df[df['ETHNICITY'] == ethnicity]
            values = ethn_df[column].value_counts()
            labels = values.index
            display_labels = disp_labels(values, labels)

            ax.pie(values, labels=display_labels, autopct=my_autopct, colors=labels.map(label_to_color))
            ax.set_title(f'{ethnicity}\n{ethnicity_counts[ethnicity]}', y = -0.12) # set title under the plot

        handles = [plt.Rectangle((0, 0), 0, 0, color=label_to_color[name], label=name) for name in label_to_color] # create boxes and labels for the legend
        fig.legend(handles=handles, fontsize=14)
        plt.savefig(f'plots/ethnicity_pie_charts_for_{column}')



def main():
    data = pandas.read_csv('MIC_Fall_2024_Data_csv.csv')
    # clean gender nulls
    data['GENDER'] = data['GENDER'].fillna('N') 
    data = data.drop(columns=['STU_PRGM_CODE'])
    plot(data)


if __name__ == '__main__':
    main()