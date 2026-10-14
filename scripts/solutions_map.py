"""Which cells of the author's solution notebooks answer which book question.

Used by `add_solutions.py`. Only the author's own answers are used: a question with no
matching answer in the sources gets no solution and is listed in GAPS instead.

Source keys name the folder a notebook sits in (HW3 is HW_3/, which holds the Fall 2019
"Homework #2" solutions; the questions match the book's wording).

A solution is `S(page, after, title, *segments)`:
  page      book notebook stem (chapters/ or labs/)
  after     text that occurs in exactly one cell of the page: the solution goes after it
            (solutions sharing an anchor keep their order here)
  title     dropdown title, numbered as the reader sees the question
  segments  md(src, cell, start, end, fixes)  prose from a markdown cell, between the
                                              start and end markers (both excluded,
                                              unless keep_start=True; unindent=True strips
                                              leading spaces, for text taken out of a list)
            code(src, cell, out, fixes)       a code cell and (out=True) its saved outputs;
                                              cell=None shows a whole .py source file
            ran(step)                         code and outputs of a re-run step (RERUN)
            text(markdown)                    connecting text written for the book
            note(markdown)                    "*Not covered here: ...*" for partial answers
`fixes` are exact (old, new[, count]) edits (`old` may be a compiled regex); a fix that no
longer matches stops the run.
`[[ps:KEY]]`, `[[ch:LECTURE]]` and `[[lab:N]]` placeholders become cross-references.
"""

import re

SOURCES = {
    "HW0": ("hw", "HW_0/AM207_HW0_Solutions.ipynb"),
    "HW1": ("hw", "HW_1/HW1_Solutions/AM207_HW1_Solutions.ipynb"),
    "HW2": ("hw", "HW_2/AM207_HW2_Solutions.ipynb"),
    "HW3": ("hw", "HW_3/AM207_HW3_Solutions.ipynb"),
    "HW4": ("hw", "HW_4/AM207_HW4_Solutions.ipynb"),
    "HW5": ("hw", "HW_5/AM207_HW5_Solutions.ipynb"),
    "HW6": ("hw", "HW_6/HW6_solutions/AM207_HW6_Solutions.ipynb"),
    "HW8": ("hw", "HW_8/HW8_solutions/AM207_HW8.ipynb"),
    "HW9": ("hw", "HW_9/HW_9_solutions/AM207_HW9_Solutions.ipynb"),
    # Labs: the notebooks the book's labs were converted from (cell numbers match the book's).
    "LAB1": ("labs", "Lab_1/lab_1_solutions.ipynb"),
    "LAB2": ("labs", "Lab_2/lab_2.ipynb"),
    "LAB3": ("labs", "Lab_3/lab_3.ipynb"),
    "LAB4": ("labs", "Lab_4/lab_4.ipynb"),
    "LAB5": ("labs", "Lab_5/Lab_5/lab_5_slides.ipynb"),
    "LAB5_SOL": ("labs", "Lab_5/Lab_5/lab_5.ipynb"),
    "LAB6": ("labs", "Lab_6/Lab_6/lab_6.ipynb"),
    "LAB7": ("labs", "Lab_7/lab_7.ipynb"),
    "LAB8": ("labs", "Lab_8/lab_8.ipynb"),
    # Helper modules the BNN solutions import.
    "HMC_PY": ("hw", "HW_8/HW8_solutions/alpha_hmc.py"),
    "BBVI_PY": ("hw", "HW_9/HW_9_solutions/bbvi.py"),
}


def S(page, after, title, *segments, key=None):
    return {"page": page, "after": after, "title": title, "segments": segments, "key": key}


def md(src, cell, start=None, end=None, fixes=(), keep_start=False, unindent=False):
    return ("md", src, cell, start, end, tuple(fixes), keep_start, unindent)


def code(src, cell, out=True, fixes=()):
    return ("code", src, cell, out, tuple(fixes))


def ran(step, code=True, out=True):
    return ("ran", step, code, out)


def text(markdown):
    return ("text", markdown)


def note(markdown):
    return ("note", markdown)


# Re-run steps: book(cell id) runs a book cell (starter code) without showing it;
# run(key, src, cell, fixes) and lit(key, source) run code that solutions show via ran(key)
# (cell=None runs a whole .py source file).
def book(cell_id):
    return ("book", cell_id)


def run(key, src, cell, fixes=()):
    return ("src", key, src, cell, tuple(fixes))


def lit(key, source):
    return ("lit", key, source)


INTRO_OLD = "These problems were originally assigned as homework. Data files are in the book's `data/` folder."
INTRO_NEW = INTRO_OLD + (" Worked solutions, where available, are collapsed beneath the questions they answer;"
                         " try each problem before expanding them.")

# Filled in page by page below.
SOLUTIONS = []
# Exact edits to question text: page -> [(old, new)]; an edit is skipped once `new` is present.
PROMPT_EDITS = {}
# Old lab answer cells (by cell id) that the merged lab solutions replace.
LAB_REMOVE = {}
# page -> re-run steps, executed in order in one kernel (after RUN_SETUP in add_solutions.py).
RERUN = {}
# Questions with no answer in the sources (listed by --report).
GAPS = {}

# ---------------------------------------------------------------------------
# 08-metropolis-hastings-gibbs (ps-hw4b): MH-in-Gibbs on the kidney cancer data
# ---------------------------------------------------------------------------

_CH08 = "08-metropolis-hastings-gibbs"
_CH08_P1 = "Exercise: Part I: The Conditional Distributions"
_CH08_P2 = "Exercise: Part II: Metropolis-Hastings-in-Gibbs"

PROMPT_EDITS[_CH08] = [
    (INTRO_OLD, INTRO_NEW),
    # The list restarts after an unindented paragraph, so the source numbers 1, 3, 4 show as is.
    ("3.  Implement and run a Metropolis", "2.  Implement and run a Metropolis"),
    ("4. Check for and discuss the convergence", "3. Check for and discuss the convergence"),
]
GAPS[_CH08] = ["Part III (Broader Impact)"]

SOLUTIONS += [
    S(_CH08, _CH08_P1, "Solution: Part I, Question 1",
      md("HW4", 8, "### Problem 1.\n", "### Problem 2.", fixes=[
          ("As we discussed in class, the MLE to represent cancer rates exagerates rate",
           "As discussed in [[ch:3]], using the MLE to represent cancer rates exaggerates the rates"),
          ("(see HW #1 solutions)", "(see the [[ps:1]])"),
          ("In Lecture #9, we discuss another advantage of choosing a hierarchical model.",
           "[[ch:11]] discusses another advantage of choosing a hierarchical model."),
      ])),
    S(_CH08, _CH08_P1, "Solution: Part I, Question 2",
      md("HW4", 8, "### Problem 2.\n", fixes=[
          ("Gamma(a, b)Gamma(c, d)", r"Gamma(\alpha; a, b)Gamma(\beta; c, d)", 2),
          ("\n\nand $p(\\alpha, \\beta | \\theta, y)$ (again treating", "\n\nSimilarly, $p(\\alpha, \\beta | \\theta, y)$ (again treating"),
      ])),
    S(_CH08, _CH08_P2, "Solution: Part II, Question 1",
      md("HW4", 9, "### Problem 1\n", "### Problem 2")),
    S(_CH08, _CH08_P2, "Solution: Part II, Question 2",
      md("HW4", 9, "### Problem 2\n"),
      code("HW4", 10),
      code("HW4", 11),
      code("HW4", 12, fixes=[("burn-in of 20% and thinning of 2\n", "burn-in of 20% and thinning of 20\n")])),
    S(_CH08, _CH08_P2, "Solution: Part II, Question 3",
      md("HW4", 13, "### Problem 3\n"),
      code("HW4", 14),
      code("HW4", 15),
      md("HW4", 16, fixes=[
          (" Recall the bimodal example from Lecture #6)", ")"),
          (" (some of you have made this modification with successful results)", ""),
      ])),
]

# ---------------------------------------------------------------------------
# 09-latent-variable-models (ps-hw4a): EM for data augmentation
# ---------------------------------------------------------------------------

_CH09 = "09-latent-variable-models"
_CH09_P1 = "Exercise: Part I: MLE Through Latent Variable Augmentation and EM"

PROMPT_EDITS[_CH09] = [(INTRO_OLD, INTRO_NEW)]

SOLUTIONS += [
    S(_CH09, _CH09_P1, "Solution: Part I, Question 1",
      md("HW4", 5, "### Problem 1\n", "### Problem 2")),
    S(_CH09, _CH09_P1, "Solution: Part I, Question 2",
      md("HW4", 5, "### Problem 2\n", "### Problem 3", fixes=[
          # The ELBO is the expectation of the log ratio.
          (r"\left[ \frac{p(Z, Y|\theta)}{q(Z)}\right]", r"\left[ \log \frac{p(Z, Y|\theta)}{q(Z)}\right]"),
          ("EM is an algorithem", "EM is an algorithm"),
          ("tractability of computation for the extent to which log likleihood is maximized",
           "tractability of computation for the extent to which log likelihood is maximized"),
          ("rewrite the above expecation", "rewrite the above expectation"),
          # log of a product is a sum of logs (the log was wrapped around the whole sum).
          (r"\left[  \log\left(\binom{y_1}{Z} +  (y_1 - Z)\log\left(\frac{1}{2}\right)  + Z\log \left(\frac{\theta}{4}\right) +  (y_2 + y_3) \log \left(\frac{1-\theta}{4}\right) + y_4 \log \left(\frac{\theta}{4}\right) \right)\right]",
           r"\left[  \log\binom{y_1}{Z} +  (y_1 - Z)\log\left(\frac{1}{2}\right)  + Z\log \left(\frac{\theta}{4}\right) +  (y_2 + y_3) \log \left(\frac{1-\theta}{4}\right) + y_4 \log \left(\frac{\theta}{4}\right) \right]"),
          (r"\mathbb{E}_{Z | Y, \theta_{old}\theta}", r"\mathbb{E}_{Z | Y, \theta_{old}}"),
          # Every factor of 1/4 contributes a log 4, not three of them.
          (r"+ y_4 \log \left({\theta}\right) - 3\log 4 \\",
           r"+ y_4 \log \left({\theta}\right) - \left(\mathbb{E}_{Z | Y, \theta_{old}}\left[Z\right] + y_2 + y_3 + y_4\right)\log 4 \\"),
          (r"+ y_4\log (\theta) - 3\log 4\\",
           r"+ y_4\log (\theta) - \left(\frac{y_1\theta_{old}}{2 + \theta_{old}} + y_2 + y_3 + y_4\right)\log 4\\"),
          (r"C = \mathbb{E}_{Z | Y, \theta}\left[\log\binom{y_1}{Z}\right] + \log\frac{1}{2} \left(y_1 - \frac{y_1\theta_{old}}{2 + \theta_{old}}\right)  - 3\log 4$",
           r"C = \mathbb{E}_{Z | Y, \theta_{old}}\left[\log\binom{y_1}{Z}\right] + \log\frac{1}{2} \left(y_1 - \frac{y_1\theta_{old}}{2 + \theta_{old}}\right)  - \left(\frac{y_1\theta_{old}}{2 + \theta_{old}} + y_2 + y_3 + y_4\right)\log 4$"),
          (r"{2 + \theta^{t-1}}", r"{2 + \theta_{old}}"),
          (r"p(Z|Y, \theta_{old}) = Bin\left(Z; y_1, \frac{\theta}{2 + \theta}\right)$",
           r"p(Z|Y, \theta_{old}) = Bin\left(Z; y_1, \frac{\theta_{old}}{2 + \theta_{old}}\right)$"),
      ])),
    S(_CH09, _CH09_P1, "Solution: Part I, Question 3",
      md("HW4", 5, "### Problem 3\n"),
      code("HW4", 6),
      md("HW4", 7, end="## Problem 4")),
]

