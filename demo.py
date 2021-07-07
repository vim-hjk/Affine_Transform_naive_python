import os
import argparse
import numpy as np

from PIL import Image
from prettyprinter import cpprint

from src.transform.affine_transform import AffineTransform2D
from src.utils.uitls import YamlConfigManager, plot_result


def demo(cfg):
    MODE = cfg.values.mode
    IMAGE_PATH = cfg.values.image_path
    OUTPUT_PATH = cfg.values.output_path
    IS_SAVE = cfg.values.is_save

    TRANSLATE_TX = cfg.values.translate.tx
    TRANSLATE_TY = cfg.values.translate.ty

    ROTATE_DEGREE = cfg.values.rotate.degree

    SCALING_X = cfg.values.scaling.sx
    SCALING_Y = cfg.values.scaling.sy
    
    AFFINE_TX = cfg.values.affine.tx
    AFFINE_TY = cfg.values.affine.ty
    AFFINE_DEGREE = cfg.values.affine.degree
    AFFINE_SX = cfg.values.affine.sx
    AFFINE_SY = cfg.values.affine.sy

    img = Image.open(IMAGE_PATH) # test.jpg : 626 x 1024 x 3
    affine = AffineTransform2D(img)

    images = list()

    images.append(np.array(img))
    images.append(np.array(affine.translate(TRANSLATE_TX, TRANSLATE_TY)))

    if MODE == 'back':        
        images.append(np.array(affine.back_rotate(ROTATE_DEGREE)))
        images.append(np.array(affine.back_scaling(SCALING_X, SCALING_Y)))        
        images.append(np.array(affine.back_affine(AFFINE_TX, AFFINE_TY, AFFINE_DEGREE, AFFINE_SX, AFFINE_SY)))
    else:
        images.append(np.array(affine.rotate(ROTATE_DEGREE)))
        images.append(np.array(affine.scaling(SCALING_X, SCALING_Y)))        
        images.append(np.array(affine.affine(AFFINE_TX, AFFINE_TY, AFFINE_DEGREE, AFFINE_SX, AFFINE_SY)))

    plot_result(images, MODE, OUTPUT_PATH, IS_SAVE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file_path', type=str, default='./config/config.yml')
    parser.add_argument('--config', type=str, default='back')
    args = parser.parse_args()

    cfg = YamlConfigManager(args.config_file_path, args.config)
    cpprint(cfg.values, sort_dict_keys=False)
    print('\n')
    demo(cfg)