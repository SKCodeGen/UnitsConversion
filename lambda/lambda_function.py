import json
from pytemp import pytemp
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('event: {}'.format(event))

    units_conversion = 'invalid'
    try:
        units_conversion = verify_unit_conversion(event["queryStringParameters"]['source_unit'],
                                                       event["queryStringParameters"]['source_value'],
                                                       event["queryStringParameters"]['target_unit'],
                                                       event["queryStringParameters"]['target_value'])
    except:
        return get_result_with_status(400, units_conversion)

    return get_result_with_status(200, units_conversion)


def get_result_with_status(status, units_conversion):
    return {
        'statusCode': status,
        'body': json.dumps({
            "units conversion": units_conversion
        })
    }


def verify_unit_conversion(source_unit, source_value, target_unit, target_value):
    # doing the temp conversion using pytemp
    converted = pytemp(float(source_value), source_unit, target_unit)
    logger.info('Expected converted temp value: {}'.format(converted))

    # rounding to tenth place
    rounded_converted = round(converted, 1)
    rounded_inputted = round(float(target_value), 1)

    if rounded_converted == rounded_inputted:
        units_conversion = 'correct'
    else:
        units_conversion = 'incorrect'

    return units_conversion