# ---------------------------------------------------------------------------
# 10-variational-inference (ps-hw5a): EM and variational inference (essay questions)
# ---------------------------------------------------------------------------

_CH10 = "10-variational-inference"
_CH10_Q = "#### Bayesian Latent Variable Model"

PROMPT_EDITS[_CH10] = [(INTRO_OLD, INTRO_NEW)]
GAPS[_CH10] = ["Question 5 (Generalizability of EM)"]

SOLUTIONS += [
    S(_CH10, _CH10_Q, "Solution: Question 1",
      md("HW5", 5, "### Problem 1: Comparing ELBOs\n", "### Problem 2", fixes=[
          ("The simliarity between", "The similarity between"),
          ("\n\n***Extra Credit is available to any student who fleshes out this argument fully!***", ""),
      ]),
      note("a comparison of the EM update steps with the CAVI update steps.")),
    S(_CH10, _CH10_Q, "Solution: Question 2",
      md("HW5", 5, "### Problem 2: Comparing ELBOs and KL-divergences\n", "### Problem 3", fixes=[
          # The variational target is the posterior over everything unobserved, z included,
          # so the intractable term is the log evidence log p(y | a, b).
          (r"p(\theta, \phi|y, z, a, b)", r"p(z, \theta, \phi|y, a, b)", 6),
          (r"p(y, z | a, b)", r"p(y | a, b)", 6),
          (r"\int_{\Theta, \Phi}p(y, z, \theta, \phi| a, b) d(\theta, \phi)",
           r"\int p(y, z, \theta, \phi| a, b)\, dz\, d\theta\, d\phi", 2),
          ("when we substitue this", "when we substitute this"),
          ("the problemmatic term", "the problematic term"),
          ("prefer to evalutation this", "prefer to evaluate this"),
          ("a hard problem to sovle", "a hard problem to solve"),
          ("is not intractible to compute", "is not intractable to compute"),
          ("is known and tractible", "is known and tractable"),
      ])),
    S(_CH10, _CH10_Q, "Solution: Question 3",
      md("HW5", 5, "### Problem 3. The Mean Field Assumption and Coordinate Ascent\n", "### Problem 4")),
    S(_CH10, _CH10_Q, "Solution: Question 4",
      md("HW5", 5, "### Problem 4. Generalizability of CAVI\n", fixes=[
          ("Bayesian Gaussain mixture", "Bayesian Gaussian mixture"),
      ])),
]

# ---------------------------------------------------------------------------
# 11-hierarchical-models (ps-hw5b): empirical Bayes and hierarchical Bayes, kidney cancer
# ---------------------------------------------------------------------------

_CH11 = "11-hierarchical-models"
_CH11_P1 = "Exercise: Part I: Empirical Bayes"
_CH11_P2 = "Exercise: Part II: Hierarchical Bayes"

PROMPT_EDITS[_CH11] = [(INTRO_OLD, INTRO_NEW)]
GAPS[_CH11] = ["Part III (Broader Impact), Questions 1-2"]

# Part I re-runs (numpy/pandas only) with the plotting helper fixed: the raw rates were
# drawn at alpha=0.0001 (invisible) and the top/bottom 300 colours were swapped.
# Part II needs pymc3, so its saved outputs are shown.
RERUN[_CH11] = [
    lit("imports", "import pandas as pd\nimport matplotlib.pyplot as plt"),
    run("helper", "HW5", 4, fixes=[
        ("# estimates_df is a numpy array", "# estimates is a numpy array"),
        ('y="pct_mortality", alpha=0.0001, color="grey")', 'y="pct_mortality", alpha=0.1, color="grey")'),
        ('alpha=0.0001, color="blue", ax=ax', 'alpha=0.5, color="red", ax=ax'),
        ('alpha=0.0001, color="red", ax=ax', 'alpha=0.5, color="blue", ax=ax'),
    ]),
    run("raw", "HW5", 7),
    run("moments", "HW5", 10),
    run("alpha-beta", "HW5", 12),
    run("posterior", "HW5", 14),
    run("posterior-plot", "HW5", 16),
]

_HW5_PART2_PLOT = text(
    "*This plot is from the original `pymc3` run (not re-run). It was drawn with the original plotting helper,"
    " which colours the top 300 raw rates blue and the bottom 300 red (the reverse of the question); the posterior"
    " means are in green.*")

SOLUTIONS += [
    S(_CH11, _CH11_P1, "Solution: Part I, Question 1",
      ran("helper", out=False),
      ran("raw"),
      md("HW5", 8)),
    S(_CH11, _CH11_P1, "Solution: Part I, Question 2",
      md("HW5", 9, "### Problem #2: Empirical Bayes\n", fixes=[
          (" Since the Poisson distribution \n", "\n"),
          # Poisson pmf: (5 n_j theta_j)^{y_j} e^{-5 n_j theta_j} / y_j!
          (r"\frac{1}{y_j!} e^{5 \cdot n_j \cdot \theta_j}",
           r"\frac{\left(5 \cdot n_j \cdot \theta_j\right)^{y_j}}{y_j!} e^{-5 \cdot n_j \cdot \theta_j}"),
          (r"\Gamma\left((\alpha + y_j - 2) - 1\right)", r"\Gamma\left((\alpha + y_j - 2) + 1\right)"),
          (r"NegBin\left(\alpha, \frac{5 n_j}{1  + \beta}\right)", r"NegBin\left(\alpha, \frac{5 n_j}{5 n_j  + \beta}\right)"),
          (r"&= \mathbb{E}[y_j] \left( \frac{5}{\beta} + \frac{1}{n_j}\right).",
           r"&= \mathbb{E}\left[\frac{y_j}{n_j}\right] \left( \frac{5}{\beta} + \frac{1}{n_j}\right)."),
          ("If we are permited to be", "If we are permitted to be"),
      ]),
      ran("moments"),
      md("HW5", 11),
      ran("alpha-beta"),
      md("HW5", 13, fixes=[("the postior mean", "the posterior mean")]),
      ran("posterior")),
    S(_CH11, _CH11_P1, "Solution: Part I, Question 3",
      md("HW5", 15, "### Problem #4: Posterior Means Visualization\n"),
      ran("posterior-plot"),
      md("HW5", 17)),
    S(_CH11, _CH11_P2, "Solution: Part II, Question 1",
      md("HW5", 18, "### Problem 1: Posterior Marginal Means of the Hierarchical Model\n"),
      code("HW5", 19, out=False, fixes=[
          ("#hyperparameters of hierarchical model\n",
           "import pymc3 as pm\nfrom pymc3 import Model\n\n#hyperparameters of hierarchical model\n"),
          ("\n    \n#draw graphical model for the thing we just defined  \nmodel_to_graphviz(hiearchical_model)", ""),
      ]),
      code("HW5", 20, fixes=[
          ("#the default sampler for pymc3 is a type of MCMC sampler called No-U-turn HMC, \n"
           "#which we have not covered in class\n",
           "#the default sampler for pymc3 is the No-U-Turn Sampler (NUTS), a type of HMC\n"),
      ]),
      code("HW5", 21),
      md("HW5", 22, end="### Problem 2", fixes=[
          ("Certainty, the traceplots", "Certainly, the traceplots"),
          ("than for the naive sampler we implemented last week!",
           "than for the Metropolis-Hastings-in-Gibbs sampler from the [[ps:4b]]!"),
      ]),
      code("HW5", 23),
      _HW5_PART2_PLOT),
    S(_CH11, _CH11_P2, "Solution: Part II, Question 2",
      md("HW5", 22, "### Problem 2: Hierarchical Bayes vs Empirical Bayes\n", fixes=[
          ("Ploting the posterior mean", "Plotting the posterior mean"),
          ("More so that in the case", "More so than in the case"),
          ("(all the rates are around 0.00005%)", "(all the rates are around 0.005%)"),
      ]),
      code("HW5", 23),
      _HW5_PART2_PLOT),
]

# ---------------------------------------------------------------------------
# 13-sgd-simulated-annealing (ps-hw6): gradient descent vs SGD on a construction-cost loss
# ---------------------------------------------------------------------------
# Not re-run: the answers compare wall-clock timings, so the saved outputs are shown.
# The source groups its answers by topic; they are regrouped here by question.

_CH13 = "13-sgd-simulated-annealing"
_CH13_P1 = "Exercise: Part I: Cost minimization with descent algorithms"
_HW6_DATA = [("'HW5_data.csv'", "'../data/HW6_data.csv'")]

PROMPT_EDITS[_CH13] = [(INTRO_OLD, INTRO_NEW)]

# Question 7 (no timings) is re-run so its plot titles state the step sizes and algorithms used
# (the source's said "stepsize 1." for step size 10 and "Gradient Descent" for SGD).
def _title_fix(old_step, new_step):
    """Title of the SGD plots: 'Gradient Descent ... stepsize <old>' -> 'Stochastic Gradient Descent ... stepsize <new>'."""
    return (r"'Total Cost vs Iteration in Gradient Descent,\n init @({}, 0), stepsize " + old_step + r"\n'",
            r"'Total Cost vs Iteration in Stochastic Gradient Descent,\n init @({}, 0), stepsize " + new_step + r"\n'")
RERUN[_CH13] = [
    run("imports", "HW6", 3),
    run("data", "HW6", 5, fixes=_HW6_DATA),
    run("loss", "HW6", 6),
    run("grad", "HW6", 12),
    run("gd", "HW6", 14),
    run("sgd", "HW6", 18),
    run("gd-run", "HW6", 15),
    run("sgd-run", "HW6", 19, fixes=[
        ("ax1.set_title('Total Loss vs Iteration in Gradient Descent')", "ax1.set_title('Total Loss vs Iteration in Stochastic Gradient Descent')"),
        ("ax2.plot(np.arange(len(costs[-100:])) + N - 100, costs[-100:]", "ax2.plot(np.arange(len(costs) - 100, len(costs)), costs[-100:]"),
        ("ax2.set_title('Total Loss vs Iteration in Gradient Descent (Last 100 Iterations)')",
         "ax2.set_title('Total Loss vs Iteration in Stochastic Gradient Descent (Last 100 Iterations)')"),
        ("ax4.plot(range(len(costs[15000:])), grad_norms_sgd[15000:]", "ax4.plot(range(15000, len(costs)), grad_norms_sgd[15000:]"),
    ]),
    run("sgd-shuffled-run", "HW6", 21, fixes=[
        ("ax1.set_title('Total Loss vs Iteration in Gradient Descent')", "ax1.set_title('Total Loss vs Iteration in Stochastic Gradient Descent')"),
        ("ax2.plot(range(len(costs[-100:])), costs[-100:]", "ax2.plot(np.arange(len(costs) - 100, len(costs)), costs[-100:]"),
        ("ax2.set_title('Total Loss vs Iteration in Gradient Descent (Last 100 Iterations)')",
         "ax2.set_title('Total Loss vs Iteration in Stochastic Gradient Descent (Last 100 Iterations)')"),
        # the run can stop well before iteration 2500; show the last 500 iterations
        ("ax4.plot(range(len(costs[2500:])), grad_norms_sgd[2500:]", "ax4.plot(np.arange(len(costs) - 500, len(costs)), grad_norms_sgd[-500:]"),
    ]),
    run("gd-step-sizes", "HW6", 24, fixes=[
        ("fig, ax = plt.subplots(1, 4, figsize=(50, 10))", "fig, ax = plt.subplots(1, 4, figsize=(24, 5))"),
        ("    ax[i].set_title('Total Loss vs Iteration in Gradient Descent')", "    ax[i].set_title('Gradient Descent, step size {}'.format(step_size))"),
    ]),
    *[run(f"sgd-step-size-{k}", "HW6", k) for k in range(26, 33)],
    run("init-gd", "HW6", 34, fixes=[
        (r"ax[0, i].set_title('Total Cost vs Iteration in Gradient Descent,\n init @({}, 0), stepsize 1.\n'",
         r"ax[0, i].set_title('Total Cost vs Iteration in Gradient Descent,\n init @({}, 0), stepsize 10\n'"),
        (r"initial 500 iterations, \n init @({}, 0), stepsize 1.\n'", r"initial 500 iterations, \n init @({}, 0), stepsize 10\n'"),
    ]),
    run("init-grad", "HW6", 36),
    run("init-sgd-10", "HW6", 38, fixes=[_title_fix("1.", "10")]),
    run("init-sgd-50", "HW6", 40, fixes=[_title_fix("50", "50")]),
    run("init-sgd-500", "HW6", 42, fixes=[_title_fix("500", "500")]),
]
GAPS[_CH13] = ["Part II (Broader Impact)"]

