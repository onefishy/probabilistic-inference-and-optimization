# Probabilistic Inference & Optimization

**Author:** [Weiwei Pan](https://onefishy.github.io)

:::{admonition} Work in progress
:class: warning
This book is adapted from the lecture notes for [AM207: Stochastic Methods for Data Analysis, Inference and Optimization](https://onefishy.github.io/am207/) (Harvard University, Fall 2021). The chapters are being revised from lecture-note form into textbook prose one at a time. Until a chapter has been revised, its code targets the course's original Python 3.7 environment and its outputs are the ones saved in the original notebooks.
:::

## About This Book

This book develops the skills needed for computational research using stochastic approaches, with an emphasis on implementation and examples. Stochastic methods make it feasible to tackle very diverse problems when the solution space is too large to explore systematically, or when microscopic rules are known but not the macroscopic behavior of a complex system. We cover Bayesian methods of data analysis alongside stochastic optimization. Topics include stochastic gradient descent and simulated annealing, Bayesian modeling, Markov chain Monte Carlo and variational inference.

The book also studies the broader social impact of statistical models and algorithms when they are deployed in real-life applications. Every part ends with an *Applications and Broader Impact* chapter that connects the technical material to downstream tasks, with a focus on assessing potential negative real-life impacts.

## Goals

After working through this book, you will be able to:

1. Build basic Bayesian and non-Bayesian statistical models for continuous, ordinal, categorical and sequential data.
2. Learn point estimates of model parameters using stochastic optimization methods.
3. Perform inference on models using sampling methods as well as variational inference approaches.
4. Evaluate the effectiveness of your inference methods.
5. Evaluate the usefulness and appropriateness of your models.
6. Implement inference methods from scratch in Python.
7. Build statistical models and perform inference using Python libraries.
8. Think broadly and critically about the entire modeling pipeline, from data collection to assessing broader downstream impact.

## Using This Book

The book is organized into six parts:

1. **Foundations of Inference.** Maximum likelihood, Bayesian modeling, and how Bayesian and frequentist inference compare.
2. **Sampling and Monte Carlo.** Posterior simulation, Monte Carlo integration, and Markov chain Monte Carlo.
3. **Latent Variables and Variational Inference.** Latent variable models, EM, variational inference and hierarchical models.
4. **Optimization.** Gradient descent, stochastic gradient descent and simulated annealing.
5. **Advanced MCMC.** Hamiltonian Monte Carlo, parallel tempering and stochastic HMC.
6. **Bayesian Deep Learning.** Neural network models, black-box variational inference, automatic differentiation and variational autoencoders.

Each chapter ends with a summary and a list of further readings; many also include exercises, most with collapsed worked solutions. Readings are tagged *Introductory*, *In-Depth* or *Research* where a level was given.

The **Labs** at the end of the book are hands-on companions to the chapters, covering sampling, MCMC, variational inference, `pymc3`, logistic regression, neural network regression and hidden Markov models. Worked solutions, with their code and plots, are collapsed so that you can attempt each exercise first.

**Prerequisites.** Familiarity with probability, linear algebra, multivariable calculus and Python (NumPy). Linear regression and basic Bayesian modeling at the level of an introductory data science course are helpful.

**Companion text.** We recommend *Bayesian Data Analysis* (3rd edition) by Gelman, Carlin, Stern, Dunson, Vehtari and Rubin as a reference for statistical modeling, though this book does not follow its structure.

**Running the code.** Every chapter can be downloaded as a Jupyter notebook using the download button at the top of the page. Data files live in the [`data/`](https://github.com/onefishy/probabilistic-inference-and-optimization/tree/main/data) folder of the book's repository.

## License

This book is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
