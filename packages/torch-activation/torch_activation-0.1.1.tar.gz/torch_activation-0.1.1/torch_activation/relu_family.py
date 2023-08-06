import torch
import torch.nn as nn
import torch.nn.functional as F

from torch import Tensor


class ShiLU(nn.Module):
    r"""
    Applies the ShiLU activation function:

    :math:`\text{ShiLU}(x) = \alpha \cdot \text{ReLU}(x) + \beta`

    Args:
        alpha : Scaling factor for the positive part of the input. Default: 1.0.
        beta : Bias term added to the output. Default: 0.0.
        inplace: can optionally do the operation in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.
        
    Attributes:
        alpha : Scaling factor for the positive part of the input. Default: 1.0.
        beta : Bias term added to the output. Default: 0.0.

    .. image:: ../images/activation_images/ShiLU.png

    Examples::
    
        >>> m = ShiLU(alpha=2.0, beta=1.0)
        >>> x = torch.randn(2)
        >>> output = m(x)

        >>> m = ShiLU(inplace=True)
        >>> x = torch.randn(2, 3, 4)
        >>> m(x)
    """

    def __init__(self, alpha=1.0, beta=0.0, inplace=False):
        super().__init__()
        self.alpha = nn.Parameter(torch.tensor(alpha))
        self.beta  = nn.Parameter(torch.tensor(beta))
        self.inplace = inplace

    def forward(self, x) -> Tensor:
        if self.inplace:
            F.relu_(x)
            x.mul_(self.alpha)
            x.add_(self.beta)
            return x
        else:    
            return self.alpha * F.relu(x) + self.beta
        

class CReLU(nn.Module):
    r"""
    Applies the Concatenated Rectified Linear Unit activation function.

    :math:`\text{CReLU}(x) = \text{ReLU}(x) \oplus \text{ReLU}(-x)`

    Args:
        dim: Dimension along which to concatenate in the output tensor. Default: 1
        inplace: can optionally do the operation in-place. Default: ``False``

    Shape:
        - Input: :math:`(*, C, *)` where :math:`*` means any number of additional dimensions
        - Output: :math:`(*, 2C, *)`

    Examples::

        >>> m = nn.CReLU()
        >>> x = torch.randn(2, 3)
        >>> output = m(x)
        
        >>> m = CReLU(inplace=True)
        >>> x = torch.randn(2, 3, 4)
        >>> m(x)
    """
    
    
    def __init__(self, dim=0):
        super(CReLU, self).__init__()
        self.dim = dim

    def forward(self, x) -> Tensor:
        return F.relu(torch.cat((x, -x), dim=self.dim))
        
        
class ReLUN(nn.Module):
    r"""Applies the element-wise function:

    :math:`\text{ReLUN}(x) = \min(\text{ReLU}(x), n)`

    Args:
        n: Upper bound for the function's output. Default is 1.0.
        inplace: can optionally do the operation in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.
        
    Attributes:
        n: Upper bound for the function's output. Default is 1.0.
        
    Examples::

        >>> m = nn.ReLUN(n=6.0) # ReLU6
        >>> x = torch.randn(2)
        >>> output = m(x)
        
        >>> m = nn.ReLUN(inplace=True)
        >>> x = torch.randn(2)
        >>> m(x)

    """
    def __init__(self, n=1.0, inplace=False):
        super(ReLUN, self).__init__()
        self.n = nn.Parameter(torch.tensor(n))
        self.inplace = inplace

    def forward(self, x) -> Tensor:
        if self.inplace:
            x.clamp_max_(self.n.data)
            x.relu_()
            return x
        else:
            return torch.clamp(x, 0, self.n.data)
        
        
class SquaredReLU(nn.Module):
    r"""
    Applies the element-wise function:

    :math:`\text{SquaredReLU}(x) = \text{ReLU}(x)^2`

    Args:
        inplace: can optionally do the operation in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.

    Examples::

        >>> m = nn.SquaredReLU()
        >>> x = torch.randn(2)
        >>> output = m(x)

        >>> m = nn.SquaredReLU(inplace=True)
        >>> x = torch.randn(2)
        >>> m(x)
    """
    
    
    def __init__(self, inplace=False):
        super().__init__()
        self.inplace = inplace

    def forward(self, x) -> Tensor:
        if self.inplace:
            return F.relu_(x).pow_(2)
        else:
            return F.relu(x).pow(2)
        
class StarReLU(nn.Module):
    r"""
    Applies the element-wise function:

    :math:`\text{StarReLU}(x) = s \cdot \text{ReLU}(x)^2 + b`

    Args:
        inplace: can optionally do the operation in-place. Default: ``False``
        s: Scaled factor for StarReLU, shared across channel. Default: 0.8944
        b: Bias term for StarReLU, shared across channel. Default: -0.4472

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.
        
    .. image:: ../images/activation_images/SquaredReLU.png

    Examples::

        >>> m = nn.StarReLU(s=1.0, b=0.0)
        >>> x = torch.randn(3, 384, 384)
        >>> output = m(x)

        >>> m = nn.StarReLU(learnable=True, inplace=True)
        >>> x = torch.randn(3, 384, 384)
        >>> m(x)
    """
    
    
    def __init__(self, s=0.8944, b=-0.4472, learnable=True, inplace=False):
        super().__init__()
        self.inplace = inplace
        if learnable:
            self.s = nn.Parameter(torch.tensor(s))
            self.b = nn.Parameter(torch.tensor(b))
        else:
            self.s = torch.tensor(s)
            self.b = torch.tensor(b)
        

    def forward(self, x) -> Tensor:
        if self.inplace:
            return F.relu_(x).pow_(2) \
                             .mul_(self.s) \
                             .add_(self.b)
        else:
            return self.s * F.relu(x).pow(2) + self.b
    
    
if __name__ == '__main__':
    pass