SOLUTIONS += [
    S(_CH13, _CH13_P1, "Solution: Part I, Question 1",
      code("HW6", 3),
      md("HW6", 4, "### Visualizing Our Loss Function\n", fixes=[
          ("In `python`, we would write the above as\n```\n", "In `python`, we would write the above as\n```python\n"),
          ("the total loss is minized for", "the total loss is minimized for"),
      ]),
      code("HW6", 5, fixes=_HW6_DATA),
      code("HW6", 6),
      code("HW6", 7),
      md("HW6", 8),
      code("HW6", 9),
      md("HW6", 10)),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 2",
      md("HW6", 11, "### Implementation: Gradient Descent\n", fixes=[
          # d/d lambda_2 of lambda_2^2 is 2 lambda_2 (the code has it right).
          (r"2 * 0.000045\lambda_2^2 \sum", r"2 * 0.000045\lambda_2 \sum"),
      ]),
      code("HW6", 12),
      md("HW6", 13, "A note on the correct stopping condition to use:", keep_start=True, fixes=[
          (re.compile(r"(?m)^> ?"), "", 2),
          (r"\| [ lambda_1,  lambda_2] - [ 2.05384, 0 ] \|_2 < 1e^{-3}", r"\| [ \lambda_1,  \lambda_2] - [ 2.05384, 0 ] \|_2 < 10^{-3}"),
          ("(which involves suming over", "(which involves summing over"),
      ]),
      code("HW6", 14),
      ran("gd-run"),
      md("HW6", 16)),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 3",
      md("HW6", 17, "### Implementation: Stochastic Gradient Descent\n"),
      code("HW6", 18),
      ran("sgd-run"),
      md("HW6", 20, fixes=[
          ("that descreases the loss", "that decreases the loss"),
          ("decrease form one iteration", "decrease from one iteration"),
      ]),
      ran("sgd-shuffled-run"),
      md("HW6", 22, fixes=[
          # Match the re-run's iteration count.
          ("after 1,990 steps (versus", "after 5,637 steps (versus"),
          ("around the optimal total loss of -9.93410279384.", "around the optimal total loss of -9.9341."),
          ("When we examing the total loss", "When we examine the total loss"),
          ("is ocillating around", "is oscillating around"),
      ])),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 4",
      md("HW6", 13, "A note on the correct loss function to use:\n", "A note on the correct stopping condition to use:", fixes=[
          (re.compile(r"(?m)^> ?"), "", 4),
          ("the loss funtion averaged", "the loss function averaged"),
      ])),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 5",
      md("HW6", 23, "#### Speed:\n", "<a id='stepsize'></a>", fixes=[
          # Match the timings printed by the runs in Questions 2 and 3.
          ("We see that it takes 0.000573873519897 seconds to compute one gradient for gradient descent, "
           "while it takes around 0.000241994857788 seconds to compute one gradient for stochastic gradient descent.",
           "In the runs above, it takes about 0.00034 seconds to compute one gradient for gradient descent, "
           "while it takes around 0.00004 seconds to compute one gradient for stochastic gradient descent."),
          (" For example, you can try to perform gradient descent in your Long Form Homework #1 and see how that will change your training time.", ""),
      ])),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 6",
      md("HW6", 23, "#### Sensitivity to Stepsize:\n"),
      ran("gd-step-sizes"),
      md("HW6", 25),
      ran("sgd-step-size-26"),
      ran("sgd-step-size-27"),
      ran("sgd-step-size-28"),
      ran("sgd-step-size-29"),
      ran("sgd-step-size-30"),
      ran("sgd-step-size-31"),
      ran("sgd-step-size-32"),
      # The source's discussion of these SGD runs describes other step sizes (0.01-1) and
      # iteration counts that the outputs above do not show, so only its conclusion is kept.
      md("HW6", 33, "The same experiments with gradient descent shows", "<a id='init'></a>", keep_start=True, fixes=[
          ("The same experiments with gradient descent shows", "The same experiments with gradient descent show"),
      ]),
      note("a step-by-step discussion of the SGD runs for each step size.")),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 7",
      md("HW6", 33, "#### Sensitivity to Initialization\n"),
      ran("init-gd"),
      md("HW6", 35),
      ran("init-grad"),
      md("HW6", 37, fixes=[
          ("In lecture, we discussed how this descent", "Earlier in this chapter we saw how this descent"),
      ]),
      ran("init-sgd-10"),
      md("HW6", 39, fixes=[
          ("We see that with step size 1., stochastic gradient descent", "We see that with step size 10, stochastic gradient descent"),
      ]),
      ran("init-sgd-50"),
      md("HW6", 41),
      ran("init-sgd-500"),
      md("HW6", 43),
      note("gradient descent with a learning rate of 50.")),
]

# ---------------------------------------------------------------------------
# 01-overview (ps-hw0): MLE and Bayesian linear regression (Fall 2020 solutions)
# ---------------------------------------------------------------------------

_CH01 = "01-overview"

PROMPT_EDITS[_CH01] = [(INTRO_OLD, INTRO_NEW)]
GAPS[_CH01] = ["Part II, Question 3 (the source answers a different question: a histogram of p(y | x=2))",
               "Part III (Broader Impact), Questions 1-2"]

# Part II re-runs (numpy/sklearn): the interval table swapped slope and intercept.
RERUN[_CH01] = [
    book("01-042"),
    run("data", "HW0", 7),
    run("fit", "HW0", 11),
    run("posterior", "HW0", 23, fixes=[("#sampling 100 points from the posterior", "#sampling 200 points from the posterior")]),
    run("joint", "HW0", 24),
    run("marginals", "HW0", 25, fixes=[
        ("#visualize the posterior marginal of w_0\nax[0]", "#visualize the posterior marginal of w_1\nax[0]"),
        ("#visualize the posterior marginal of w_1\nax[1]", "#visualize the posterior marginal of w_0\nax[1]"),
    ]),
    # Column 0 of the samples is the slope w_1 and column 1 the intercept w_0 (x_matrix = [x, 1]).
    run("intervals", "HW0", 30, fixes=[
        ("posterior_samples[:, 1]", "posterior_samples[:, @]", 3),
        ("posterior_samples[:, 0]", "posterior_samples[:, 1]", 3),
        ("posterior_samples[:, @]", "posterior_samples[:, 0]", 3),
        ("columns=['posterior mean', ", "columns=['posterior median', "),
    ]),
]

SOLUTIONS += [
    S(_CH01, "1. **(Model Building)**", "Solution: Part I, Question 1",
      md("HW0", 3, "**Solution:** ", fixes=[
          (r"\prod_{n=1}^N \frac{1}{\sqrt{2\pi 0.5}} \exp\left\{-\frac{(y - (w_1x + w_0))^2}{2 * 0.5} \right\} = \left(\frac{1}{\sqrt{2\pi 0.5}}\right)^N \exp\left\{-\frac{\sum_{n=1}^N (y - (w_1x + w_0))^2}{2 * 0.5} \right\}",
           r"\prod_{n=1}^N \frac{1}{\sqrt{2\pi 0.5}} \exp\left\{-\frac{(y_n - (w_1x_n + w_0))^2}{2 * 0.5} \right\} = \left(\frac{1}{\sqrt{2\pi 0.5}}\right)^N \exp\left\{-\frac{\sum_{n=1}^N (y_n - (w_1x_n + w_0))^2}{2 * 0.5} \right\}"),
      ])),
    S(_CH01, "2. **(Defining a Learning Objective)**", "Solution: Part I, Question 2",
      md("HW0", 4, "**Solution:** ", fixes=[("is equivalant to minimizing", "is equivalent to minimizing")])),
    S(_CH01, "3. **(Model Fitting)**", "Solution: Part I, Question 3",
      md("HW0", 5, "**Solution:** ", fixes=[
          ("From #2, we see", "From Question 2, we see"),
          (r"\frac{\partial}{w_1}", r"\frac{\partial}{\partial w_1}", 2),
          (r"\frac{\partial}{w_0}", r"\frac{\partial}{\partial w_0}", 2),
          # Setting the derivative to zero gives sum x y - (1/N) sum x sum y in the numerator.
          (r"\sum_{n=1}^Nx^2_n + \frac{1}{N} \sum_{n=1}^N x_n  \sum_{n=1}^N y_n + w_1",
           r"\sum_{n=1}^Nx^2_n - \frac{1}{N} \sum_{n=1}^N x_n  \sum_{n=1}^N y_n + w_1"),
          (r"\sum_{n=1}^N x_n y_n + \frac{1}{N} \sum_{n=1}^N x_n  \sum_{n=1}^N y_n",
           r"\sum_{n=1}^N x_n y_n - \frac{1}{N} \sum_{n=1}^N x_n  \sum_{n=1}^N y_n", 2),
          ("mean square error of our linear model is concave", "mean square error of our linear model is convex"),
          ("verify that it is negative definite (the multivariable version of 'the second derivative is negative')",
           "verify that it is positive definite (the multivariable version of 'the second derivative is positive')"),
          (r"\mathbf{x}_n = [x_1\;\; 1]", r"\mathbf{x}_n = [x_n\;\; 1]"),
      ])),
    S(_CH01, "4. **(Model Evaluation)**", "Solution: Part I, Question 4",
      md("HW0", 6, "**Solution:**\n"),
      code("HW0", 7),
      md("HW0", 8),
      code("HW0", 9),
      md("HW0", 10),
      code("HW0", 11, out=False),
      md("HW0", 12),
      code("HW0", 13),
      md("HW0", 14, fixes=[
          # Least-squares residuals with an intercept average exactly zero, and the histogram peaks at 0.
          ("From the histogram of the residuals (on the left), we can see that (1) the residuals are not normally distributed"
           " as we assumed in our model (2) they are not centered at zero as we assumed.",
           "From the histogram of the residuals (on the right), we can see that the residuals are not normally distributed"
           " as we assumed in our model."),
      ]),
      note("the clinical interpretation of the parameters $w_0, w_1$.")),
    S(_CH01, "1. **(Inference)**", "Solution: Part II, Question 1",
      md("HW0", 21, "**Solution:** ", fixes=[
          ("we introduced in Part I Problem 3", "we introduced in Part I, Question 3"),
          (r"(\mathbf{X}w - \mathbf{y}) + -\frac{1}{2} (w - m)^\top S^{-1}(w - m)", r"(\mathbf{X}w - \mathbf{y}) -\frac{1}{2} (w - m)^\top S^{-1}(w - m)"),
          (r"(w_1x_n + w_0)^2)", r"(w_1x_n + w_0))^2", 2),
          # The likelihood covariance is N x N.
          (r"I_{2\times 2}", r"I_{N}", 4),
          (r"I_{2\times2}", r"I_{N}"),
          ("is the 2x2 identity matrix", r"is the $N\times N$ identity matrix"),
          # Keep the -1/2 of the Gaussian exponent, and complete the square with b A^{-1} b^T.
          (r"\mathrm{exp}\left\{ \mathbf{y}^\top\Sigma^{-1}\mathbf{y} + m^\top S^{-1}m \right\}",
           r"\mathrm{exp}\left\{ -\frac{1}{2}\left(\mathbf{y}^\top\Sigma^{-1}\mathbf{y} + m^\top S^{-1}m\right) \right\}"),
          (r"\mathrm{exp}\left\{ w^\top \left(S^{-1} + \mathbf{X}^\top\Sigma^{-1}\mathbf{X}\right) w - 2\left(\mathbf{y}^\top \Sigma^{-1}\mathbf{X} + m^\top S^{-1} \right) w\right\}",
           r"\mathrm{exp}\left\{ -\frac{1}{2}\left(w^\top \left(S^{-1} + \mathbf{X}^\top\Sigma^{-1}\mathbf{X}\right) w - 2\left(\mathbf{y}^\top \Sigma^{-1}\mathbf{X} + m^\top S^{-1} \right) w\right)\right\}", 2),
          (r"\mathrm{exp}\left\{ w^\top A w - 2b w\right\}",
           r"\mathrm{exp}\left\{ -\frac{1}{2}\left(w^\top A w - 2b w\right)\right\}", 2),
          ("add and subtract the term $bA b^\\top$", "add and subtract the term $bA^{-1} b^\\top$"),
          (r"\mathrm{exp}\left\{ w^\top A w - 2b w + bA b^\top- bA b^\top\right\}",
           r"\mathrm{exp}\left\{ -\frac{1}{2}\left(w^\top A w - 2b w + bA^{-1} b^\top- bA^{-1} b^\top\right)\right\}"),
          (r"\mathrm{exp}\left\{ (w - A^{-1}b^\top)^\top A(w - A^{-1}b^\top) - bA b^\top\right\}",
           r"\mathrm{exp}\left\{ -\frac{1}{2}\left((w - A^{-1}b^\top)^\top A(w - A^{-1}b^\top) - bA^{-1} b^\top\right)\right\}"),
          (r"\mathrm{exp}\left\{ - b^\top A b^\top\right\}\mathrm{exp}\left\{ (w - A^{-1}b^\top)^\top A(w - A^{-1}b^\top)\right\}",
           r"\mathrm{exp}\left\{ \frac{1}{2} bA^{-1} b^\top\right\}\mathrm{exp}\left\{ -\frac{1}{2}(w - A^{-1}b^\top)^\top A(w - A^{-1}b^\top)\right\}"),
          (r"const * \mathrm{exp}\left\{ (w - A^{-1}b^\top)^\top A(w - A^{-1}b^\top)\right\}.",
           r"const * \mathrm{exp}\left\{ -\frac{1}{2}(w - A^{-1}b^\top)^\top A(w - A^{-1}b^\top)\right\}."),
          ("with mean $A^{-1}b$ and", "with mean $A^{-1}b^\\top$ and"),
      ])),
    S(_CH01, "2. **(Model Interpretation)**", "Solution: Part II, Question 2",
      md("HW0", 22, "**Solution:** ", fixes=[
          ("From #1, we see", "From Question 1, we see"),
          ("by sampling 100 points from", "by sampling 200 points from"),
          ("of these 100 samples", "of these 200 samples"),
          # Column 0 of the samples is the slope w_1 (x_matrix = [x, 1]).
          (r"For the posterior marginal distribution $p(w_0 | y_1, \ldots y_n, x_1, \ldots, x_n)$, we simply histogram the first coordinates (representing $w_0$)",
           r"For the posterior marginal distribution $p(w_1 | y_1, \ldots y_n, x_1, \ldots, x_n)$, we simply histogram the first coordinates (representing $w_1$)"),
          (r"The same can be done for $p(w_1 | y_1, \ldots y_n, x_1, \ldots, x_n)$.",
           r"The same can be done for $p(w_0 | y_1, \ldots y_n, x_1, \ldots, x_n)$."),
      ]),
      ran("posterior"),
      ran("joint"),
      ran("marginals"),
      md("HW0", 26, fixes=[
          ("but does they cannot tell you", "but they cannot tell you"),
          ("such correlations is important", "such correlations are important"),
      ]),
      text("We can also summarize each marginal posterior by its median and its 95% interval:"),
      ran("intervals"),
      note("the empirical variances of the marginal posteriors, and what the widths of these intervals "
           "say about our confidence in the estimates.")),
]

