"""
Module for audio classification
"""
from pyara.Model.model import model_eval
from pyara.audio_prepare import prediction, prepare_signal
from pyara.config import CFG


def predict_audio(file_path):
    """
    Function for audio syntesized / bonafide prediction

    :param file_path: path to the file
    :return: prediction about audio
    0: if bonafide voice
    1: if syntesized voice
    """

    # Model to predict
    model = model_eval()
    signal = prepare_signal(file_path, width=CFG.width)

    prediction_of_model = prediction(model, signal)

    return prediction_of_model


if __name__ == '__main__':
    print(predict_audio("mozila11_1.wav"))
