import tensorflow as tf

class EchoStateLayer(tf.keras.layers.Layer):
    """Custom Echo State Network Layer."""
    def __init__(self, units, return_sequences=False, **kwargs):
        super(EchoStateLayer, self).__init__(**kwargs)
        self.units = units
        self.return_sequences = return_sequences
        self.state = None

    def build(self, input_shape):
        self.input_dim = input_shape[-1]
        self.W_in = self.add_weight(
            shape=(self.input_dim, self.units),
            initializer="uniform",
            trainable=False,
            name="W_in",
        )
        self.W_res = self.add_weight(
            shape=(self.units, self.units),
            initializer="uniform",
            trainable=False,
            name="W_res",
        )
        self.b = self.add_weight(
            shape=(self.units,),
            initializer="zeros",
            trainable=False,
            name="bias",
        )
        super(EchoStateLayer, self).build(input_shape)

    def call(self, inputs):
        batch_size = tf.shape(inputs)[0]
        timesteps = tf.shape(inputs)[1]
        if self.state is None:
            self.state = tf.zeros((batch_size, self.units))

        outputs = []
        for t in range(timesteps):
            input_t = inputs[:, t, :]
            self.state = tf.nn.tanh(
                tf.matmul(input_t, self.W_in) + tf.matmul(self.state, self.W_res) + self.b
            )
            outputs.append(self.state)

        outputs = tf.stack(outputs, axis=1)
        if self.return_sequences:
            return outputs
        else:
            return outputs[:, -1, :]

    def compute_output_shape(self, input_shape):
        if self.return_sequences:
            return (input_shape[0], input_shape[1], self.units)
        else:
            return (input_shape[0], self.units)

def ESN(
    input_shape,
    output_size,
    loss,
    optimizer,
    recurrent_units=[64],
    return_sequences=False,
    dense_layers=[32],
    dense_dropout=0,
    out_activation="linear",
):
    """Echo State Network (ESN).

    Args:
        input_shape (tuple): Shape of the input data.
        output_size (int): Number of neurons of the last layer.
        loss (tf.keras.Loss): Loss to be used for training.
        optimizer (tf.keras.Optimizer): Optimizer that implements the training algorithm.
        recurrent_units (list, optional): Number of recurrent units for each ESN layer.
            Defaults to [64].
        return_sequences (bool, optional): Whether to return the last output in the output sequence or the full sequence.
            Defaults to False.
        dense_layers (list, optional): List with the number of hidden neurons for each
            layer of the dense block before the output. Defaults to [32].
        dense_dropout (float between 0 and 1, optional): Fraction of the dense units to drop. Defaults to 0.0.
        out_activation (tf activation function, optional): Activation of the output layer.
            Defaults to "linear".

    Returns:
        tf.keras.Model: ESN model.
    """
    input_shape = input_shape[-len(input_shape) + 1:]
    inputs = tf.keras.layers.Input(shape=input_shape)

    x = inputs
    if len(input_shape) < 2:
        x = tf.keras.layers.Reshape((inputs.shape[1], 1))(x)

    # ESN layers
    for i, u in enumerate(recurrent_units):
        return_sequences_tmp = (
            return_sequences if i == len(recurrent_units) - 1 else True
        )
        x = EchoStateLayer(u, return_sequences=return_sequences_tmp)(x)

    # Dense layers
    if return_sequences:
        x = tf.keras.layers.Flatten()(x)
    for hidden_units in dense_layers:
        x = tf.keras.layers.Dense(hidden_units)(x)
        if dense_dropout > 0:
            x = tf.keras.layers.Dropout(dense_dropout)(x)
    x = tf.keras.layers.Dense(output_size, activation=out_activation)(x)

    model = tf.keras.Model(inputs=inputs, outputs=x)
    model.compile(optimizer=optimizer, loss=loss)

    return model