# ---------------------------------------------------------------------------
# 03-bayesian-modeling (ps-hw1): multinomial/Dirichlet models of product ratings (Fall 2020)
# ---------------------------------------------------------------------------

_CH03 = "03-bayesian-modeling"

PROMPT_EDITS[_CH03] = [(INTRO_OLD, INTRO_NEW)]
GAPS[_CH03] = ["Part III (Broader Impact), Question 1"]

# Part II re-runs (numpy): the posterior predictive drew 160 Lotus ratings; there are 163.
RERUN[_CH03] = [
    book("03-044"),
    run("posterior-samples", "HW1", 10),
    run("posterior-mean", "HW1", 13),
    run("predictive", "HW1", 16, fixes=[("np.random.multinomial(160, sample", "np.random.multinomial(163, sample")]),
    run("predictive-percent", "HW1", 17),
    run("credible-intervals", "HW1", 20),
]

SOLUTIONS += [
    S(_CH03, "Exercise: Part I: A Maximum Likelihood Model", "Solution: Part I, Question 1",
      md("HW1", 4, "**Solution:** ", fixes=[
          ("{10!6!10!27!109!}", "{10!6!10!28!109!}"),
          ("$[10 6 10 28 109]$", r"$[10\;\; 6\;\; 10\;\; 28\;\; 109]$"),
          ("$[57 33 29 45 246]$", r"$[57\;\; 33\;\; 29\;\; 45\;\; 246]$"),
      ])),
    S(_CH03, "2. **(Model Fitting)**", "Solution: Part I, Question 2",
      md("HW1", 5, "**Solution:**\n", fixes=[
          ("From lecture, we know that the solution", "From [[ch:2]], we know that the solution"),
          ("Since the likelihood is concave and the constraints affine",
           "Since the log-likelihood is concave and the constraint is affine"),
          # The Lotus counts 10 + 6 + 10 + 28 + 109 add up to 163.
          ("{162}", "{163}", 5),
          ("these estimates of $\\theta$ are precise the percentages", "these estimates of $\\theta$ are precisely the percentages"),
      ])),
    S(_CH03, "3. **(Model Interpretation)**", "Solution: Part I, Question 3",
      md("HW1", 6, "**Solution:** ", fixes=[
          ("total number of reveiws", "total number of reviews"),
          ("equally reasonablbe", "equally reasonable"),
      ])),
    S(_CH03, "Exercise: Part II: A Bayesian Model", "Solution: Part II, Question 1",
      md("HW1", 7, "**Solution:** ")),
    S(_CH03, "2. **(Inference)** Analytically derive the posterior distribution (using the likelihoods",
      "Solution: Part II, Question 2",
      md("HW1", 8, "**Solution:** ")),
    # The source's second prior is alpha = 1/5, not the book's [1, 1, 1, 1, 1]; that part is left out.
    S(_CH03, "3. **(The Maximum A Posterior Estimate)**", "Solution: Part II, Question 3",
      md("HW1", 9, "**Solution:**\n", "But to what extend"),
      md("HW1", 9, "Rather than analytically computing", keep_start=True, fixes=[
          (r"unimodal when $\alpha_i> 1$. This estimation", r"unimodal when $\alpha_i> 1$, this estimation"),
      ]),
      ran("posterior-samples"),
      md("HW1", 11),
      note(r"the MAP estimates under the uniform prior $\alpha = [1, 1, 1, 1, 1]$, and the conjecture about"
           " the effect of the prior.")),
    S(_CH03, "4. **(The Posterior Mean Estimate)**", "Solution: Part II, Question 4",
      md("HW1", 12, "**Solution:** "),
      ran("posterior-mean"),
      md("HW1", 14)),
    S(_CH03, "5. **(The Posterior Predictive Estimate)**", "Solution: Part II, Question 5",
      md("HW1", 15, "**Solution:** ", fixes=[("parametrizes a distinct binomial model", "parametrizes a distinct multinomial model")]),
      ran("predictive"),
      ran("predictive-percent"),
      md("HW1", 18)),
    S(_CH03, "6. **(Model Evaluation)**", "Solution: Part II, Question 6",
      md("HW1", 19, "**Solution:** ", fixes=[("just as in Homework #0, we empirically", "Just as in the [[ps:0]], we empirically")]),
      ran("credible-intervals"),
      md("HW1", 21, fixes=[
          ("have comparible width", "have comparable width"),
          ("may be unreasonble to use", "may be unreasonable to use"),
      ])),
    S(_CH03, "2. **(Comparison of Ranking Systems)**", "Solution: Part III, Question 2",
      md("HW1", 22, "**Solution:** \n"),
      note("which point estimate of $\\theta$, if any, to use to rank the two products.")),
]

# ---------------------------------------------------------------------------
# 04-bayesian-vs-frequentist (ps-hw2): polynomial regression under covariate shift (Fall 2020 draft)
# ---------------------------------------------------------------------------

_CH04 = "04-bayesian-vs-frequentist"

PROMPT_EDITS[_CH04] = [
    (INTRO_OLD, INTRO_NEW),
    # Question 2's sub-steps were indented 2 spaces, so they rendered as items 3-5 of the question list
    # (and the next question showed up as a second "3."); 3 spaces nest them under Question 2.
    ("\n\n  1. randomly sample two datasets", "\n\n   1. randomly sample two datasets"),
    ("\n  2. plot the validation score as a function", "\n   2. plot the validation score as a function"),
    ("\n  3. based on the plot, select", "\n   3. based on the plot, select"),
    ("\n\n  Explain why performing model selection", "\n\n   Explain why performing model selection"),
    ("<br><br>\n  Implement model selection by cross-validation", "<br><br>\n   Implement model selection by cross-validation"),
]
GAPS[_CH04] = ["Part I, Question 4 (the source fits Lasso, not Ridge, and has no discussion)",
               "Part II, Questions 1-3", "Part III (Broader Impact), Questions 1-3"]

