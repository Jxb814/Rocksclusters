# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""
import os

import sys
sys.path.append("./")
sys.path.append("..")

from analysis_thread.sampling_simulation_thread import PeriodSampling

from analysis_task.demo_turbine.task_turbine_sampling_simulation import UnitHPSimulation

# TODO：add your module
from analysis_task.m300exair.task_exair_sampling_simulation import UnitExaircoffSimulation

if __name__ == "__main__":

    TaskList = []

    pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    analysis_taskpath = os.path.join(pardir, "analysis_task")

    taginfile = os.path.join(analysis_taskpath, "demo_turbine", "task_turbine_tag_in.txt")

    SimulationUnitHP = UnitHPSimulation(taginfile)
    TaskList.append(SimulationUnitHP)

    # TODO: add your task
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")

    Simulation = UnitExaircoffSimulation(taginfile)
    TaskList.append(Simulation)


    OnlineTasks = PeriodSampling(2, TaskList)
    OnlineTasks.settag()
    OnlineTasks.worker()
