# plotting.py

# imports
from typing import Any

import matplotlib as mpl
import numpy as np
import pandas as pd

from matplotlib.axes import Axes
from matplotlib.colors import Colormap


# define a function to deduplicate legend entries
def deduplicate_legend(ax: Axes, **legend_kwargs: Any) -> None:
    """
    Deduplicate legend entries for the given Axes object.

    Parameters:
    ax (Axes): The Axes object to deduplicate legend entries for.
    **legend_kwargs: Additional keyword arguments to pass to ax.legend.
    """
    # get the current legend handles and labels
    handles, labels = ax.get_legend_handles_labels()

    # create a dictionary to deduplicate labels
    by_label = dict(zip(labels, handles))

    # set the legend with deduplicated entries
    ax.legend(by_label.values(), by_label.keys(), **legend_kwargs)


# define a class to create a grouped bar plot
class GroupedBarPlot:
    """
    A class to create grouped bar plots using Matplotlib.

    Attributes:
    -----------
    df : pd.DataFrame
        The dataframe containing the data to plot.
    group_key : object
        The key to group the data by.
    colormap : Union[str, Colormap]
        The colormap to use for the bars.
    label_dict : Dict[object, str], optional
        A dictionary mapping column names to labels for the legend.

    Methods:
    --------
    calc_axis_params() -> Dict[str, float]:
        Calculate default axis parameters for the plot.
    create_plot(ax: Axes, axis_param_dict: Dict[str, float] = None, **bar_kwargs: Any) -> None:
        Create the grouped bar plot on the given Axes object.
    """

    def __init__(self, df: pd.DataFrame, colormap: str | Colormap = 'tab10', label_dict: dict[object, str] = None):
        """
        Initialize the GroupedBarPlot class.

        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the data to plot.
        group_key : object
            The key to group the data by.
        colormap : Union[str, Colormap], optional
            The colormap to use for the bars. Default is 'tab10'.
        label_dict : Dict[object, str], optional
            A dictionary mapping column names to labels for the legend.
        """
        # check that the dataframe has at least two columns
        if len(df.columns) < 2:
            raise ValueError("Dataframe must have at least two columns.")

        # check that each entry to index is unique
        if not df.index.is_unique:
            raise ValueError("Index of DataFrame must be unique.")

        # load the colormap
        if isinstance(colormap, str):
            self.colormap = mpl.colormaps[colormap]
        elif isinstance(colormap, Colormap):
            self.colormap = colormap
        else:
            raise ValueError("Colormap must be a string in mpl.colormaps or a matplotlib Colormap object.")

        # save variables
        self.df = df
        # save either the dict or an empty dict
        self.label_dict = label_dict if label_dict else {}


    def calc_axis_params(self) -> dict[str, float]:
        """
        Calculate default axis parameters for the plot.

        Returns:
        --------
        Dict[str, float]
            A dictionary containing default axis parameters.
        """
        # get the number of groups and list of categories
        group_num = self.df.index.nunique()
        categories = self.df.columns
        cat_num = len(categories)

        # define values for horizontal scaling
        min_x = 0
        max_x = 1

        group_padding = 0.2 / cat_num
        ax_padding = 1 / group_num

        group_width = ((max_x - min_x) / (group_num-1)) - group_padding
        bar_width = (group_width / cat_num)

        # calculate the center of each group
        x_ticks = np.linspace(min_x, max_x, group_num)

        # for each group calculate the center of each bar
        bar_pos = {}
        for i, (_, row_series) in enumerate(self.df.iterrows()):
            # this will be the key of bar_pos
            x_tick = x_ticks[i]

            # calculate the left-edge placement of each bar
            first_left = x_tick - (group_width / 2)
            last_left = x_tick + (group_width / 2) - bar_width

            # calculate the center placement of each bar
            bar_centers = np.linspace(first_left, last_left, cat_num) + (bar_width / 2)

            # associate each center with a category and height
            bar_pos[x_tick] = [
                (cat, bcen, row_series[cat])
                for bcen, cat in zip(bar_centers, categories)
            ]

        # create and return the dictionary of axis parameters
        return {
            'group_num': group_num,
            'categories': categories,
            'cat_num': cat_num,
            'min_x': min_x,
            'max_x': max_x,
            'group_padding': group_padding,
            'ax_padding': ax_padding,
            'group_width': group_width,
            'bar_width': bar_width,
            'x_ticks': x_ticks,
            'bar_pos_dict': bar_pos
        }


    def create_plot(self, ax: Axes, axis_param_dict: dict[str, float] = None, **bar_kwargs: Any) -> None:
        """
        Create the grouped bar plot on the given Axes object.

        Parameters:
        -----------
        ax : Axes
            The Axes object to create the plot on.
        axis_param_dict : Dict[str, float], optional
            A dictionary containing axis parameters. If not provided, default parameters will be used.
        **bar_kwargs : Any
            Additional keyword arguments to pass to the ax.bar method.
        """
        # get the param dict and ensure all keys are available
        if axis_param_dict:
            default_params = self.calc_axis_params()
            missing_keys = set(default_params.keys()) - set(axis_param_dict.keys())
            axis_param_dict.update({key: default_params[key] for key in missing_keys})
        else:
            axis_param_dict = self.calc_axis_params()

        # ensure bar_kwargs does not contain 'x', 'height', or 'width'
        prohibited_keys = {'x', 'height', 'width'}
        if prohibited_keys & set(bar_kwargs.keys()):
            raise ValueError(f"bar_kwargs cannot contain the keys {prohibited_keys}.")

        # check for label or color overrides
        color_override = {'facecolor', 'color'} & set(bar_kwargs.keys())
        label_override = 'label' in bar_kwargs

        # set horizontal labels
        x_ticks = axis_param_dict['x_ticks']
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(self.df.index)

        # set horizontal limits
        min_x = axis_param_dict['min_x']
        max_x = axis_param_dict['max_x']
        ax_padding = axis_param_dict['ax_padding']
        ax.set_xlim(min_x - ax_padding, max_x + ax_padding)

        # plot each bar from the bar_pos_dict
        bar_width = axis_param_dict['bar_width']
        for _, bar_list in axis_param_dict['bar_pos_dict'].items():
            for j, (cat, bar_center, height) in enumerate(bar_list):
                # attempt to get the label from the label dict
                if not label_override:
                    bar_kwargs['label'] = self.label_dict.get(cat, cat)

                # get the color and handle errors
                if not color_override:
                    try:
                        bar_kwargs['facecolor'] = self.colormap(j)
                    except ValueError as e:
                        cat_num = len(self.df.columns)
                        raise ValueError(f"Colormap must have at least {cat_num} colors.") from e

                # add the bar using the kwargs dict
                ax.bar(
                    x=bar_center,
                    height=height,
                    width=bar_width,
                    **bar_kwargs
                )