# Re-run (numpy/sklearn) against the book's generate_data, which returns (x_train, y_train, x_test).
# The source's "bootstrap" ensembles drew fresh datasets from the true generating process;
# they now resample one training set with replacement, as the question asks.
_BOOT = "    # Bootstrap: resample the training data with replacement\n"
RERUN[_CH04] = [
    book("04-030"),
    book("04-031"),
    run("fit", "HW2", 7, fixes=[
        ("x_train, y_train, x_test, y_test = generate_data(number_of_points=20, noise_variance=0.3) \n",
         "x_train, y_train, x_test = generate_data(number_of_points=20, noise_variance=0.3)\n"
         "# Noisy test outcomes from the same cubic function\n"
         "y_test = 3 * x_test**3 + np.random.normal(0, 0.3**0.5, size=x_test.shape)\n"),
    ]),
    run("fit-plot", "HW2", 8, fixes=[
        ("ax[row, col].plot(x_test, ys, label='training data')", "ax[row, col].plot(x_test, ys, label='MLE polynomial model')"),
        ("alpha=0.9, label='MLE polynomial model')", "alpha=0.9, label='training data')"),
    ]),
    run("mse", "HW2", 10),
    run("new-data", "HW2", 12, fixes=[("x_train_new, y_train_new, _, _ = generate_data", "x_train_new, y_train_new, _ = generate_data")]),
    run("cv", "HW2", 15, fixes=[
        ("x_train, y_train, _, _ = generate_data", "x_train, y_train, _ = generate_data"),
        ("x_valid, y_valid, _, _ = generate_data", "x_valid, y_valid, _ = generate_data"),
    ]),
    run("cv-plot", "HW2", 16),
    lit("train-data", "# The training data for the ensembles below\n"
                      "x_train, y_train, x_test = generate_data(number_of_points=20, noise_variance=0.3)"),
    run("train-plot", "HW2", 20, fixes=[("# Visualize the average validation mse for each degree\n", "# Visualize the training data\n")]),
    run("ensemble", "HW2", 22, fixes=[
        ("    # Generate a random training samples from the true distribution over x\n"
         "    x_train, y_train, x_test, _ = generate_data(number_of_points=20, noise_variance=0.3)\n",
         _BOOT + "    idx = np.random.choice(len(x_train), size=len(x_train), replace=True)\n"
                 "    x_boot, y_boot = x_train[idx], y_train[idx]\n"),
        ("poly.fit_transform(x_train.reshape((-1, 1)))", "poly.fit_transform(x_boot.reshape((-1, 1)))"),
        ("linear_regressor.fit(x_train_poly, y_train.reshape(-1, 1))", "linear_regressor.fit(x_train_poly, y_boot.reshape(-1, 1))"),
    ]),
    run("intervals", "HW2", 23),
    run("ensemble-plot", "HW2", 24, fixes=[
        ("    ys = predictions[i].flatten()\n", ""),
        ("label='MLE polynomial model') #scatter plot the training data", "label='training data') #scatter plot the training data"),
    ]),
    run("ensemble-sizes", "HW2", 26, fixes=[
        ("    pred_per_data = []\n",
         "    pred_per_data = []\n    # One training dataset of this size\n"
         "    x_train_sample, y_train_sample, _ = generate_data(number_of_points=size, noise_variance=0.3)\n"),
        ("        # Generate a random training samples from the true distribution over x\n"
         "        x_train_sample, y_train_sample, _, _ = generate_data(number_of_points=size, noise_variance=0.3)\n",
         "    " + _BOOT + "        idx = np.random.choice(len(x_train_sample), size=len(x_train_sample), replace=True)\n"
                         "        x_boot, y_boot = x_train_sample[idx], y_train_sample[idx]\n"),
        ("poly.fit_transform(x_train_sample.reshape((-1, 1)))", "poly.fit_transform(x_boot.reshape((-1, 1)))"),
        ("linear_regressor.fit(x_train_poly, y_train_sample.reshape(-1, 1))", "linear_regressor.fit(x_train_poly, y_boot.reshape(-1, 1))"),
    ]),
    run("ensemble-sizes-plot", "HW2", 27, fixes=[
        ("label='MLE polynomial model') #scatter plot the training data", "label='training data') #scatter plot the training data"),
    ]),
]

SOLUTIONS += [
    S(_CH04, "1. **(Effect of Model Complexity)**", "Solution: Part I, Question 1",
      md("HW2", 6, "**Solutions:** "),
      ran("fit"),
      ran("fit-plot"),
      md("HW2", 9, fixes=[("fit the data welll", "fit the data well"), ("and test errror", "and test error")]),
      ran("mse"),
      md("HW2", 11, fixes=[("the actualy data generating function", "the actual data generating function")]),
      ran("new-data"),
      # The re-run shows degrees 10 and 15 with similar train/test gaps (degree 15's test MSE is
      # below degree 5's), so the source's paragraph singling out degrees 15+ and setting degree 10
      # apart is left out.
      md("HW2", 13, fixes=[
          ("Now, with a new toy dataset sampled from the same distribution as our training dataset, we can finally see"
           " evidence that degrees 15 and higher are indeed overfitting. But although we decided, based on our visual"
           " anlysis, that the degree 10 polynomial model is overfitting, the difference between train and test MSE for"
           " this model is not significantly different from the degree 3 or degree 5 model. \n\nFinally, it is clear",
           "It is clear"),
      ])),
    S(_CH04, "2. **(Model Selection)**", "Solution: Part I, Question 2",
      ran("cv"),
      ran("cv-plot"),
      md("HW2", 17, fixes=[
          (" For example, in Exercise 1 we thought that the degree 10 model looked comparable with degrees 3 and 5"
           " based on its performance on one validation dataset!", ""),
      ])),
    S(_CH04, "3. **(Uncertainty Estimation)**", "Solution: Part I, Question 3",
      md("HW2", 19, "**Solution:** "),
      ran("train-data"),
      ran("train-plot"),
      md("HW2", 21, fixes=[("very disimilar to the training data", "very dissimilar to the training data")]),
      ran("ensemble"),
      ran("intervals"),
      ran("ensemble-plot"),
      md("HW2", 25, fixes=[
          ("but it's uncertainty doesn't scale", "but its uncertainty doesn't scale"),
          ("the model we picked via cross-validation in Exercise 3!", "the model we picked via cross-validation in Question 2!"),
      ]),
      ran("ensemble-sizes"),
      ran("ensemble-sizes-plot"),
      note("a discussion of the ensembles fitted on larger training sets (what happens in the data-rich and"
           " data-poor regions, and whether any of the intervals are ideal when data is abundant).")),
]

# ---------------------------------------------------------------------------
# 06-monte-carlo-integration (ps-hw3): Monte Carlo estimates of E[h(X)]
# ---------------------------------------------------------------------------
# Bugs fixed before re-running (numpy/scipy):
#   - rejection sampling averaged h over all proposals instead of the accepted samples;
#   - inverse_transform ignored the inverse CDF it was given (always the global F_inv_X_vec),
#     so "stratified sampling" was naive Monte Carlo, and the per-stratum inverse CDFs were wrong;
#   - Part III computed standard deviations and called them variances.

_CH06 = "06-monte-carlo-integration"
_CH06_P1 = "Exercise: Part I. Implement Some Monte Carlo Estimates"
_CH06_P2 = "Exercise: Part II. Debug Your Samplers"
_CH06_P3 = "Exercise: Part III: Variance Reduction"

PROMPT_EDITS[_CH06] = [
    (INTRO_OLD, INTRO_NEW),
    # Each list restarts after an unindented paragraph, so the source numbers show as is.
    ("2. ***Stratified Sampling*** using 4 strata", "4. ***Stratified Sampling*** using 4 strata"),
    ("3. Based on your experiments, would you feel comfortable", "2. Based on your experiments, would you feel comfortable"),
]

_STRATA_INV = (
    "F_inv_1 = lambda y: (1 + 2 * np.sqrt(6 * y)) * 6\nF_inv_2 = lambda y: (5 - 2 * np.sqrt(2 * (1 - 3 * y))) * 6\n"
    "F_inv_3 = lambda y: (5 + 2 * np.sqrt(3 * y - 1)) * 3\nF_inv_4 = lambda y: (9 - 2 * np.sqrt(3 * (1 - y))) * 3",
    "F_inv_1 = lambda y: 1 + 2 * np.sqrt(y)\nF_inv_2 = lambda y: 5 - 2 * np.sqrt(1 - y)\n"
    "F_inv_3 = lambda y: 5 + 2 * np.sqrt(y)\nF_inv_4 = lambda y: 9 - 2 * np.sqrt(1 - y)")

RERUN[_CH06] = [
    book("06-045"),
    run("imports", "HW3", 3, fixes=[("import scipy as sp\n", "import scipy as sp\nimport scipy.stats\n")]),
    run("pdf", "HW3", 5),
    run("cdf-area", "HW3", 7),
    run("inverse-cdf", "HW3", 9, fixes=[("    x_samples = F_inv_X_vec(y)", "    x_samples = F_inv_X(y)")]),
    run("inverse-cdf-estimate", "HW3", 10, fixes=[("inverse_transform(h, F_inv_X, S)", "inverse_transform(h, F_inv_X_vec, S)")]),
    run("proposals", "HW3", 12),
    run("proposal-plot", "HW3", 13, fixes=[("#choose an M_2 so that f_X <= M_2 * prop_1", "#choose an M_2 so that f_X <= M_2 * prop_2")]),
    run("rejection-normal", "HW3", 15, fixes=[
        ("    mean_rej = np.mean(h(samples))", "    #average h over the accepted samples only\n    mean_rej = np.mean(h(accepted_sampes))"),
    ]),
    run("rejection-uniform", "HW3", 16),
    run("importance", "HW3", 18),
    run("stratified", "HW3", 20, fixes=[("#define the four inverse pdf's", "#define the four inverse CDF's"), _STRATA_INV]),
    run("check-inverse", "HW3", 22),
    run("check-rejection", "HW3", 24),
    run("accepted", "HW3", 26),
    run("weights", "HW3", 28),
    run("importance-plot", "HW3", 30, fixes=[("sigma={}'.format(5, 1.6)", "sigma={}'.format(5.3, 1.6)")]),
    run("check-strata", "HW3", 32),
    run("h-strata", "HW3", 34),
    run("variances", "HW3", 37, fixes=[
        ("inverse_transform(h, F_inv_X, S)", "inverse_transform(h, F_inv_X_vec, S)"),
        ("np.std(", "np.var(", 6),
    ]),
    run("variances-print", "HW3", 38, fixes=[("'std of ", "'variance of ", 6)]),
]

_ONE_OVER_S = (r"\approx \sum_{s=1}^{S} h(X_s)", r"\approx \frac{1}{S}\sum_{s=1}^{S} h(X_s)")

SOLUTIONS += [
    S(_CH06, _CH06_P1, "Solution: Part I, Question 1",
      md("HW3", 4, "**Solution:**\n"),
      ran("imports", out=False),
      ran("pdf"),
      md("HW3", 6, "### 1. Inverse Transform Sampling\n"),
      ran("cdf-area"),
      md("HW3", 8, fixes=[_ONE_OVER_S]),
      ran("inverse-cdf"),
      ran("inverse-cdf-estimate")),
    S(_CH06, _CH06_P1, "Solution: Part I, Question 2",
      md("HW3", 11, "### 2. Rejection Sampling\n"),
      ran("proposals"),
      ran("proposal-plot"),
      md("HW3", 14, fixes=[_ONE_OVER_S]),
      ran("rejection-normal"),
      ran("rejection-uniform")),
    S(_CH06, _CH06_P1, "Solution: Part I, Question 3",
      md("HW3", 17, "### 3. Importance Sampling\n", fixes=[
          (r"\widehat{I}_{\text{IS}} = \sum_{s=1}^S", r"\widehat{I}_{\text{IS}} = \frac{1}{S}\sum_{s=1}^S"),
      ]),
      ran("importance")),
    S(_CH06, _CH06_P1, "Solution: Part I, Question 4",
      md("HW3", 19, "### 4. Stratified Sampling\n", fixes=[
          ("Note that we already have the inverse CDF's for each $f_i$:", "Inverting the CDF of each $f_i$ gives:"),
          (r"F^{-1}_1 = 6(1 + 2\sqrt{6y}),\; F^{-1}_2 = 6(5 - 2\sqrt{2(1 - 3y)}),\; F^{-1}_3 = 3(5 + 2\sqrt{3y - 1}),\; F^{-1}_4= 3(9 - 2\sqrt{3(1 - y)}).",
           r"F^{-1}_1 = 1 + 2\sqrt{y},\; F^{-1}_2 = 5 - 2\sqrt{1 - y},\; F^{-1}_3 = 5 + 2\sqrt{y},\; F^{-1}_4= 9 - 2\sqrt{1 - y}."),
      ]),
      ran("stratified")),
    S(_CH06, _CH06_P2, "Solution: Part II, Question 1",
      md("HW3", 21, "### 1. Inverse CDF and Rejection Sampling\n", fixes=[("Let's firt visualize", "Let's first visualize")]),
      ran("check-inverse"),
      md("HW3", 23, fixes=[("histogram of the 100 samples", "histogram of the 500 samples")]),
      ran("check-rejection"),
      # The re-run histograms don't show the uniform proposal doing "much better", so the
      # source's opening comparison is left out.
      md("HW3", 25, "More formally, recall that", keep_start=True, fixes=[
          ("More formally, recall that the effficiency", "Recall that the efficiency"),
          ("bounds the ratio $g/f_X$", "bounds the ratio $f_X/g$"),
          ("we'd accept the first sampler", "we'd expect the first sampler"),
      ]),
      ran("accepted"),
      md("HW3", 27, end="### 2. Importance Sampling MC Estimate", fixes=[
          ("From intuition and the formal proof from lecture, we know that fewer samples", "We know that fewer samples"),
      ])),
    S(_CH06, _CH06_P2, "Solution: Part II, Question 2",
      md("HW3", 27, "### 2. Importance Sampling MC Estimate\n"),
      ran("weights"),
      md("HW3", 29, fixes=[("this mean, again", "this means, again"), ("less dissimlar", "less dissimilar")]),
      ran("importance-plot"),
      md("HW3", 31, end="### Stratified Sampling", fixes=[
          ("hard to determin by", "hard to determine by"),
          ("visibly more heterogenous", "visibly more heterogeneous"),
          ("uniform importand distribution", "uniform importance distribution"),
      ])),
    S(_CH06, _CH06_P2, "Solution: Part II, Question 3",
      md("HW3", 31, "### Stratified Sampling\n"),
      ran("check-strata"),
      md("HW3", 33),
      ran("h-strata"),
      # With the stratified sampler fixed, the variance reduction is large (Part III), so the
      # source's prediction that it "may be very insignificant" is left out.
      md("HW3", 35, fixes=[
          ("We see that the convinient way", "We see that the convenient way"),
          (" This means that the variance reduction we get may be very insignificant!", ""),
      ])),
    S(_CH06, _CH06_P3, "Solution: Part III, Question 1",
      md("HW3", 36, "### 1. Computing sample variance\n"),
      ran("variances"),
      ran("variances-print"),
      md("HW3", 39, end="### 2. Overall comparison", fixes=[
          # The fixed stratified estimate has about a fifth of the naive variance, not "close to" it.
          ("Now, the variance of stratified sampling is smaller but close to the variance of naive MC with inverse CDF"
           " sampling. We expect stratified sampling to deliver a variance reduction, which it apparently does, but this"
           " reduction may be small (depending on our design choices). We'd anticipated this by visualizing the function"
           " $h$ across the strata.\n\nFurthermore, if you ran a smaller number of trials, the sample estimation of the"
           " variance itself will be noisy and you may find that the **estimated variance** of stratified sampling can be"
           " higher than the **estimated variance** of naive Monte Carlo!\n\n", ""),
          ("less that $S$ samples", "less than $S$ samples"),
          ("both higher that that of", "both higher than that of"),
      ]),
      note("a discussion of the stratified estimate's variance, which is the lowest of the six above.")),
    S(_CH06, _CH06_P3, "Solution: Part III, Question 2",
      md("HW3", 39, "### 2. Overall comparison\n")),
]

