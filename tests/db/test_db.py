import os


def test_piccolo_diagnose():
    piccolo_diagnose = "piccolo --diagnose"
    diagnosis = os.system(piccolo_diagnose)
    assert diagnosis == 0
