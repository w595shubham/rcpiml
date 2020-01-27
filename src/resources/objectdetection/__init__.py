import os
import tensorflow.compat.v1 as tf

root = os.path.abspath(__file__ + "/../../../")
PATH_TO_CKPT = os.path.join(root, 'trained_model', 'inference_graph', 'frozen_inference_graph.pb')

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    prediction_session = tf.Session(graph=detection_graph)

