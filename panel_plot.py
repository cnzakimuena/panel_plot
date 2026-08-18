""" 
This script generates a panel plot of images with specified dimensions. It uses microscopic 
images for demonstration and includes example annotations. The function creates a grid 
of subplots, each displaying an image from the provided list of image paths.
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import pypalettes

from preprocessing import Preprocessor

# non-italic matplotlib greek characters
matplotlib.rcParams['mathtext.default'] = 'regular'


def generate_plot(img_paths, panel_dim, **plot_kwargs):
    """
    Generates a panel plot of images with specified dimensions and optional
    labelling and color palette. The function creates a grid of subplots, each displaying an
    image from the provided list of image paths. The panel dimensions, x and y
    labelling, and color palette can be customized through the function's parameters.
    """
    # set new font
    plt.rcParams['font.family'] = ['Arial']
    # set font size
    global_font_size = 18
    plt.rcParams.update({'font.size': global_font_size})

    # default color palette assignment if not provided
    if 'palette_list' not in plot_kwargs:
        plot_kwargs['palette_list'] = sns.color_palette("Blues", panel_dim[0])
    elif 'palette_list' in plot_kwargs:
        plot_kwargs['palette_list'] = plot_kwargs['palette_list'][:panel_dim[0]]

    with plt.rc_context({'axes.edgecolor': 'black'}):

        fig, _ = plt.subplots(panel_dim[0], panel_dim[1],
                                 sharex=False, sharey=False,
                                 figsize=(10.5, 7))

        # if no x labelling specified, assign as 'image x' where x is the column index
        if 'specified_x_label' not in plot_kwargs:
            plot_kwargs['specified_x_label'] = \
                [f"{'image '}{i}" for i in range(1, panel_dim[1] + 1)]
        if len(plot_kwargs['specified_x_label']) != panel_dim[1]:
            raise ValueError(r'Specified x labelling length does not match total panel columns.')

        # if no y labelling specified, assign as 'category x' where x is the reverse row index
        if 'specified_y_label' not in plot_kwargs:
            plot_kwargs['specified_y_label'] = \
                [f"{'category '}{i}" for i in range(panel_dim[0], 0, -1)]
        if len(plot_kwargs['specified_y_label']) != panel_dim[0]:
            raise ValueError(r'Specified y labelling length does not match total panel rows.')
        # initialise y labelling count
        y_label_count = 0
        # get row start indices as list
        y_labels_idx = [r * panel_dim[1] for r in range(panel_dim[0])]

        count = 0

        for ax in fig.axes:

            # adjust subplots spacing
            plt.subplots_adjust(bottom=0.1, top=0.9,
                                left=0.14, right=0.86,
                                wspace=0.03, hspace=0.03)

            # read image in, gather dimensions
            pic = plt.imread(img_paths[count])
            curr_height_len = pic.shape[0]
            curr_width_len = pic.shape[1]

            # add the image to the axes
            ax.imshow(pic, cmap='gray')

            # Turn off tick labels
            ax.set_yticklabels([])
            ax.set_xticklabels([])

            # hide spines
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

            # hide ticks
            ax.set_xticks([])
            ax.set_yticks([])

            # add column labelling
            if count < panel_dim[1]:
                ax.set(title=plot_kwargs['specified_x_label'][count])
                ax.title.set_size(global_font_size)

            # add dimension annotation
            height_loc = curr_height_len * 0.9
            width_loc = curr_width_len * 0.7
            if (count + 1) % panel_dim[1] == 0:
                ax.text(width_loc - width_loc * 0.075,
                        height_loc - height_loc * 0.075,
                        r'10 $\mu$m', va='center', fontsize=10, color="black")

            # add dimension line
            x, y = np.array([[width_loc, width_loc + width_loc * 0.15],
                             [height_loc, height_loc]])
            line = Line2D(x, y, lw=2, color='black')
            ax.add_line(line)

            # assign row labelling and color
            if count in y_labels_idx:
                ax.set_ylabel(plot_kwargs['specified_y_label'][y_label_count])
                ax.yaxis.label.set_color(plot_kwargs['palette_list'][y_label_count])
                y_label_count += 1

            count += 1

    # add custom labelling text next to subplots
    plt.figtext(0.0775, 0.75, "Apicomplexa", rotation=90,
                ha="center", va="top", fontsize=global_font_size, color="k")
    # draw custom line next to subplots
    ax2 = plt.axes([0, 0, 1, 1], facecolor=(1, 1, 1, 0))
    ax2.axis('off')
    x, y = np.array([[0.098, 0.098], [0.4,  0.865]])
    line = Line2D(x, y, lw=2, color='k')
    ax2.add_line(line)


if __name__ == '__main__':

    # --- read data ---
    EXAMPLE_DATA_PATH = r'.\dataset'
    example_data = Preprocessor(EXAMPLE_DATA_PATH)
    example_data.dataset_preprocessing()

    # palette setup (optional)
    cmap = pypalettes.load_cmap("Landscape")
    pypalettes_list = cmap.colors # return colors as a list of hexadecimal values

    # --- plot data ---
    generate_plot(example_data.prep_img_paths, [3, 4],
                  specified_y_label=['Babesia', 'Toxoplasma', 'Trypanosoma'],
                  palette_list=pypalettes_list)

    # save figure
    FILE_DESTINATION = r'.\figure'
    plt.savefig(os.path.join(FILE_DESTINATION + '.pdf').replace("\\", "/"), format="pdf")
    plt.savefig(os.path.join(FILE_DESTINATION + '.png').replace("\\", "/"), dpi=300)
    plt.close()