# define a plot label object
class PlotLabel:
    """
    A class to represent a label for a Matplotlib plot.

    Attributes:
    ----------
    key : object
        The key associated with the PlotLabel object.
    text : str
        The text for the PlotLabel object.
    plt_args : dict
        A dictionary of plotting arguments for the PlotLabel object.

    Methods:
    -------
    __init__(self, key: object, text: str, plt_args: dict)
        Initializes the PlotLabel object with the given key, text, and plotting arguments.

    get_key(self) -> object
        Returns the key associated with the PlotLabel object.

    get_text(self) -> str
        Returns the text for the PlotLabel object.

    get_plt_args(self) -> dict
        Returns the dictionary of plotting arguments for the PlotLabel object.

    __repr__(self)
        Returns a string representation of the PlotLabel object.
    """

    def __init__(self, key: object, text: str, plt_args: dict):
        """
        Initializes the PlotLabel object with the given key, text, and plotting arguments.

        Parameters:
        ----------
        key : object
            The key associated with the PlotLabel object.
        text : str
            The text for the PlotLabel object.
        plt_args : dict
            A dictionary of plotting arguments for the PlotLabel object.

        Raises:
        ------
        ValueError
            If plt_args is None or not a dictionary, or if text is not a string.
        """
        # ensure that plt_args is at least an empty dict
        if plt_args is None:
            raise ValueError("plt_args cannot be None")
        if not isinstance(plt_args, dict):
            raise ValueError("plt_args must be a dict")

        # ensure text is a string
        if not isinstance(text, str):
            raise ValueError("text must be a string")

        # save data
        self.key = key
        self.text = text
        self.plt_args = plt_args

    def get_key(self) -> object:
        """
        Returns the key associated with the PlotLabel object.

        Returns:
        -------
        object
            The key associated with the PlotLabel object.
        """
        return self.key

    def get_text(self) -> str:
        """
        Returns the text for the PlotLabel object.

        Returns:
        -------
        str
            The text for the PlotLabel object.
        """
        return self.text

    def get_plt_args(self) -> dict:
        """
        Returns the dictionary of plotting arguments for the PlotLabel object.

        Returns:
        -------
        dict
            The dictionary of plotting arguments for the PlotLabel object.
        """
        return self.plt_args

    def __repr__(self):
        return f"PlotLabel(key={self.key}, text='{self.text}', plt_args={self.plt_args})"


