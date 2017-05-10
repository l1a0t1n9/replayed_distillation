# 784-1200-1200-10 model
# with 50% dropout on hidden and 20% on visible nodes
import tensorflow as tf
import numpy as np

def create_model(inp, out_size, keep_inp=0.8, keep=0.5, temp=1.0):
    with tf.variable_scope('784-1200-1200-10'):
        with tf.variable_scope('inp_drop'):
            inp_drop = tf.nn.dropout(inp, keep_prob=keep_inp)

        with tf.variable_scope('fc1'):
            w = tf.Variable(tf.truncated_normal([int(inp.get_shape()[-1]), 1200]), name='w')
            b = tf.Variable(tf.constant(0.1, shape=[1200]), name='b')
            z = tf.nn.relu(tf.matmul(inp_drop, w) + b, name='relu')
            z_drop = tf.nn.dropout(z, keep_prob=keep)

        with tf.variable_scope('fc2'):
            w = tf.Variable(tf.truncated_normal([1200, 1200]), name='w')
            b = tf.Variable(tf.constant(0.1, shape=[1200]), name='b')
            z = tf.nn.relu(tf.matmul(z_drop, w) + b, name='relu')
            z_drop = tf.nn.dropout(z, keep_prob=keep)

        with tf.variable_scope('fc3'):
            w = tf.Variable(tf.truncated_normal([1200, out_size]), name='w')
            b = tf.Variable(tf.constant(0.1, shape=[out_size]), name='b')
            h = tf.matmul(z_drop, w) + b

        with tf.variable_scope('temp'):
            h_soft = tf.div(h, temp)

    return h_soft

def create_constant_model(sess, inp, drop_dict):
    with tf.variable_scope('784-1200-1200-10_const'):
        with tf.variable_scope('inp_drop'):
            # mere rescaling
            #  inp = inp * 0.8
            # TODO NIPS: use drop_dict
            inp = tf.multiply(inp, drop_dict['drop_inp_var'])

        with tf.variable_scope('fc1'):
            w = tf.constant(sess.run('784-1200-1200-10/fc1/w:0'), name='w')
            b = tf.constant(sess.run('784-1200-1200-10/fc1/b:0'), name='b')
            z = tf.nn.relu(tf.matmul(inp, w) + b, name='relu')
            # mere rescaling
            #  z = z * 0.5
            # TODO NIPS: use drop_dict
            z = tf.multiply(z, drop_dict['drop_fc1_var'])

        with tf.variable_scope('fc2'):
            w = tf.constant(sess.run('784-1200-1200-10/fc2/w:0'), name='w')
            b = tf.constant(sess.run('784-1200-1200-10/fc2/b:0'), name='b')
            z = tf.nn.relu(tf.matmul(z, w) + b, name='relu')
            #  z = z * 0.5
            # TODO NIPS: use drop_dict
            z = tf.multiply(z, drop_dict['drop_fc2_var'])

        with tf.variable_scope('fc3'):
            w = tf.constant(sess.run('784-1200-1200-10/fc3/w:0'), name='w')
            b = tf.constant(sess.run('784-1200-1200-10/fc3/b:0'), name='b')
            h = tf.matmul(z, w) + b

    return h

