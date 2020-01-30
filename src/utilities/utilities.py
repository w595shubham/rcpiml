import base64
import datetime
import sqlite3

import cv2
import numpy as np

from src import logger, app
from src.constants import sql_object
from src.utilities.visualization_utils import visualize_boxes_and_labels_on_image_array


def get_predictions(session, image_bytes, category_index):
    image_tensor = session.graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = session.graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = session.graph.get_tensor_by_name('detection_scores:0')
    detection_classes = session.graph.get_tensor_by_name('detection_classes:0')
    num_detections = session.graph.get_tensor_by_name('num_detections:0')

    image_expanded = np.expand_dims(image_bytes, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = session.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    visualize_boxes_and_labels_on_image_array(
        image_bytes,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=2,
        min_score_thresh=0.90)

    # Convert image ndarray to encoded image and then get image bytes
    success, encoded_image = cv2.imencode('.jpg', image_bytes)
    # Convert image image bytes to base64 encoded string
    image_bytes_string = base64.b64encode(encoded_image.tobytes())

    predictions = []
    for class_index, score, box in zip(np.squeeze(classes).astype(np.int32), np.squeeze(scores), np.squeeze(boxes)):
        if int(100 * score) >= 90:
            predictions.append({
                'part': str(category_index[class_index]['name']),
                'probability': str(int(100 * score)),
                'coordinates': get_xy_coordinates(box, image_bytes)
            })

    return {
        'predictions': predictions,
        'imagebytes': str(image_bytes_string).replace("b\'", "data:image/jpeg;base64,").replace("\'", ""),
    }


def get_xy_coordinates(box, image_bytes):
    image_height = image_bytes.shape[0]
    image_width = image_bytes.shape[1]

    reversed_box = box[::-1]
    xmax = round(reversed_box[0] * image_width)
    ymax = round(reversed_box[1] * image_height)
    xmin = round(reversed_box[2] * image_width)
    ymin = round(reversed_box[3] * image_height)

    return {
        'xmin': xmin,
        'ymin': ymin,
        'xmax': xmax,
        'ymax': ymax,
    }


def has_user_expired(username):
    # Check if user is expired or not
    logger.info("Check if user is expired or not")
    now = datetime.datetime.now()

    # Create database connection with sqlite database
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_FILE'])
    cursor = conn.cursor()
    updated_query = sql_object.UPDATE_LAST_ACTIVE_USER_BY_NAME.format(now, username, now)
    logger.info("UPDATE_LAST_ACTIVE_USER_BY_NAME query %s", updated_query)

    # Execute query and fetch result
    rows_affected = cursor.execute(updated_query)
    conn.commit()
    return rows_affected.rowcount == 0 if True else False
