import tensorflow as tf


class Regressor(tf.keras.Model):
    def __init__(self, name=None, dtype=None) -> None:
        super().__init__(name=name, dtype=dtype)
