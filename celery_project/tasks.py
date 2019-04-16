# from __future__ import absolute_import

import time

from celery import Celery

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from utils import *
from music_generation_module import run_custom_music_composition, music_analysis


app = Celery('celery_project',
             broker='pyamqp://segal:segal@localhost:5672/segal',
             backend='rpc://')

app.conf.task_routes   = {'celery_project.tasks.*': {'queue': 'celery'}}
# app.conf.task_protocol = 1

print app.conf.task_routes

app.conf.update(result_expires=3600)

@app.task
def test_lol(sent_score, lex_score, compl_score, length, output_name):
    print sent_score, lex_score, compl_score, length, output_name

@app.task
def longtime_add(x, y):
    print 'long time task begins'

    time.sleep(5)

    return x + y

@app.task
def music_composition_wrapper(sent_score, lex_score, compl_score, length, output_name):
    # [sentiment_score, lexical_score, complexity_score, length]
    custom_query = [sent_score, lex_score, compl_score, length]
    print 'Music would be composed for {} query and outputed into {}'.format(custom_query, output_name)

    pcs = music_analysis()
    run_custom_music_composition(pcs, custom_query, output_name=output_name)
