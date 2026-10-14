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
                                              unless keep_start=True)
            code(src, cell, out, fixes)       a code cell and (out=True) its saved outputs
            ran(step)                         code and outputs of a re-run step (RERUN)
            text(markdown)                    connecting text written for the book
            note(markdown)                    "*Not covered here: ...*" for partial answers
`fixes` are exact (old, new[, count]) edits; a fix that no longer matches stops the run.
`[[ps:KEY]]`, `[[ch:LECTURE]]` and `[[lab:N]]` placeholders become cross-references.
"""

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
}


def S(page, after, title, *segments, key=None):
    return {"page": page, "after": after, "title": title, "segments": segments, "key": key}


def md(src, cell, start=None, end=None, fixes=(), keep_start=False):
    return ("md", src, cell, start, end, tuple(fixes), keep_start)


def code(src, cell, out=True, fixes=()):
    return ("code", src, cell, out, tuple(fixes))


def ran(step, code=True, out=True):
    return ("ran", step, code, out)


def text(markdown):
    return ("text", markdown)


def note(markdown):
    return ("note", markdown)


# Re-run steps: book(cell id) runs a book cell (starter code) without showing it;
# run(key, src, cell, fixes) and lit(key, source) run code that solutions show via ran(key).
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
    "*This plot comes from the original `pymc3` run, which drew the raw rates almost transparent;"
    " only the posterior means (green) are visible.*")

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
          (r"\| [ lambda_1,  lambda_2] - [ 2.05384, 0 ] \|_2 < 1e^{-3}", r"\| [ \lambda_1,  \lambda_2] - [ 2.05384, 0 ] \|_2 < 10^{-3}"),
          ("(which involves suming over", "(which involves summing over"),
      ]),
      code("HW6", 14),
      code("HW6", 15),
      md("HW6", 16)),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 3",
      md("HW6", 17, "### Implementation: Stochastic Gradient Descent\n"),
      code("HW6", 18),
      code("HW6", 19),
      md("HW6", 20, fixes=[
          ("that descreases the loss", "that decreases the loss"),
          ("decrease form one iteration", "decrease from one iteration"),
      ]),
      code("HW6", 21),
      md("HW6", 22, fixes=[
          # The run above (cell output) took 751 iterations.
          ("after 1,990 steps (versus", "after 751 steps (versus"),
          ("around the optimal total loss of -9.93410279384.", "around the optimal total loss of -9.9341."),
          ("When we examing the total loss", "When we examine the total loss"),
          ("is ocillating around", "is oscillating around"),
      ])),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 4",
      md("HW6", 13, "A note on the correct loss function to use:\n", "A note on the correct stopping condition to use:", fixes=[
          ("the loss funtion averaged", "the loss function averaged"),
      ])),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 5",
      md("HW6", 23, "#### Speed:\n", "<a id='stepsize'></a>", fixes=[
          # Match the timings printed by the runs in Questions 2 and 3.
          ("We see that it takes 0.000573873519897 seconds to compute one gradient for gradient descent, "
           "while it takes around 0.000241994857788 seconds to compute one gradient for stochastic gradient descent.",
           "In the runs above, it takes about 0.00024 seconds to compute one gradient for gradient descent, "
           "while it takes around 0.00011 to 0.00017 seconds to compute one gradient for stochastic gradient descent."),
          (" For example, you can try to perform gradient descent in your Long Form Homework #1 and see how that will change your training time.", ""),
      ])),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 6",
      md("HW6", 23, "#### Sensitivity to Stepsize:\n"),
      code("HW6", 24),
      md("HW6", 25),
      code("HW6", 26),
      code("HW6", 27),
      code("HW6", 28),
      code("HW6", 29),
      code("HW6", 30),
      code("HW6", 31),
      code("HW6", 32),
      # The source's discussion of these SGD runs describes other step sizes (0.01-1) and
      # iteration counts that the outputs above do not show, so only its conclusion is kept.
      md("HW6", 33, "The same experiments with gradient descent shows", "<a id='init'></a>", keep_start=True, fixes=[
          ("The same experiments with gradient descent shows", "The same experiments with gradient descent show"),
      ]),
      note("a step-by-step discussion of the SGD runs for each step size.")),
    S(_CH13, _CH13_P1, "Solution: Part I, Question 7",
      md("HW6", 33, "#### Sensitivity to Initialization\n"),
      code("HW6", 34),
      md("HW6", 35),
      code("HW6", 36),
      md("HW6", 37, fixes=[
          ("In lecture, we discussed how this descent", "Earlier in this chapter we saw how this descent"),
      ]),
      code("HW6", 38),
      md("HW6", 39, fixes=[
          ("We see that with step size 1., stochastic gradient descent", "We see that with step size 10, stochastic gradient descent"),
      ]),
      code("HW6", 40),
      md("HW6", 41),
      code("HW6", 42),
      md("HW6", 43),
      note("gradient descent with a learning rate of 50.")),
]
