# -*- coding: utf-8 -*-
 
from fastai.vision.widgets import *
from fastbook import *
from pathlib import Path

chart_folder = Path('data')
fns = get_image_files(chart_folder)

charts = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label)

dls = charts.dataloaders(chart_folder)

learn = cnn_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(4)

learn.export(fname='apple_trading.pkl')