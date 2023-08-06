import os

import matplotlib.pyplot as plt

def save_figure(figure_obj):
    path = get_figure_path(figure_obj)
    figures_obj = figure_obj.figures_obj
    save_fig(path, figures_obj)
    plt.close()

def get_figure_path(figure_obj):
    file_name = get_file_name(figure_obj)
    file_name = f"{file_name}.{figure_obj.figures_obj.format}"
    path = os.path.join(figure_obj.figures_obj.path, file_name)
    return path

def get_file_name(figure_obj):
    if len(figure_obj.figures_obj.data_object_groups) == 1:
        return get_base_file_name(figure_obj.figures_obj)
    else:
        return get_numbered_file_name(figure_obj)

def get_base_file_name(figure_objs):
    if figure_objs.title is None:
        return "Figure"
    else:
        return str(figure_objs.title)

def get_numbered_file_name(figure_obj):
    file_name = get_base_file_name(figure_obj.figure_objs)
    file_name = f"{file_name} {figure_obj.figure_index + 1}"
    return file_name

def save_fig(path, figures_obj):
    plt.savefig(path,
                dpi=figures_obj.dpi,
                format=figures_obj.format,
                metadata=figures_obj.metadata,
                bbox_inches=figures_obj.bbox_inches,
                pad_inches=figures_obj.pad_inches,
                facecolor=figures_obj.facecolor,
                edgecolor=figures_obj.edgecolor,
                backend=figures_obj.backend)
