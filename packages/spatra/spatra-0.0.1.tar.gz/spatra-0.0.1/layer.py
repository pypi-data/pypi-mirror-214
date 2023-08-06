import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class GlobalTransform(nn.Module):
    """ The GlobalTransform layer enables global transformations of input signals.
    These transformations are parameterized by a 2x3 matrix and are applied to
    all elements of the input signal, e.g., to all pixels in an image.

    :param mode: The mode specifies the processing of the 2x3 transformation matrix.
                 We support the following values:

             - ``vanilla``: The global transformation follows the behaviour
               of the original Spatial Transformer by
               (`Jaderberg et. al <https://arxiv.org/abs/1506.02025>`_)

             - ``diffeo``: Implements an invertible affine transformation
               using a matrix exponential on the transformation matrix following
               (`Detlefsen et. al <https://ieeexplore.ieee.org/document/8578561>`_)

    :type mode: str

    :raises ValueError: If an invalid `mode` is provided.

    The behavior of the object depends on the selected mode.

    """

    def __init__(self, mode='vanilla'):
        """ Initializes the GlobalTransform object.
        """
        super(GlobalTransform, self).__init__()
        self.mode = mode

    @staticmethod
    def _transform(signal: torch.tensor, t_matrix: torch.tensor) -> torch.tensor:
        """ This applies a global affine transformation to the input signal
        parameterized by the transformation matrix.

        :param signal: Input signal, i.e., an image of shape (batch x channel x height x width)
        :param t_matrix: transformation matrix of shape (batch x 2 x 3)

        :return: transformed input signal of shape (batch x channel x height x width)
        """
        grid = F.affine_grid(t_matrix, signal.size())
        signal = F.grid_sample(signal, grid)
        return signal

    @staticmethod
    def _diffeomorphism(t_matrix: torch.tensor) -> torch.tensor:
        """ This renders the transformation matrix to a diffeomorphic transformation.

        :param t_matrix: transformation matrix of shape (batch x 2 x 3)

        :return: diffeomorphic transformation matrix of shape (batch x 2 x 3)
        """
        # add constant row for square matrix
        matrix_fill = torch.zeros(t_matrix.shape[0], 1, 3).to(t_matrix.device)
        theta = torch.concat([t_matrix, matrix_fill], dim=1)
        theta = torch.linalg.matrix_exp(theta)
        return theta[:, :2, :]

    def _apply_mode(self, t_matrix: torch.tensor) -> torch.tensor:
        """ Applies the specified mode to the transformation matrix.

        :param t_matrix: transformation matrix of shape (batch x 2 x 3)

        :return: new transformation matrix of shape (batch x 2 x 3)

        :raises ValueError: If an invalid `mode` is provided.
        """
        if self.mode == 'vanilla':
            return t_matrix
        elif self.mode == 'diffeo':
            return self.diffeomorphism(t_matrix)
        else:
            raise ValueError('Invalid mode!')

    def forward(self, signal: torch.tensor, t_matrix: torch.tensor) -> torch.tensor:
        """ Forwards the signal through the transformation.

        :param signal: Input signal, i.e., an image of shape (batch x channel x height x width)
        :param t_matrix: transformation matrix of shape (batch x 2 x 3)

        :return: transformed input signal of shape (batch x channel x height x width)
        """
        t_matrix = self.apply_mode(t_matrix)
        return self.affine_transformation(signal, t_matrix)
