"""Implements the main logic of ADLStream2 framework."""

import numpy as np
import logging
from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager
from typing import Callable, ContextManager, List, Optional, Tuple, Type, Union


class ADLStreamContext:
    """ADLStream2 context.
    This object is shared among training, predicting, stream-generator and validator processes.
    It is used to send the data from the stream generator to the predicting process,
    then it is used for training and finally the validator has access to the output predictions.
    Parameters:
        batch_size (int): Number of instances per batch.
        num_batches_fed (int): Maximun number of batches to be used for training.
        log_file (str, optional): Name of log file.
            If None, log will be printed on screen and will not be saved.
            If log_file is given, log level is set to "DEBUG". However if None,
            log level is kept as default.
            Defaults to None.
    """

    def __init__(
        self,
        batch_size: int,
        num_batches_fed: int,
        log_file: Optional[str] = None,
    ) -> None:

        self.batch_size = batch_size
        self.num_batches_fed = num_batches_fed

        self.time_out = False
        self.finished = False
        self.new_model_available = False
        self.output_size = None
        self.weights = None

        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

        self.y_eval = []
        self.o_eval = []
        self.x_eval = []

        self.data_lock = Lock()
        self.eval_lock = Lock()

        self.num_instances_to_train = num_batches_fed * batch_size

        self._configure_logging(log_file)

    def _configure_logging(self, log_file: str) -> None:
        if log_file is not None:
            with open(log_file, "w"):
                pass
            logging.basicConfig(
                filename=log_file,
                format="%(asctime)s %(levelname)-8s %(message)s",
                level=logging.DEBUG,
            )

    def log(
        self,
        level: str,
        message: str,
    ) -> None:
        """Log message.

        Args:
            level (str): Log level - "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
            message (str): Logging message.

        Raises:
            Exception: Level is not valid.
        """
        if level == "DEBUG":
            logging.debug(message)
        elif level == "INFO":
            logging.info(message)
        elif level == "WARNING":
            logging.warning(message)
        elif level == "ERROR":
            logging.error(message)
        elif level == "CRITICAL":
            logging.critical(message)
        else:
            raise Exception("{} is not a valid logging level".format(level))

    def get_batch_size(self) -> int:
        """Get the batch size.

        Returns:
            int: Batch size.
        """
        return self.batch_size

    def get_num_batches_fed(self) -> int:
        """Get the number of batches to fed for training.

        Returns:
            int: Number of batches to fed.
        """
        return self.num_batches_fed

    def set_time_out(self, time_out: bool = True) -> None:
        """Set time out to true by the stream generator.

        Args:
            time_out (bool, optional): Whether is time out. Defaults to True.
        """
        self.time_out = time_out

    def is_time_out(self) -> bool:
        """Whether the stream has timed out.

        Returns:
            bool: Time out.
        """
        return self.time_out

    def set_finished(self, finished: bool = True) -> None:
        """Indicate that the stream has finished.

        Args:
            finished (bool, optional): Whether the stream has finished. Defaults to True.
        """
        self.finished = finished

    def is_finished(self) -> bool:
        """Whether the stream has finished or not.

        Returns:
            bool: True if the stream has finished.
        """
        return self.finished

    def set_new_model_available(self, new_model_available: bool) -> None:
        """Indicate that there are new weights available for the model.

        Args:
            new_model_available (bool): True if there is a new model. False otherwise.
        """
        self.new_model_available = new_model_available

    def is_new_model_available(self) -> bool:
        """Whether there are updated weights available for the model.

        Returns:
            bool: True if there is a new model.
        """
        return self.new_model_available

    def get_output_size(self) -> int:
        """Get output size of the model (number of neurons of the last layer).

        Returns:
            int: output size.
        """
        return self.output_size

    def set_output_size(self, output_size: int) -> None:
        """Indicate the number of features of the output.

        Args:
            output_size (int): output size.
        """
        self.output_size = output_size

    def set_weights(self, w: List[np.ndarray]) -> None:
        """Update the model's weigths.

        Args:
            w (List[np.ndarray]): model's weights.
        """
        self.weights = w

    def get_weights(self) -> List[np.ndarray]:
        """Get the most updated model's weights.

        Returns:
            List[np.ndarray]: model's weights.
        """
        return self.weights

    def add(self, x: List[float], y: Optional[List[float]] = None):
        """Add a new instance from the stream.
        The instances will be added to the prediction buffer. The inputs (x) and outputs (y)
        do not need to arrive at the same time. However they have to arrive in the same order.
        So that the first output (y_0) corresponds to the first input (x_0).

        Args:
            x (List[float]): input instance of the model.
            y (List[float], optional): output intance of the model. Defaults to None.
        """
        with self.data_lock:
            if x is not None:
                if len(self.x_train) < self.batch_size:
                    # Fill initial training data
                    self.x_train.append(x)
                else:
                    # Get prediction before using it for training
                    self.x_test.append(x)

            if y is not None:
                if len(self.y_train) < self.batch_size:
                    # Fill initial training data
                    self.y_train.append(y)
                else:
                    self.y_test.append(y)

    def get_test_data(self) -> List[List[float]]:
        """Get the test data (prediction). Once the test data is provided to the
        prediction process, the data is added to the training buffer.

        Returns:
            List[List[float]]: X_test -- model's input.
        """
        X, y = [], []
        with self.data_lock:
            X = self.x_test
            y = self.y_test
            self.x_test, self.y_test = [], []
            self.x_train += X
            self.y_train += y
            with self.eval_lock:
                self.y_eval += y
                self.x_eval += X
        return X

    def get_remaining_test(self) -> int:
        """Get length of the test buffer.

        Returns:
            int: length of test buffer.
        """
        return len(self.x_test)

    def get_training_data(self) -> Tuple[List[List[float]], List[List[float]]]:
        """Get data for training the model.
        Returns a tuple with two lists such as (X_train, y_train). The length of both lists, is
        given by `min(len(y_train), batch_size*num_batches_fed)`. If the training buffer has more
        instance than the maximun (`batch_size*num_batches_fed`), it returns the newest instances.

        Returns:
            (List[List[float]], List[List[float]]): X_train, y_train
        """
        X, y = [], []

        with self.data_lock:
            X = self.x_train
            y = self.y_train
            if len(y) > self.num_instances_to_train:
                index = len(y) - self.num_instances_to_train
                X = X[index:]
                y = y[index:]
                self.x_train = X
                self.y_train = y
            elif len(y) < self.batch_size:
                return [], []

        return X[: len(self.y_train)], y

    def get_predictions(
        self,
    ) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
        """Returns the input instances (x), expected output (y) and models predictions(o).

        Returns:
            (List[List[float]], List[List[float]], List[List[float]]): (x, y, o)
        """
        with self.eval_lock:
            x_eval, self.x_eval = self.x_eval, []
            y_eval, self.y_eval = self.y_eval, []
            o_eval, self.o_eval = self.o_eval, []
        return x_eval, y_eval, o_eval

    def add_predictions(self, o_eval):
        o_eval = [list(p) for p in o_eval]
        with self.eval_lock:
            self.o_eval += o_eval


