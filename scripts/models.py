#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is describing a ConvNet model, with its parameters could be set 
at 'param.py'. It takes multi-inputs which are TWO-channels and meta information 
such as 'inc_angle'.

@author: cttsai (Chia-Ta Tsai), @Oct 2017
"""
import numpy as np
import random as rand
import math

from keras.layers import Activation, Dense, Dropout, Flatten
from keras.layers import BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, Input
from keras.layers import GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.layers.merge import Concatenate
from keras.models import Model, load_model
from keras.optimizers import Adam


def model_test(**config):
    """ Quick model for testing."""

    lr = config.get('lr', 8e-5)
    decay = config.get('decay', 1e-6)
    relu_type = config.get('relu_type', 'relu')

    input_1 = Input(shape=(75, 75, 3))

    fcnn = BatchNormalization()(input_1)
    fcnn = Conv2D(8, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((5, 5))(fcnn)
    fcnn = BatchNormalization()(fcnn)

    fcnn = Flatten()(fcnn)

    dense = Dropout(0.2)(fcnn)
    dense = Dense(5, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)

    output = Dense(1, activation="sigmoid")(dense)

    model = Model(input_1, output)

    optim = Adam(lr=lr, decay=decay)
    model.compile(
        optimizer=optim, loss="binary_crossentropy", metrics=["accuracy"])
    return model


def model0(**config):
    """ Bandwidth model from the kernel keras0.18lb - managed to 
    produce 0.16 when trained with data augumentation."""

    lr = config.get('lr', 8e-5)
    decay = config.get('decay', 1e-6)
    relu_type = config.get('relu_type', 'relu')
    channels = config.get('channels', 3)

    input_1 = Input(shape=(75, 75, channels))

    fcnn = BatchNormalization()(input_1)
    fcnn = Conv2D(32, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((3, 3))(fcnn)
    fcnn = BatchNormalization()(fcnn)

    fcnn = Conv2D(64, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = BatchNormalization()(fcnn)
    fcnn = Dropout(0.1)(fcnn)

    fcnn = Conv2D(128, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = Dropout(0.2)(fcnn)

    fcnn = Conv2D(128, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = Dropout(0.2)(fcnn)
    fcnn = BatchNormalization()(fcnn)

    fcnn = Flatten()(fcnn)

    dense = Dropout(0.2)(fcnn)
    dense = Dense(256, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)
    dense = Dense(128, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)
    dense = Dense(64, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)

    output = Dense(1, activation="sigmoid")(dense)

    model = Model(input_1, output)

    optim = Adam(lr=lr, decay=decay)
    model.compile(
        optimizer=optim, loss="binary_crossentropy", metrics=["accuracy"])
    return model


def model1_wider(**config):
    """ Bandwidth model from the kernel keras0.18lb - managed to 
    produce 0.16 when trained with data augumentation."""

    lr = config.get('lr', 8e-5)
    decay = config.get('decay', 1e-6)
    relu_type = config.get('relu_type', 'relu')
    channels = config.get('channels', 3)

    input_1 = Input(shape=(75, 75, channels))

    fcnn = BatchNormalization()(input_1)
    fcnn = Conv2D(32, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((3, 3))(fcnn)
    fcnn = BatchNormalization()(fcnn)

    fcnn = Conv2D(64, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = BatchNormalization()(fcnn)
    fcnn = Dropout(0.1)(fcnn)

    fcnn = Conv2D(256, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = Dropout(0.2)(fcnn)

    fcnn = Conv2D(128, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = Dropout(0.2)(fcnn)
    fcnn = BatchNormalization()(fcnn)

    fcnn = Flatten()(fcnn)

    dense = Dropout(0.2)(fcnn)
    dense = Dense(256, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)
    dense = Dense(128, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)
    dense = Dense(64, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)

    output = Dense(1, activation="sigmoid")(dense)

    model = Model(input_1, output)

    optim = Adam(lr=lr, decay=decay)
    model.compile(
        optimizer=optim, loss="binary_crossentropy", metrics=["accuracy"])
    return model


def model1_meta(**config):
    """ Bandwidth model from the kernel keras0.18lb - managed to 
    produce 0.16 when trained with data augumentation."""

    lr = config.get('lr', 8e-5)
    decay = config.get('decay', 1e-6)
    relu_type = config.get('relu_type', 'relu')
    channels = config.get('channels', 3)

    input_1 = Input(shape=(75, 75, channels))

    fcnn = Conv2D(
        32, kernel_size=(3, 3),
        activation=relu_type)(BatchNormalization()(input_1))
    fcnn = MaxPooling2D((3, 3))(fcnn)
    fcnn = BatchNormalization()(fcnn)

    fcnn = Conv2D(64, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = BatchNormalization()(fcnn)
    fcnn = Dropout(0.1)(fcnn)

    fcnn = Conv2D(128, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = Dropout(0.2)(fcnn)

    fcnn = Conv2D(
        128, kernel_size=(3, 3), activation=relu_type, padding='same')(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = Dropout(0.2)(fcnn)
    fcnn = BatchNormalization()(fcnn)

    fcnn = Flatten()(fcnn)

    input_2 = Input(shape=[1], name='angle')
    input_2_bn = BatchNormalization()(input_2)

    fcnn = Concatenate()([fcnn, input_2_bn])

    dense = Dense(256, activation=relu_type)(fcnn)
    dense = Dropout(0.2)(dense)
    dense = Dense(128, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)
    dense = Dense(64, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)

    output = Dense(1, activation="sigmoid")(dense)

    model = Model([input_1, input_2], output)

    optim = Adam(lr=lr, decay=decay)
    model.compile(
        optimizer=optim, loss="binary_crossentropy", metrics=["accuracy"])
    return model


def model2_meta(**config):
    """ Bandwidth model from the kernel keras0.18lb - managed to 
    produce 0.16 when trained with data augumentation."""

    lr = config.get('lr', 8e-5)
    decay = config.get('decay', 1e-6)
    relu_type = config.get('relu_type', 'relu')
    channels = config.get('channels', 3)

    input_1 = Input(shape=(75, 75, channels))

    fcnn = Conv2D(
        32, kernel_size=(3, 3),
        activation=relu_type)(BatchNormalization()(input_1))
    fcnn = MaxPooling2D((3, 3))(fcnn)
    fcnn = BatchNormalization()(fcnn)
    fcnn_1 = Dropout(0.1)(fcnn)

    #Path 1
    fcnn = Conv2D(128, kernel_size=(3, 3), activation=relu_type)(fcnn_1)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = Dropout(0.2)(fcnn)

    fcnn = Conv2D(128, kernel_size=(3, 3), activation=relu_type)(fcnn)
    fcnn = MaxPooling2D((2, 2), strides=(2, 2))(fcnn)
    fcnn = Dropout(0.2)(fcnn)
    fcnn = BatchNormalization()(fcnn)

    fcnn = Flatten()(fcnn)

    #Path 2
    fcnn_2 = Conv2D(64, kernel_size=(3, 3), activation=relu_type)(fcnn_1)
    fcnn_2 = BatchNormalization()(fcnn_2)

    fcnn_2 = Conv2D(128, kernel_size=(3, 3), activation=relu_type)(fcnn_2)
    fcnn_2 = BatchNormalization()(fcnn_2)

    fcnn_2 = Conv2D(
        256, kernel_size=(3, 3), activation=relu_type, padding='same')(fcnn_2)
    fcnn_2 = BatchNormalization()(fcnn_2)

    fcnn_2 = Conv2D(
        512, kernel_size=(3, 3), activation=relu_type, padding='same')(fcnn_2)
    fcnn_2 = Dropout(0.2)(fcnn_2)
    fcnn_2 = BatchNormalization()(fcnn_2)

    fcnn_2 = Conv2D(
        256, kernel_size=(3, 3), activation=relu_type, padding='same')(fcnn_2)
    fcnn_2 = MaxPooling2D((2, 2), strides=(2, 2))(fcnn_2)
    fcnn_2 = Dropout(0.2)(fcnn_2)
    fcnn_2 = BatchNormalization()(fcnn_2)

    fcnn_2 = Conv2D(
        64, kernel_size=(3, 3), activation=relu_type, padding='same')(fcnn_2)
    fcnn_2 = MaxPooling2D((2, 2), strides=(2, 2))(fcnn_2)
    fcnn_2 = Dropout(0.2)(fcnn_2)
    fcnn_2 = BatchNormalization()(fcnn_2)

    fcnn_2 = Flatten()(fcnn_2)

    input_2 = Input(shape=[1], name='angle')
    input_2_bn = BatchNormalization()(input_2)

    fcnn = Concatenate()([fcnn, fcnn_2, input_2_bn])

    dense = Dense(256, activation=relu_type)(fcnn)
    dense = Dropout(0.2)(dense)
    dense = Dense(128, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)
    dense = Dense(64, activation=relu_type)(dense)
    dense = Dropout(0.2)(dense)

    output = Dense(1, activation="sigmoid")(dense)

    model = Model([input_1, input_2], output)

    optim = Adam(lr=lr, decay=decay)
    model.compile(
        optimizer=optim, loss="binary_crossentropy", metrics=["accuracy"])
    return model


models = [model0]

if __name__ == '__main__':
    config = {'lr': 1, 'decay': .1, 'rely_type': 'relu'}
    for model in models:
        model(**config).summary()
