# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_activation']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.0.0']

setup_kwargs = {
    'name': 'torch-activation',
    'version': '0.1.1',
    'description': 'A library of new activation function implement in PyTorch to save time in experiment and have fun',
    'long_description': '# :zap: PyTorch Activations :zap:\n\nA collection of activation functions for the PyTorch library. This project is designed for ease of use during experimentation with different activation functions (or simply for fun :wink:). \n\n\n## Installation\n\n```bash\n$ pip install torch-activation\n```\n\n## Usage\n\nTo use the activation functions, simply import from `torch_activation`:\n\n```python\nfrom torch_activation import ShiLU\n\nm = ShiLU(inplace=True)\nx = torch.rand(16, 3, 384, 384)\nm(x)\n```\n\nList of available functions below.\n\n\n## Available Functions\n\n| Activation Functions   | Equations |\n|-|-|\n| **ReLU Variations** ||\n| ShiLU [[1]](#1) |$\\alpha \\cdot \\text{ReLU}(x) + \\beta$|\n| ReLUN [[1]](#1) |$\\min(\\text{ReLU}(x), n)$|\n| CReLU [[2]](#2) |$\\text{ReLU}(x) \\oplus \\text{ReLU}(-x)$|\n| SquaredReLU [[5]](#5) |$\\text{ReLU}(x)^2$|\n| StarReLU [[8]](#8) |$s \\cdot \\text{ReLU}(x)^2 + b$|\n\n| **GLU Variations** ||\n|-|-|\n| ReGLU [[6]](#6) |$\\text{ReLU} (xW + b) \\odot (xV + c)$|\n| GeGLU [[6]](#6) |$\\text{GeLU} (xW + b) \\odot (xV + c)$|\n| SwiGLU [[6]](#6) |$\\sigma (xW + b) \\odot (xV + c)$|\n| SeGLU |$\\text{SELU} (xW + b) \\odot (xV + c)$|\n\n| **Composite Functions** ||\n|-|-|\n| DELU [[1]](#1) |$\\text{if }  x \\leqslant 0 \\text{, SiLU}(x); \\text{ else, } x(n-1)$|\n| DReLUs |$\\text{if }  x \\leqslant 0 \\text{, } \\alpha (e ^ x -1); \\text{ else, }  x$|\n\n| **Trigonometry Based** ||\n|-|-|\n| GCU [[3]](#3) |$x \\cdot \\cos(x)$|\n| CosLU [[1]](#1) |$(x + \\alpha \\cdot \\cos(\\beta x)) \\cdot \\sigma(x)$|\n| SinLU |$(x + \\alpha \\cdot \\sin (\\beta x)) \\cdot \\sigma (x)$|\n\n| **Others** ||\n|-|-|\n| ScaledSoftSign [[1]](#1) |$\\frac{\\alpha \\cdot x}{\\beta + \\|x\\|}$|\n| CoLU [[4]](#4) |$\\frac{x}{1-x \\cdot e^{-(x + e^x)}}$|\n\n| **Linear Combination** ||\n|-|-|\n| LinComb [[7]](#7) |$\\sum_{i=1}^{n} w_i \\cdot F_i(x)$|\n| NormLinComb [[7]](#7) |$\\frac{\\sum_{i=1}^{n} w_i \\cdot F_i(x)}{\\|\\|W\\|\\|}$|\n\n\n## Contact\n\nAlan Huynh - [LinkedIn](https://www.linkedin.com/in/alan-huynh-64b357194/) - hdmquan@outlook.com\n\nProject Link: [https://github.com/alan191006/torch_activation](https://github.com/alan191006/torch_activation)\n\n\n## References\n<a id="1">[1]</a>\nPishchik, E. (2023). Trainable Activations for Image Classification. Preprints.org, 2023010463. DOI: 10.20944/preprints202301.0463.v1.\n\n<a id="2">[2]</a>\nShang, W., Sohn, K., Almeida, D., Lee, H. (2016). Understanding and Improving Convolutional Neural Networks via Concatenated Rectified Linear Units. arXiv:1603.05201v2 (cs).\n\n<a id="3">[3]</a>\nNoel, M. M., Arunkumar, L., Trivedi, A., Dutta, P. (2023). Growing Cosine Unit: A Novel Oscillatory Activation Function That Can Speedup Training and Reduce Parameters in Convolutional Neural Networks. arXiv:2108.12943v3 (cs).\n\n<a id="4">[4]</a>\nVagerwal, A. (2021). Deeper Learning with CoLU Activation. arXiv:2112.12078v1 (cs).\n\n<a id="5">[5]</a>\nSo, D. R., Mańke, W., Liu, H., Dai, Z., Shazeer, N., Le, Q. V. (2022). Primer: Searching for Efficient Transformers for Language Modeling. arXiv:2109.08668v2 (cs)\n\n<a id="6">[6]</a>\nNoam, S. (2020). GLU Variants Improve Transformer. arXiv:2002.05202v1 (cs)\n\n<a id="7">[7]</a>\nPishchik, E. (2023). Trainable Activations for Image Classification. Preprints.org, 2023010463. DOI: 10.20944/preprints202301.0463.v1\n\n<a id="8">[8]</a>\nWeihao, Y., et al (2022). MetaFormer Baselines for Vision. arXiv:2210.13452v2 (cs)\n\n[Back to top](#Installation)',
    'author': 'Alan Huynh',
    'author_email': 'hdmquan@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
