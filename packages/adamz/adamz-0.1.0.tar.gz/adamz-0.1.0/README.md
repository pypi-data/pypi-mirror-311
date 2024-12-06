# AdamZ 
A PyTorch implementation of AdamZ, an enhanced variant of the widely-used Adam optimizer, that is designed to improve upon its predecessor by offering more efficient convergence and potentially better generalization capabilities across various neural network training tasks.

#### Prerequisites

- Python 3.9 or later
- PyTorch 2.5.1

### Usage
Instantiate the AdamZ optimizer similarly to other standard optimizers, ensuring you configure the hyperparameters to suit your specific task. Note that the performance of AdamZ is highly sensitive to these parameters, and default settings may not be optimal for all applications.

```python
from adamz import AdamZ
import torch

model = torch.nn.Linear(10, 1)
optimizer = AdamZ(
    model.parameters(),
    lr=learning_rate,
    overshoot_factor=0.5,
    stagnation_factor=1.2,
    stagnation_threshold=0.2,
    patience=100,
    stagnation_period=10
)
# Training loop
for input, target in dataset:
    optimizer.zero_grad()
    loss = loss_fn(model(input), target)
    loss.backward()
    optimizer.step()
```

## Citation
If you find this code helpful, please cite our paper in the following format.

```bibtex
@misc{zaznov2024adamzenhancedoptimisationmethod,
      title={AdamZ: An Enhanced Optimisation Method for Neural Network Training}, 
      author={Ilia Zaznov and Atta Badii and Alfonso Dufour and Julian Kunkel},
      year={2024},
      eprint={2411.15375},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2411.15375}, 
}
```

## Contributions

Contributions are welcome! Please feel free to submit a pull request or open an issue for suggestions and improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions, please contact i.zaznov@pgr.reading.ac.uk or open an issue on GitHub.

