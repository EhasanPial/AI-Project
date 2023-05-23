#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 08:50:35 2023

@author: kanizfatema
"""


def getMembershipService(service):
    degree = {}
    if service < 0.0 or service > 1.0:
        degree["poor"] = 0
        degree["excellent"] = 0
        degree["good"] = 0
    if service <= .2:
        degree["poor"] = 1
        degree["excellent"] = 0
        degree["good"] = 0
    elif service > .2 and service < .4:
        degree["poor"] = float((.4 - service) * (1 / (.4 - .2)))
        degree["good"] = float((service - .2) * (1 / (.4 - .2)))
        degree["excellent"] = 0
    elif service >= .4 and service <= .6:
        degree["poor"] = 0
        degree["good"] = 1
        degree["excellent"] = 0
    elif service > .6 and service < .8:
        degree["poor"] = 0
        degree["excellent"] = float((.8 - service) * (1 / (.8 - .4)))
        degree["good"] = float((service - .4) * (1 / (.8 - .4)))
    elif service >= .8 and service <= 1.0:
        degree["poor"] = 0
        degree["excellent"] = 0
        degree["good"] = 1
    return degree


def getMembershipFood(food):
    degree = {}

    if food < 0 or food > 1:
        degree["b"] = 0
        degree["d"] = 0

    elif food <= .4:
        degree["b"] = 1
        degree["d"] = 0

    elif food > .4 and food < .8:
        degree["b"] = float((.8 - food) * (1 / (.8 - .4)))
        degree["d"] = float((food - .40) * 1.0 / (.80 - .40))

    elif food >= .80 and food <= 1:

        degree["b"] = 0
        degree["d"] = 1

    return degree


def crispInput(val, base):
    # print(val * (1.0 / (base)))
    return val * (1.0 / (base - 1))


def ruleEvalationAssessment(service, food):
    cheap = max(service["poor"], food["b"])
    average = service["good"]
    generous = max(service["excellent"], food["d"])

    return cheap, average, generous


def defuzzificationAssessment(cheap, average, generous):

    cheap1 = 0
    cheap1 += cheap * 0
    cheap1 += cheap * 0.05
    cheap1 += cheap * 1

    average1 = 0
    average1 += average * 0.8
    average1 += average * 1.4
    average1 += average * 1.6

    generous1 = 0
    generous1 += generous * 1.5
    generous1 += generous * 1.7
    generous1 += generous * 1.8

    numerator = cheap1 + average1 + generous1
    denominator = cheap + average + generous

    if denominator == 0:
        return 0
    else:
        return numerator / denominator


# input
ser, foodd = 6, 3

s = crispInput(ser, 10)
f = crispInput(foodd, 10)
fuzzyservice = getMembershipService(s)

fuzzyfood = getMembershipFood(f)
print("Service : ", fuzzyservice)
print("Food: ", fuzzyfood)

cheap, average, generous = ruleEvalationAssessment(fuzzyservice, fuzzyfood)
print("Cheap ", cheap, "Avg: ", average, "Generous: ", generous)
conAssessment = defuzzificationAssessment(cheap, average, generous)
print("Fuzzified Continuous Assessment: ", conAssessment)