# ---------------------------------------------------------------------------
# 17-black-box-vi (ps-hw8): Bayesian neural networks with HMC and BBVI
# ---------------------------------------------------------------------------
# Sources: the BNN/HMC solution (HW_8) and the BBVI solution (HW_9), plus their HMC and BBVI
# classes. Re-run (autograd) with the book's ReLU network (the sources used rbf), after fixing:
#   - the likelihood used the variance 0.5^2 as a standard deviation;
#   - HMC's leapfrog changed the caller's position in place (so the Metropolis-Hastings step
#     compared the proposal with itself), skipped the last position update, and the trace was
#     thinned twice;
#   - BBVI's softplus output is the standard deviation of q (it scales the N(0, I) samples) but
#     the entropy treated it as a variance.
# The fixed BBVI matches the exact KL(q||p) optimum on the logistic unit test (mean -0.562,
# std 0.549 by quadrature); the fixed HMC recovers N(0, 1).

_CH17 = "17-black-box-vi"
_CH17_P1 = "Exercise: Part I: Inference for Bayesian Neural Networks Using HMC"
_CH17_P2 = "Exercise: Part II: Inference for BNNs Using Black-Box Variational Inference"
_CH17_P3 = "Exercise: Part III: Comparison"

PROMPT_EDITS[_CH17] = [(INTRO_OLD, INTRO_NEW)]
GAPS[_CH17] = ["Part I, Question 4", "Part II, Question 4", "Part III, Question 3"]

_HMC_FIXES = [
    ("        # initialize position\n        position = position_init\n",
     "        # initialize position (a copy, so the caller's array is not changed in place)\n"
     "        position = np.copy(position_init)\n"),
    ("        position_proposal = position #+ self.params['step_size'] * momentum\n",
     "        position_proposal = position + self.params['step_size'] * momentum\n"),
    ("        momentum_proposal = momentum - self.params['step_size'] * self.grad_potential_energy(position) / 2\n",
     "        momentum_proposal = momentum - self.params['step_size'] * self.grad_potential_energy(position_proposal) / 2\n"),
    ("        self.trace = self.trace[::self.params['thinning_factor']]",
     "        # (run_hmc already keeps every thinning_factor-th sample)"),
]
_BBVI_FIXES = [
    (re.compile(r"\bvar\b"), "std", 18),
    ("return 0.5 * np.sum(np.log(2 * np.pi * np.e) + np.log(std))", "return np.sum(0.5 * np.log(2 * np.pi * np.e) + np.log(std))"),
    ("Sigma = np.diag(std)", "Sigma = np.diag(std**2)"),
    ("Sigma_inv = np.linalg.det(Sigma)", "Sigma_inv = np.linalg.inv(Sigma)"),
]
_PLOT_SAMPLES = "for y_pred in y_pred_test:\n    ax.plot(x_test.flatten(), y_pred, color='gray', alpha=0.1)\n"

RERUN[_CH17] = [
    book("17-037"), book("17-038"), book("17-040"), book("17-042"), book("17-044"), book("17-045"),
    run("log-joint", "HW8", 12, fixes=[
        ("N = 12\n", "N = x_train.shape[1]\n"),
        # sigma_y is the variance 0.5^2
        ("constant = (-np.log(sigma_y) - 0.5 * np.log(2 * np.pi)) * N",
         "constant = (-0.5 * np.log(sigma_y) - 0.5 * np.log(2 * np.pi)) * N"),
        ("exponential = -0.5 * sigma_y**-2 * np.sum(", "exponential = -0.5 * sigma_y**-1 * np.sum("),
    ]),
    run("hmc-class", "HMC_PY", None, fixes=_HMC_FIXES),
    run("energies", "HW8", 13),
    # The source's step size (1e-2, 20 leapfrog steps) diverges on the book's ReLU network, so
    # this uses the settings the problem suggests.
    run("hmc-sample", "HW8", 15, fixes=[
        ("step_size = 1e-2\n", "step_size = 1e-3\n"),
        ("leapfrog_steps = 20\n", "leapfrog_steps = 50\n"),
        ("total_samples = 20000\n", "total_samples = 10000\n"),
        ("thinning_factor = 1\n", "thinning_factor = 2\n"),
    ]),
    run("trace-plot", "HW8", 17, fixes=[
        ("ax[row, col].plot(range(total_samples), HMC_sampler.trace[:, i]",
         "ax[row, col].plot(range(len(HMC_sampler.trace)), HMC_sampler.trace[:, i]"),
    ]),
    run("hmc-predictive", "HW8", 20, fixes=[
        ("posterior_samples = HMC_sampler.trace[::100]\n",
         "#100 randomly selected posterior samples\n"
         "posterior_samples = HMC_sampler.trace[random.choice(len(HMC_sampler.trace), 100, replace=False)]\n"),
        ("size=(total_samples, len(x_test)))", "size=(total_samples, x_test.shape[1]))"),
        ("label='test log-likelihood:{}'.format(np.round(log_likelihood, 4))", "label='95% predictive interval'"),
        ("ax.set_title('posterior predictive from HMC samples of the BNN posterior')",
         "ax.set_title('posterior predictive from HMC samples of the BNN posterior\\n(train log-likelihood: {})'.format(np.round(log_likelihood, 4)))"),
        ("ax.scatter(x_train.flatten(), y_train.flatten(), color='red', s=10, alpha=0.5, label='train data')",
         _PLOT_SAMPLES + "ax.scatter(x_train.flatten(), y_train.flatten(), color='red', s=10, alpha=0.5, label='train data')"),
    ]),
    run("bbvi-class", "BBVI_PY", None, fixes=_BBVI_FIXES),
    # Calls BBVI directly; the source went through wrapper modules (bayesian_regression.py,
    # inference.py) whose relevant steps are these.
    lit("bbvi-fit", """\
#log joint distribution of the BNN (log_prior and log_lklhd are defined in Part I)
def log_joint(W, t):
    return log_lklhd(W) + log_prior(W)

#initialize the variational means at the MLE weights and the variational std's near zero
init_mean = nn.weights.reshape((nn.D, ))
init_var = np.ones(init_mean.shape) * -10
init = np.hstack((init_mean, init_var))

#fit a mean-field Gaussian approximation of the posterior with BBVI
#(with step size 1e-3 the ELBO is still rising after 10,000 iterations)
bbvi = BBVI(log_joint, nn.D, S=500, random=random)
bbvi.fit(step_size=1e-2, max_iteration=10000, check_point=1000, params_init=init)

#keep the variational parameters with the best ELBO over the last 100 iterations
best = np.argmax(bbvi.ELBO[-100:])
var_mean, var_std = np.split(bbvi.variational_params[-100:][best], 2)"""),
    lit("vi-samples", """\
#100 samples from the variational approximation of the posterior
posterior_samples = var_mean + var_std * random.randn(100, nn.D)
#posterior predictive samples: network outputs plus observation noise
y_pred_test = nn.forward(posterior_samples, x_test).reshape((100, -1)) + random.normal(0, sigma_y**0.5, size=(100, x_test.shape[1]))
#compute the 95% predictive interval and the predictive mean
y_postpred_ub = np.percentile(y_pred_test, 97.5, axis=0)
y_postpred_lb = np.percentile(y_pred_test, 2.5, axis=0)
y_postpred_means = np.mean(y_pred_test, axis=0)"""),
    run("vi-plot", "HW9", 16, fixes=[
        ("ax.scatter(x_train, y_train, color='red', label='training data')",
         _PLOT_SAMPLES + "ax.scatter(x_train, y_train, color='red', label='training data')"),
    ]),
]

SOLUTIONS += [
    S(_CH17, _CH17_P1, "Solution: Part I, Question 1",
      ran("log-joint")),
    S(_CH17, "2. (**Sample from the Posterior**)", "Solution: Part I, Question 2",
      ran("hmc-class"),
      ran("energies"),
      ran("hmc-sample")),
    S(_CH17, "3. (**Visualize the Posterior Predictive**) Visualize 100 samples, randomly selected",
      "Solution: Part I, Question 3",
      ran("hmc-predictive")),
    S(_CH17, _CH17_P2, "Solution: Part II, Question 1",
      ran("bbvi-class"),
      note("a unit test of the implementation on the Bayesian logistic regression model.")),
    S(_CH17, "2. (**Variational Inference for BNNs**)", "Solution: Part II, Question 2",
      ran("bbvi-fit")),
    S(_CH17, "3. (**Visualize the Posterior Predictive**) Visualize 100 samples $\\mathbf{W}^s$",
      "Solution: Part II, Question 3",
      ran("vi-samples"),
      ran("vi-plot")),
    S(_CH17, _CH17_P3, "Solution: Part III, Question 1",
      md("HW9", 17, "### 5. Comparison with HMC Posterior Predictive\n", fixes=[
          ("Recall that the posterior preditive produced by HMC in HW#7 looks like:\n\n"
           "<img src=\"./hmc_pred.png\" style='height:300px;'>\n\n",
           "Compare the posterior predictive in Part II, Question 3 with the one produced by HMC in Part I, Question 3.\n\n"),
          ("whereas the predcitive uncertainty produced variational inference rather uniform",
           "whereas the predictive uncertainty produced by variational inference is rather uniform"),
      ]),
      note("whether the posterior approximation is good.")),
    S(_CH17, "2. (**Quality of Posterior Vs Quality of Posterior Predictive**)", "Solution: Part III, Question 2",
      ran("trace-plot"),
      md("HW8", 18),
      note("whether a mean-field Gaussian is a good approximation of the BNN posterior, which set of samples"
           " better captures it, and how posterior approximation relates to the quality of the posterior"
           " predictive uncertainties.")),
]


