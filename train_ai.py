# -*- coding: utf-8 -*-
 
from fastai.vision.widgets import *
from fastbook import *
from pathlib import Path

def main():
    chart_folder = Path('data\\model_data')

    charts = DataBlock(
        blocks=(ImageBlock, CategoryBlock), 
        get_items=get_image_files, 
        splitter=RandomSplitter(valid_pct=0.2, seed=42),
        get_y=parent_label)

    dls = charts.dataloaders(chart_folder)

    learn = cnn_learner(dls, resnet18, metrics=error_rate)
    learn.fine_tune(4)

    learn.export(fname='data\\deep_trading.pkl')

if __name__ == '__main__':
    main()