# define a class to manage unique labels and parameters
class PlotLabelManager:
    """
    A class to manage PlotLabel objects for labeling Matplotlib plots.

    Attributes:
    ----------
    labels : dict
        A dictionary to hold PlotLabel objects.
    access : dict
        A dictionary to track access to PlotLabel objects.
    arg_map : dict[str, list]
        A dictionary mapping keys to lists of arguments for PlotLabel objects.

    Methods:
    -------
    __init__(self, args_map_dict: dict[str, list])
        Initializes the PlotLabelManager with a dictionary of argument mappings.

    get_plot_label(self, key: object) -> PlotLabel
        Returns the PlotLabel object associated with the given key.

    key_exists(self, key: object) -> bool
        Checks if a key exists in the labels dictionary.
    """

    def __init__(self, args_map_dict: dict[str, list]):
        """
        Initializes the PlotLabelManager with a dictionary of argument mappings.

        Parameters:
        ----------
        args_map_dict : dict[str, list]
            A dictionary mapping keys to lists of arguments for PlotLabel objects.

        Raises:
        ------
        ValueError
            If the lists in args_map_dict have inconsistent lengths.
        """
        # define a dict to hold PlotLabel objects and access booleans
        self.labels = {}
        self.access = {}

        # store the argument map with lists reversed for popping
        self.arg_map = {k:v[::-1] for k, v in args_map_dict.items()}

        # check for inconsistent list lengths
        list_lens = set(len(v) for v in self.arg_map.values())
        if len(list_lens) > 1:
            # get the shortest list
            min_len = min(list_lens)

            # print warning
            print(f"Warning: not all lists in arg_map are the same length. Shortest list has {min_len} elements.")


    def get_plot_label(self, key: object) -> PlotLabel:
        """
        Returns the PlotLabel object associated with the given key.

        Parameters:
        ----------
        key : object
            The key associated with the desired PlotLabel object.

        Returns:
        -------
        PlotLabel
            The PlotLabel object associated with the given key.

        Raises:
        ------
        ValueError
            If the key does not exist in the labels dictionary.
        """
        # check if key exists
        if not self.key_exists(key):
            raise ValueError(f"Key '{key}' not found")

        return self.labels[key]


    def key_exists(self, key: object) -> bool:
        """
        Checks if a key exists in the labels dictionary.

        Parameters:
        ----------
        key : object
            The key to check for existence in the labels dictionary.

        Returns:
        -------
        bool
            True if the key exists, False otherwise.
        """
        return key in self.labels


    def add(self, key: object, text: str, plt_args: dict = None) -> None:
        """
        Adds a new PlotLabel object to the labels dictionary.

        Parameters:
        ----------
        key : object
            The key associated with the new PlotLabel object.
        text : str
            The text for the new PlotLabel object.
        plt_args : dict, optional
            A dictionary of plotting arguments for the new PlotLabel object. If None, arguments are extracted from the arg_map.

        Raises:
        ------
        ValueError
            If the key already exists in the labels dictionary.
        """
        # check if key is already in list
        if self.key_exists(key):
            raise ValueError(f"Key '{key}' already exists")

        # if no plt_args are supplied, extract them from the arg_map
        if plt_args is None:
            # replace plt_args with an empty dict
            plt_args = {}

            # iterate over each key:list pair of the arg_map
            for arg_key, arg_list in self.arg_map.items():
                # check that arg_list is not empty
                if len(arg_list) == 0:
                    raise IndexError(f"arg_list for '{arg_key}' has been depleted of unique values")

                # the key of arg_key is the argument key in matplotlib.plt
                plt_args[arg_key] = arg_list.pop()

        # create a new PlotLabel object and append
        plot_label = PlotLabel(key, text, plt_args)
        self.labels[plot_label.get_key()] = plot_label
        self.access[plot_label.get_key()] = False


    def try_add(self, key: object, text: str, plt_args: dict = None) -> None:
        """
        Tries to add a new PlotLabel object to the labels dictionary if the key does not already exist.

        Parameters:
        ----------
        key : object
            The key associated with the new PlotLabel object.
        text : str
            The text for the new PlotLabel object.
        plt_args : dict, optional
            A dictionary of plotting arguments for the new PlotLabel object. If None, arguments are extracted from the arg_map.
        """
        # check if key is not already in list
        if not self.key_exists(key):
            self.add(key=key, text=text, plt_args=plt_args)


    def get_args(self, key: object) -> dict:
        """
        Returns the plotting arguments for the PlotLabel object associated with the given key.

        Parameters:
        ----------
        key : object
            The key associated with the desired PlotLabel object.

        Returns:
        -------
        dict
            A dictionary of plotting arguments for the PlotLabel object, including the 'label' key.
        """
        # prepare the return dict
        plot_label = self.get_plot_label(key)
        return_dict = plot_label.get_plt_args().copy()
        return_dict['label'] = plot_label.get_text()

        # deduplicate the label entry for plotting
        if self.access[key]:
            return_dict['label'] = None
        else:
            self.access[key] = True

        return return_dict


    def __repr__(self):
        # compose the repr string out of repr strings from contained plot labels in a list
        head = "PlotLabelManager:\n - "
        labels = "\n - ".join([f"{plot_label}" for plot_label in self.labels.values()])

        return_str = head + labels
        return return_str