class ADLStreamManager(BaseManager):
    """ADLStream2 Manager
    Manager server which hold ADLStreamContext object.
    It allows other processes to manipulate the shared context.

    ```
    self.register("context", ADLStreamContext)
    ```
    """

    def __init__(self):
        super().__init__()
        self.register("context", ADLStreamContext)


class ADLStream:
    """ADLStream2.
    This is the main object of the framework.
    Based on a stream generator and a given deep learning model, it runs the training and
    predicting process in paralell (ideally in two different GPU) to obtain obtain accurate
    predictions as soon as an instance is received.
    Parameters:
        stream_generator (ADLStream2.data.BaseStreamGenerator):
            It is in charge of generating new instances from the stream.
        evaluator (ADLStream2.evaluator.BaseEvaluator):
            It will deal with the validation logic.
        batch_size (int): Number of instances per batch.
        num_batches_fed (int): Maximun number of batches to be used for training.
        model_architecture (str): Model architecture to use.
            Possible options can be found in ADLStream2.models.
        model_loss (tf.keras.Loss): Loss function to use.
            For references, check tf.keras.losses.
        model_optimizers (tf.keras.Optimizer, optional): It defines the training algorithm to use.
            Fore references, check tf.keras.optimizers.
            Defaults to "adam".
        model_parameters (dict, optional): It contains all the model-creation parameters.
            It depends on the model architecture chosen.
            Defaults to {}.
        train_gpu_index (int, optional): GPU index to be used fore training.
            Defaults to 0.
        predict_gpu_index (int, optional): GPU index to be used fore predicting.
            Defaults to 1.
        log_file (str, optional): Name of log file.
            If None, log will be printed on screen and will not be saved.
            If log_file is given, log level is set to "DEBUG". However if None,
            log level is kept as default.
            Defaults to None.
    """

    def __init__(
        self,
        stream_generator: Type["BaseStreamGenerator"],
        evaluator: Type["BaseEvaluator"],
        batch_size: int,
        num_batches_fed: int,
        model_architecture: str,
        model_loss: Union[str, Callable],
        model_optimizer: str = "adam",
        model_parameters: dict = {},
        train_gpu_index: int = 0,
        predict_gpu_index: int = 1,
        log_file: Optional[str] = None,
    ) -> None:
        self.stream_generator = stream_generator
        self.evaluator = evaluator
        self.batch_size = batch_size
        self.num_batches_fed = num_batches_fed
        self.model_architecture = model_architecture
        self.model_loss = model_loss
        self.model_optimizer = model_optimizer
        self.model_parameters = model_parameters
        self.train_gpu_index = train_gpu_index
        self.predict_gpu_index = predict_gpu_index
        self.log_file = log_file

        self.x_shape = None
        self.output_size = None
        self.weights = None

        self.manager = ADLStreamManager()

    def training_process(self, context: ADLStreamContext, gpu_index: int) -> None:
        """Training process.
        Args:
            context (ADLStreamContext): Shared object among processes.
            gpu_index (int): Index of the GPU to use for training
        """
        import tensorflow as tf
        from ADLStream2.models import create_model

        # Select GPU device
        gpus = tf.config.experimental.list_physical_devices("GPU")
        if len(gpus) > gpu_index:
            try:
                tf.config.experimental.set_visible_devices(gpus[gpu_index], "GPU")
                context.log(
                    "INFO",
                    "TRAINING-PROCESS - GPU device using: {}".format(gpus[gpu_index]),
                )
            except RuntimeError as e:
                context.log("ERROR", "TRAINING-PROCESS - {}".format(e))
        else:
            tf.config.experimental.set_visible_devices([], "GPU")
            context.log(
                "WARNING",
                "TRAINING-PROCESS - There are no enough GPU devices, using CPU",
            )

        model = None
        y_shape = None
        output_shape = None
        while not context.is_finished():
            X, y = context.get_training_data()
            if not X:
                continue

            X, y = np.asarray(X), np.asarray(y)

            if model is None:
                y_shape = y.shape

                output_shape = y.reshape(y_shape[0], -1).shape
                context.set_output_size(output_shape[-1])

                model = create_model(
                    self.model_architecture,
                    X.shape,
                    context.get_output_size(),
                    self.model_loss,
                    self.model_optimizer,
                    **self.model_parameters
                )
                self.x_shape = X.shape

            y = y.reshape((y.shape[0], context.get_output_size()))

            context.log(
                "INFO",
                "TRAINING-PROCESS - Training with the last {} instances".format(
                    X.shape[0]
                ),
            )
            model.fit(X, y, context.get_batch_size(), epochs=1, verbose=0)

            context.set_weights(model.get_weights())
            context.set_new_model_available(True)

        context.log("INFO", "TRAINING-PROCESS - Finished stream")

    def predicting_process(self, context: ContextManager, gpu_index: int) -> None:
        """Predicting process.
        Args:
            context (ADLStreamContext): Shared object among processes.
            gpu_index (int): Index of the GPU to use for training
        """
        import tensorflow as tf
        from ADLStream2.models import create_model

        # Select GPU device
        gpus = tf.config.experimental.list_physical_devices("GPU")
        if len(gpus) > gpu_index:
            try:
                tf.config.experimental.set_visible_devices(gpus[gpu_index], "GPU")
                context.log(
                    "INFO",
                    "PREDICTING-PROCESS - GPU device using: {}".format(gpus[gpu_index]),
                )
            except RuntimeError as e:
                context.log("ERROR", "PREDICTING-PROCESS - {}".format(e))
        else:
            tf.config.experimental.set_visible_devices([], "GPU")
            context.log(
                "WARNING",
                "PREDICTING-PROCESS - There are no enough GPU devices, using CPU",
            )

        # Wait until model is created and trained for the first time.
        while not context.is_new_model_available():
            if context.is_time_out():
                if not context.get_remaining_test() > 0:
                    context.log(
                        "INFO",
                        "PREDICTING-PROCESS - Time out, no instances were received. Finishing process.",
                    )
                    context.set_finished()
                    return
            pass

        context.log("INFO", "Starting predictions")

        model = None
        while True:
            X = context.get_test_data()

            if not X:
                if context.is_time_out():
                    context.set_finished(True)
                    context.log("INFO", "PREDICTING-PROCESS - Finished stream")
                    break
                continue

            X = np.asarray(X)

            if model is None:
                model = create_model(
                    self.model_architecture,
                    X.shape,
                    context.get_output_size(),
                    self.model_loss,
                    self.model_optimizer,
                    **self.model_parameters
                )

            if context.is_new_model_available():
                model.set_weights(context.get_weights())
                context.set_new_model_available(False)

            predictions = model.predict(X)
            context.log(
                "INFO", "PREDICTING-PROCESS: {} instances predicted.".format(X.shape[0])
            )

            context.add_predictions(predictions)

    def run(self) -> None:
        """Function that run ADLStream2.
        It run 4 different processes:
        - Training process.
        - Predicting process.
        - Stream generator process.
        - Evaluator process.
        """
        self.manager.start()
        context = self.manager.context(
            self.batch_size, self.num_batches_fed, log_file=self.log_file
        )

        process_stream = Process(
            target=self.stream_generator.run,
            args=[context],
        )
        process_train = Process(
            target=self.training_process, args=[context, self.train_gpu_index]
        )
        process_predict = Process(
            target=self.predicting_process, args=[context, self.predict_gpu_index]
        )
        process_evaluator = Process(target=self.evaluator.run, args=[context])

        process_stream.start()
        process_train.start()
        process_predict.start()
        process_evaluator.start()

        process_stream.join()
        process_train.join()
        process_predict.join()
        process_evaluator.join()

        self.output_size = context.get_output_size()
        self.weights = context.get_weights()

        self.manager.shutdown()

    def get_model(self) -> object:
        """Returns model with the latest weights.

        Returns:
            tf.model: Model.
        """
        from ADLStream2.models import create_model

        model = create_model(
            self.model_architecture,
            self.x_shape,
            self.output_size,
            self.model_loss,
            self.model_optimizer,
            **self.model_parameters
        )
        model.set_weights(self.weights)
        return model
