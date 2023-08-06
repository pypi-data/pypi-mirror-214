import math

import numpy as np

from my_model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    #JUST CHECKING IF RESULT VALUE IS A FLOAT...

    # When
    result = make_prediction(input_data=sample_input_data)

    # Then

    assert isinstance(result[0], np.float64)