# ===========================================================================
# Labs
# ===========================================================================
# The converter collapsed each lab's answer cells (am207_map.LABS) as separate "Solution"
# dropdowns and hide-input code cells whose plots stayed visible. Here those cells are merged
# into one dropdown per question (LAB_REMOVE lists the cells they replace).

def _lab_cells(slug, numbers):
    return [f"{slug}-{n:03d}" for n in numbers]


# ---------------------------------------------------------------------------
# lab-03-monte-carlo-integration
# ---------------------------------------------------------------------------

_LAB3 = "lab-03-monte-carlo-integration"
LAB_REMOVE[_LAB3] = _lab_cells(_LAB3, range(8, 19))

SOLUTIONS += [
    S(_LAB3, "## Exercise: Monte Carlo Integration", "Solution",
      md("LAB3", 8, fixes=[(r"\widehat{I} = \sum_{s=1}^S", r"\widehat{I} = \frac{1}{S}\sum_{s=1}^S")]),
      code("LAB3", 9),
      md("LAB3", 10),
      code("LAB3", 11),
      md("LAB3", 12),
      code("LAB3", 13),
      md("LAB3", 14, fixes=[
          ('Looking at the "Nitty Gritty" slides page on importance sampling,',
           'Looking at the discussion of the design of $q$ ("Nitty Gritty of Importance Sampling") in [[ch:6]],'),
      ]),
      code("LAB3", 15),
      md("LAB3", 16),
      code("LAB3", 17),
      md("LAB3", 18)),
]

# ---------------------------------------------------------------------------
# lab-06-logistic-regression: one prompt cell; answers grouped by its sections.
# The data-loading cells 5-6 stay in place as setup. The Bayesian model uses pymc3: saved outputs.
# ---------------------------------------------------------------------------

_LAB6 = "lab-06-logistic-regression"
_LAB6_AFTER = "X = df[['mothers income (normalized)', 'mothers age (normalized)']].values"
LAB_REMOVE[_LAB6] = _lab_cells(_LAB6, range(7, 20))
GAPS[_LAB6] = ["Data Heterogeneity, Question 2"]

SOLUTIONS += [
    S(_LAB6, _LAB6_AFTER, "Solution: Modeling for Testing Scientific Hypotheses",
      code("LAB6", 7), code("LAB6", 9), code("LAB6", 10, out=False), code("LAB6", 11),
      note("an interpretation of the plots and of the MLE coefficients.")),
    S(_LAB6, _LAB6_AFTER, "Solution: Predictiveness",
      code("LAB6", 12), code("LAB6", 13),
      note("an interpretation of the accuracy and of the calibration plot.")),
    S(_LAB6, _LAB6_AFTER, "Solution: Uncertainty",
      code("LAB6", 14),
      note("the mean bootstrap coefficients, and an interpretation of the bootstrap decision boundaries.")),
    S(_LAB6, _LAB6_AFTER, "Solution: A Bayesian Approach",
      code("LAB6", 15), code("LAB6", 16), code("LAB6", 17), code("LAB6", 18), code("LAB6", 19),
      note("the comparison of the bootstrap and Bayesian uncertainties.")),
    S(_LAB6, _LAB6_AFTER, "Solution: Data Heterogeneity, Question 1",
      md("LAB6", 8, fixes=[("the data is heterogneous", "the data is heterogeneous")])),
]

# ---------------------------------------------------------------------------
# lab-08-vi-vs-hmc (pymc3: saved outputs, not re-run)
# ---------------------------------------------------------------------------

_LAB8 = "lab-08-vi-vs-hmc"
LAB_REMOVE[_LAB8] = _lab_cells(_LAB8, range(6, 15))

SOLUTIONS += [
    S(_LAB8, "#mixture weights", "Solution",
      text("*The saved outputs below come from the first model (a Bayesian logistic regression with a"
           " single observation), not from the Gaussian mixture: when the notebook was run, the mixture cell"
           " failed because it did not import `theano`. Re-running them requires `pymc3`.*"),
      code("LAB8", 6, fixes=[("#define the mixture model in pymc3\nwith pm.Model() as model:\n    w = pm.Normal",
                              "#define a Bayesian logistic regression model in pymc3 (the saved outputs below come from it)\n"
                              "with pm.Model() as model:\n    w = pm.Normal")]),
      code("LAB8", 7, fixes=[("#define the mixture model in pymc3\n", "#define the mixture model in pymc3\nimport theano\n")]),
      code("LAB8", 8),
      code("LAB8", 9),
      code("LAB8", 10),
      code("LAB8", 11),
      code("LAB8", 12),
      code("LAB8", 13),
      code("LAB8", 14),
      note("a comparison of how well HMC and variational inference capture the target distribution.")),
]

# ---------------------------------------------------------------------------
# lab-02-posterior-simulation (re-run, numpy/scipy)
# ---------------------------------------------------------------------------
# Fixes: the Normal-Normal posterior mean used s^2 m instead of sigma^2 m and its variance was
# missing the 1/(N s^2 + sigma^2) factor; N(mu, 5) has variance 5, so the data and the
# posterior predictive are drawn with standard deviation sqrt(5), not 5.

_LAB2 = "lab-02-posterior-simulation"
LAB_REMOVE[_LAB2] = _lab_cells(_LAB2, [7, 8, 9, 11, 12, 13])
PROMPT_EDITS[_LAB2] = [
    ("Say that you generated the data using 1,000 flips of a fair coin and observed 4,950 heads.",
     "Say that you generated the data using 10 flips of a coin whose probability of heads is $\\theta = 0.3$."),
]
GAPS[_LAB2] = ["The Beta-Binomial Posterior, Questions 2-3", "The Normal-Normal Model, Question 4"]

RERUN[_LAB2] = [
    book(f"{_LAB2}-003"),
    lit("scipy", "import scipy.stats"),
    run("data", "LAB2", 7),
    run("posterior", "LAB2", 8),
    run("predictive", "LAB2", 9),
    run("normal-posterior", "LAB2", 12, fixes=[
        ("data = np.random.normal(3, 5, size=50)", "data = np.random.normal(3, 5**0.5, size=N)"),
        ("mean = (data.sum() * s_squared + s_squared * m) / (N * s_squared + sigma_squared)",
         "mean = (data.sum() * s_squared + sigma_squared * m) / (N * s_squared + sigma_squared)"),
        ("variance = sigma_squared * s_squared\n", "variance = sigma_squared * s_squared / (N * s_squared + sigma_squared)\n"),
    ]),
    run("normal-predictive", "LAB2", 13, fixes=[
        ("np.random.normal(sample, 5) for sample in posterior_samples", "np.random.normal(sample, sigma_squared**0.5) for sample in posterior_samples"),
    ]),
]

SOLUTIONS += [
    S(_LAB2, "## The Beta-Binomial Posterior and Posterior Predictive", "Solution: Question 1",
      ran("data"), ran("posterior")),
    S(_LAB2, "## The Beta-Binomial Posterior and Posterior Predictive", "Solution: Question 4",
      ran("predictive"),
      note("what the comparison says about the model.")),
    S(_LAB2, "## The Normal-Normal Model", "Solution: Questions 1-2",
      md("LAB2", 11, "**Solution:** ", fixes=[
          ("recall from class that for the model", "Recall that for the model"),
          (r"\frac{s^2\sum_{n=1}^N y_n + s^2 m}{Ns^2 + \sigma^2}, s^2\sigma^2\right)",
           r"\frac{s^2\sum_{n=1}^N y_n + \sigma^2 m}{Ns^2 + \sigma^2}, \frac{s^2\sigma^2}{Ns^2 + \sigma^2}\right)"),
      ]),
      ran("normal-posterior")),
    S(_LAB2, "## The Normal-Normal Model", "Solution: Question 3",
      ran("normal-predictive"),
      note("what the comparison says about the model.")),
]

# ---------------------------------------------------------------------------
# lab-04-gibbs-metropolis-hastings (re-run, numpy/scipy)
# ---------------------------------------------------------------------------
# Book cell n is source cell n - 1 here (the source keeps a "**Solution:**" inside cell 4).
# Fixes: the conditional variance of a bivariate Gaussian is sigma^2 (1 - rho^2); numpy's normal
# takes a standard deviation (the Gibbs conditionals and the mixture proposal passed variances);
# the np.savetxt cells are dropped. The mixture example's "large" proposal effectively had
# standard deviation 9 (3**2), so it is now stated as variance 81, keeping the run the source shows.

_LAB4 = "lab-04-gibbs-metropolis-hastings"
LAB_REMOVE[_LAB4] = _lab_cells(_LAB4, [5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17])

RERUN[_LAB4] = [
    book(f"{_LAB4}-003"),
    lit("scipy", "import scipy.stats"),
    run("gibbs", "LAB4", 5, fixes=[
        ("#implementation of the posterior distributions", "#implementation of the conditional distributions"),
        ("sigma_x**2 * (1 - rho), 1)[0]", "(sigma_x**2 * (1 - rho**2))**0.5, 1)[0]"),
        ("sigma_y**2 * (1 - rho), 1)[0]", "(sigma_y**2 * (1 - rho**2))**0.5, 1)[0]"),
    ]),
    run("gibbs-run", "LAB4", 6),
    run("gibbs-plot", "LAB4", 8),
    run("mh", "LAB4", 10, fixes=[
        ("MH_samples, accepts = MH_sampler(S, log_target, init, burn_in, thinning, Sigma=Sigma_prop)",
         "MH_samples, accepts = MH_sampler(S, log_target, init, burn_in, thinning, Sigma=Sigma_prop)\n"
         "print('acceptance rate:', accepts)"),
    ]),
    run("mh-plot", "LAB4", 11),
    run("mixture", "LAB4", 13, fixes=[
        ("np.random.normal(current, sigma_sq**2)", "np.random.normal(current, sigma_sq**0.5)"),
        ("sigma_sqs[0]**2", "sigma_sqs[0]**0.5"),
        ("sigma_sqs[1]**2", "sigma_sqs[1]**0.5"),
    ]),
    run("mixture-run", "LAB4", 14, fixes=[
        ("#proposal variance\nsigma_sq_large = 3.\n", "#proposal variance (standard deviation 9)\nsigma_sq_large = 81.\n"),
    ]),
    run("mixture-plot", "LAB4", 16, fixes=[
        ("ax[0] = plot_samples(ax[0], target, samples_large_var[200:], 'target distribution vs all samples, S={}, init={}, proposal variance={}'.format(S, init, sigma_sq_large))",
         "ax[0] = plot_samples(ax[0], target, samples_large_var[burn_in:], 'target distribution vs samples after {} burn-in, S={}, init={}, proposal variance={}'.format(burn_in, S, init, sigma_sq_large))"),
        ("samples_small_var[200:]", "samples_small_var[burn_in:]"),
    ]),
]

SOLUTIONS += [
    S(_LAB4, "## Gibbs on a Bivariate Gaussian", "Solution",
      md("LAB4", 4, "**Solution:**\n", fixes=[
          (r"\sigma_Y^2(1 - \rho)", r"\sigma_Y^2(1 - \rho^2)", 2),
          (r"\sigma_X^2(1 - \rho)", r"\sigma_X^2(1 - \rho^2)", 2),
      ]),
      ran("gibbs"), ran("gibbs-run"), ran("gibbs-plot"),
      note("the effect of the initialization, the second Gaussian, and how the shape of the Gaussian affects the sampler.")),
    S(_LAB4, "## Gibbs versus Metropolis Hastings on a Bivariate Gaussian", "Solution",
      ran("mh"), ran("mh-plot"),
      note(r"the $\sigma^2 I_{2\times 2}$ proposals, and the discussion questions.")),
    S(_LAB4, "## Metropolis Hastings on a Mixture of Gaussians", "Solution",
      ran("mixture"), ran("mixture-run"), ran("mixture-plot"),
      note("a discussion of how the proposal variance and the initialization affect the sampler.")),
]

