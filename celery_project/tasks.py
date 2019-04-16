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
app.conf.update(result_expires=3600)

print app.conf.task_routes


pcs = music_analysis()

@app.task
def music_composition_wrapper(sent_score, lex_score, compl_score, length, output_name):
    # [sentiment_score, lexical_score, complexity_score, length]
    custom_query = [sent_score, lex_score, compl_score, length]
    print 'Music would be composed for {} query and outputed into {}.mid'.format(custom_query, output_name)

    run_custom_music_composition(pcs, custom_query, output_name=output_name)
