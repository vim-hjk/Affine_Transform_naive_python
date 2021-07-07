import yaml
import matplotlib.pyplot as plt

from easydict import EasyDict


# Config Manager
class YamlConfigManager:
    def __init__(self, config_file_path, config_name):
        super().__init__()
        self.values = EasyDict()        
        if config_file_path:
            self.config_file_path = config_file_path
            self.config_name = config_name
            self.reload()
    
    def reload(self):
        self.clear()
        if self.config_file_path:
            with open(self.config_file_path, 'r') as f:
                self.values.update(yaml.safe_load(f)[self.config_name])

    def clear(self):
        self.values.clear()
    
    def update(self, yml_dict):
        for (k1, v1) in yml_dict.items():
            if isinstance(v1, dict):
                for (k2, v2) in v1.items():
                    if isinstance(v2, dict):
                        for (k3, v3) in v2.items():
                            self.values[k1][k2][k3] = v3
                    else:
                        self.values[k1][k2] = v2
            else:
                self.values[k1] = v1

    def export(self, save_file_path):
        if save_file_path:
            with open(save_file_path, 'w') as f:
                yaml.dump(dict(self.values), f)


def plot_result(images, mode, output_path, is_save):
    # set figure index
    rows = [-1, 2, 2, 2, 2]
    cols = [-1, 4, 4, 4, 4]
    index = [-1, 3, 4, 7, 8]

    axes = []
    fig = plt.figure(figsize=(25, 22))

    # set sub_title
    if mode == 'back' : title = ["Original Image", "Translate", "Back Rotate", "Back Scaling", "Back Affine Transform"]
    else: title = ["Original Image", "Translate", "Rotate", "Scaling", "Affine Transform"]

    # plot figure
    for a in range(5):
        b = images[a]
        if a == 0: axes.append(fig.add_subplot(1, 2, 1))
        else: axes.append(fig.add_subplot(rows[a], cols[a], index[a]))
        subplot_title = title[a]
        axes[-1].set_title(subplot_title)
        plt.imshow(b)

    fig.tight_layout()

    # save option
    if is_save: plt.savefig(output_path, dpi=199)

    plt.show()