import json
import logging
import os

import cv2
import numpy
from flask import Blueprint
from flask_restplus import Api, Resource
from pyzbar import pyzbar
from werkzeug.datastructures import FileStorage

from src.infrastructure.logging.initialize import LoggerAdapter
from src.infrastructure.security.middleware.secureroute import secureroute
from src.resources.objectdetection import prediction_session
from src.utilities.label_map_util import load_labelmap, convert_label_map_to_categories, create_category_index
from src.utilities.utilities import get_predictions

object_detection_blueprint = Blueprint('objectdetection', __name__)
api = Api(object_detection_blueprint, doc='/objectdetection/docs')

ns_object_detection = api.namespace('objectdetection', description='Identify individual freight car components')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@ns_object_detection.route('/')
class CarPartRelationshipHierarchies(Resource):
    @secureroute()
    def post(self):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            args = upload_parser.parse_args()
            uploaded_file = args['file']  # This is FileStorage instance

            # Identify individual freight car components
            logger.info("Identify individual freight car components start")

            root = os.path.abspath(__file__ + "/../../../")
            PATH_TO_LABELS = os.path.join(root, 'trained_model', 'training', 'labelmap.pbtxt')

            label_map = load_labelmap(PATH_TO_LABELS)
            categories = convert_label_map_to_categories(label_map, max_num_classes=7, use_display_name=True)
            category_index = create_category_index(categories)

            logger.info('Predicting image start')
            image_bytes = cv2.imdecode(numpy.fromstring(uploaded_file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
            predictions = get_predictions(prediction_session, image_bytes, category_index)
            logger.info('Predicting image end')

            return json.loads(json.dumps(predictions)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}


@ns_object_detection.route('/decodebarcode')
class BarCodeDetection(Resource):
    @secureroute()
    def post(self):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            args = upload_parser.parse_args()
            uploaded_file = args['file']  # This is FileStorage instance

            # load the input image
            image_bytes = cv2.imdecode(numpy.fromstring(uploaded_file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

            # find the barcodes in the image and decode each of the barcodes
            barcodes = pyzbar.decode(image_bytes)

            detected_barcodes = []
            # loop over the detected barcodes
            for barcode in barcodes:
                detected_barcodes.append(barcode.data.decode("utf-8"))
            return json.loads(json.dumps(detected_barcodes)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}