# ---------------------------------------------------------------------------
# lab-01-scientific-computing (new: from lab_1_solutions.ipynb; re-run, numpy/scipy/pandas)
# ---------------------------------------------------------------------------
# Fixes: the simulations used the covariance [[2.5, 1], [1, 2.5]] instead of the prompt's
# [[1.5, 1], [1, 1.5]], and drew epsilon ~ N(0, 5) with standard deviation 5 instead of sqrt(5);
# neither changes the expected values.

_LAB1 = "lab-01-scientific-computing"
_LAB1_Q = "## Model of USPS Package Processing Time"
_LAB1_COV = ("Sigma = np.ones((2, 2)) + 1.5 * np.eye(2)", "Sigma = np.ones((2, 2)) + 0.5 * np.eye(2)")

PROMPT_EDITS[_LAB1] = [
    ("This lab is adapted from AM207 (Harvard). Data files are in the book's `data/` folder.",
     "This lab is adapted from AM207 (Harvard). Data files are in the book's `data/` folder."
     " Worked solutions are collapsed: try each exercise before expanding them."),
]

RERUN[_LAB1] = [
    run("imports", "LAB1", 2),
    lit("scipy", "import scipy.stats"),
    run("poisson", "LAB1", 5),
    run("gaussian", "LAB1", 7),
    run("sample-total-time", "LAB1", 9, fixes=[
        _LAB1_COV,
        ("epsilons = np.random.normal(0, 5, size=total_packages)", "epsilons = np.random.normal(0, 5**0.5, size=total_packages)"),
    ]),
    run("total-time-hist", "LAB1", 10),
    run("totals", "LAB1", 12, fixes=[_LAB1_COV]),
    run("mean-total-time", "LAB1", 15),
]

SOLUTIONS += [
    S(_LAB1, _LAB1_Q, "Solution: Task 1",
      md("LAB1", 4, "**Solutions:**\n"),
      ran("poisson"),
      md("LAB1", 6),
      ran("gaussian"),
      md("LAB1", 8, end="**Processing Time as a Random Variable**", fixes=[
          ("around 120 $cm^3$ and 4 lbs", "around 120 $in^3$ and 4 lbs"),
          ("contorl which aspect", "control which aspect"),
          ("shape of the pdf is effected", "shape of the pdf is affected"),
      ]),
      md("LAB1", 11, "Compute the expected average weight and size of packages that arrive over a single day.\n", fixes=[
          ("so it's mean is", "so its mean is"),
          ("is the producted of the", "is the product of the"),
      ]),
      ran("totals"),
      md("LAB1", 13),
      note("the expected total size, and the expected average weight and size of a package.")),
    S(_LAB1, _LAB1_Q, "Solution: Task 2",
      md("LAB1", 14, "2. Compute the expected number of packages that arrives in a single day.\n",
         "3. Compute the expected processing time of a single package.", unindent=True)),
    S(_LAB1, _LAB1_Q, "Solution: Task 3",
      md("LAB1", 14, "3. Compute the expected processing time of a single package.\n",
         "4. Compute the expected processing time of all packages over a single day.", unindent=True, fixes=[
          ("We've already written a simulation for $T$ as part of the function `sample_total_time()`, we could have estimated",
           "The function `sample_total_time()` in Task 4 simulates $T$ for every package, so we could also have estimated"),
          ("[T]$ using simulations.", "[T]$ by simulation."),
      ])),
    S(_LAB1, _LAB1_Q, "Solution: Task 4",
      md("LAB1", 8, "**Processing Time as a Random Variable**", keep_start=True),
      ran("sample-total-time"),
      ran("total-time-hist"),
      md("LAB1", 11, end="---"),
      md("LAB1", 14, "4. Compute the expected processing time of all packages over a single day.\n", unindent=True, fixes=[
          ("The expression for a single package is\n$$\nT_{\\text{total}}", "The expression for the total processing time is\n$$\nT_{\\text{total}}"),
          ("from Question 3.", "from Task 3."),
          ("At the beginning of this notebook, we'd simulated samples", "Above, we simulated samples"),
      ]),
      ran("mean-total-time"),
      md("LAB1", 16, fixes=[
          ("This look close to", "This looks close to"),
          ("(by computint the various integrals exactly)", "(by computing the various integrals exactly)"),
      ])),
]

# ---------------------------------------------------------------------------
# lab-05-kl-divergence-pymc3 (new: from lab_5.ipynb, which has the worked solution; re-run)
# ---------------------------------------------------------------------------
# Fixes: scipy was used without being imported; the reverse-KL row of histograms was titled
# D_KL(p||q). The pymc3 exercise that only lab_5.ipynb has (a prompt the book does not
# include) is not added.

_LAB5 = "lab-05-kl-divergence-pymc3"
LAB_REMOVE[_LAB5] = _lab_cells(_LAB5, [7])
GAPS[_LAB5] = ["A Pooled Bayesian Model for the Kidney Cancer Data Set (Question)"]

RERUN[_LAB5] = [
    lit("imports", "import numpy as np\nimport matplotlib.pyplot as plt"),
    lit("scipy", "import scipy as sp\nimport scipy.stats"),
    run("optimal-q", "LAB5_SOL", 6),
    run("contours", "LAB5_SOL", 7),
    run("marginals", "LAB5_SOL", 8, fixes=[
        ("ax[1, 0].set_title('marginal distribution of x under q using D_KL(p||q)')",
         "ax[1, 0].set_title('marginal distribution of x under q using D_KL(q||p)')"),
        ("ax[1, 1].set_title('marginal distribution of y under q using D_KL(p||q)')",
         "ax[1, 1].set_title('marginal distribution of y under q using D_KL(q||p)')"),
    ]),
]

SOLUTIONS += [
    S(_LAB5, "## Which KL-Divergence Should We Optimize?", "Solution",
      ran("scipy"), ran("optimal-q"), ran("contours"), ran("marginals"),
      note("a written answer to which KL-divergence to use.")),
]

# ---------------------------------------------------------------------------
# lab-07-nonlinear-regression (re-run, autograd/sklearn)
# ---------------------------------------------------------------------------
# Fixes: the log-likelihood of the observed data now compares the observed y with predictions at
# the observed x (the NN term used the bootstrap y; the polynomial term scored the bootstrap
# sample) and includes the N in its constant; Part II bootstraps the network fits, as the prompt
# asks; 100 trials, as the prompt asks (it said 50 in the code and "1000" in two places in the
# prompt). Feedforward.fit never resets its traces, so the loop resets them before each fit
# (otherwise each fit copies every earlier trace).
# The data-loading and architecture cells (6, 7) and the Part II data generator (17) stay in place.

_LAB7 = "lab-07-nonlinear-regression"
LAB_REMOVE[_LAB7] = _lab_cells(_LAB7, [5, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 23])
PROMPT_EDITS[_LAB7] = [
    ("over these 1000 MLE models.<br><br>\n\n3. (**Model Evaluation**) Visualize the predictive distributions of your 1000"
     " MLE models (i.e. use them to predict on a range of uniformly spaced values from [-8, 8]",
     "over these 100 MLE models.<br><br>\n\n3. (**Model Evaluation**) Visualize the predictive distributions of your 100"
     " MLE models (i.e. use them to predict on a range of uniformly spaced values from [-8, 8]"),
    ("over these 1000 MLE models.<br><br>\n\n3. (**Model Evaluation**) Visualize the predictive distributions of your 1000"
     " MLE models (i.e. use them to predict on a range of uniformly spaced values from [-11, 11]",
     "over these 100 MLE models.<br><br>\n\n3. (**Model Evaluation**) Visualize the predictive distributions of your 100"
     " MLE models (i.e. use them to predict on a range of uniformly spaced values from [-11, 11]"),
]

_LAB7_LOGLIK = (
    "log_likelihood = lambda y_actual, y_pred: -0.5 * np.log(2 * np.pi * output_noise) - 0.5 * ((y_actual.flatten() - y_pred.flatten())**2).sum() / output_noise",
    "log_likelihood = lambda y_actual, y_pred: -0.5 * len(y_actual.flatten()) * np.log(2 * np.pi * output_noise) - 0.5 * ((y_actual.flatten() - y_pred.flatten())**2).sum() / output_noise")
_LAB7_SCORE = [
    ("trials = 50\n", "trials = 100\n"),
    ("    log_lkhd_nn.append(log_likelihood(bootstrap_y, y_train))", "    log_lkhd_nn.append(log_likelihood(y, y_train))"),
    ("    y_train = linear_model.predict(bootstrap_x_poly)\n    log_lkhd_poly.append(log_likelihood(bootstrap_y, y_train.flatten()))",
     "    y_train = linear_model.predict(x_poly)\n    log_lkhd_poly.append(log_likelihood(y, y_train.flatten()))"),
]
_LAB7_FIT = "    #fit my neural network to minimize MSE on the given data\n    nn.fit(x.reshape((1, -1)), y.reshape((1, -1)), params)\n"
_LAB7_RESET = ("    #reset the optimization traces kept by the previous fit\n"
               "    nn.objective_trace = np.empty((1, 1))\n    nn.weight_trace = np.empty((1, nn.D))\n")
_LAB7_PLOT = [("#plot the 50 neural network and polynomial models", "#plot the neural network and polynomial models")]

RERUN[_LAB7] = [
    book(f"{_LAB7}-002"), book(f"{_LAB7}-003"), book(f"{_LAB7}-006"), book(f"{_LAB7}-007"),
    run("fit-one-nn", "LAB7", 8), run("plot-one-nn", "LAB7", 9), run("one-poly", "LAB7", 11),
    run("ensembles", "LAB7", 13, fixes=[_LAB7_LOGLIK, *_LAB7_SCORE, (_LAB7_FIT, _LAB7_RESET + _LAB7_FIT)]),
    run("ensembles-plot", "LAB7", 14, fixes=_LAB7_PLOT),
    book(f"{_LAB7}-017"),
    run("fit-one-nn-2", "LAB7", 18), run("plot-one-nn-2", "LAB7", 19), run("one-poly-2", "LAB7", 21),
    run("ensembles-2", "LAB7", 22, fixes=[
        # the Part II data has noise variance y_var = 1.0, not 0.5**2
        ("##define normal log-likelihood with variance 0.5**2\noutput_noise = 0.5**2\n",
         "##define normal log-likelihood with the noise variance of the data\noutput_noise = y_var\n"),
        _LAB7_LOGLIK, *_LAB7_SCORE,
        (_LAB7_FIT, _LAB7_RESET + "    #fit my neural network to minimize MSE on the bootstrap sample\n"
                                  "    nn.fit(bootstrap_x.reshape((1, -1)), bootstrap_y.reshape((1, -1)), params)\n"),
    ]),
    run("ensembles-plot-2", "LAB7", 23, fixes=_LAB7_PLOT),
]

_LAB7_NOTE = note("which model class fits the data better, and which gives better aleatoric and epistemic uncertainty.")

SOLUTIONS += [
    S(_LAB7, "###define rbf activation function", "Solution: Part I",
      md("LAB7", 5), ran("fit-one-nn"), ran("plot-one-nn"),
      md("LAB7", 10), ran("one-poly"),
      md("LAB7", 12), ran("ensembles"), ran("ensembles-plot"),
      _LAB7_NOTE),
    S(_LAB7, "## generate training data", "Solution: Part II",
      md("LAB7", 16), ran("fit-one-nn-2"), ran("plot-one-nn-2"),
      md("LAB7", 20), ran("one-poly-2"),
      ran("ensembles-2"), ran("ensembles-plot-2"),
      _LAB7_NOTE),
]

# Pages with no source solution at all.
GAPS["14-hamiltonian-monte-carlo"] = ["the whole problem set (Exercises 1-8 and 10)"]
GAPS["lab-09-hidden-markov-models"] = ["the whole lab"]
