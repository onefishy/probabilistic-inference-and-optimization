"""Mapping from the AM207 (Fall 2021) course repo onto the book's structure.

Everything that required a human judgement call during conversion lives here, so
that `convert_am207.py` stays mechanical.
"""

# Book parts, in order. Each part ends with an "Applications and Broader Impact" chapter.
PARTS = [
    ("I", "Foundations of Inference", "impact-1-foundations"),
    ("II", "Sampling and Monte Carlo", "impact-2-sampling"),
    ("III", "Latent Variables and Variational Inference", "impact-3-latent-variables"),
    ("IV", "Optimization", "impact-4-optimization"),
    ("V", "Advanced MCMC", "impact-5-advanced-mcmc"),
    ("VI", "Bayesian Deep Learning", "impact-6-bayesian-deep-learning"),
]

# lecture number -> (chapter slug, chapter title, part index, course week)
LECTURES = {
    1: ("01-overview", "Overview: Stochastic Methods for Data Analysis", 0, 1),
    2: ("02-maximum-likelihood", "Maximum Likelihood Estimation", 0, 2),
    3: ("03-bayesian-modeling", "Bayesian Modeling", 0, 2),
    4: ("04-bayesian-vs-frequentist", "Bayesian versus Frequentist Inference", 0, 3),
    5: ("05-sampling", "Sampling for Posterior Simulation", 1, 3),
    6: ("06-monte-carlo-integration", "Monte Carlo Integration", 1, 4),
    7: ("07-mcmc", "Markov Chain Monte Carlo", 1, 4),
    8: ("08-metropolis-hastings-gibbs", "Metropolis-Hastings and Gibbs", 1, 5),
    9: ("09-latent-variable-models", "Latent Variable Models and MLE", 2, 5),
    10: ("10-variational-inference", "Bayesian Latent Variable Models and Variational Inference", 2, 6),
    11: ("11-hierarchical-models", "Hierarchical Models", 2, 6),
    12: ("12-logistic-regression-gradient-descent", "Logistic Regression and Gradient Descent", 3, 7),
    13: ("13-sgd-simulated-annealing", "Stochastic Gradient Descent and Simulated Annealing", 3, 7),
    14: ("14-hamiltonian-monte-carlo", "Hamiltonian Monte Carlo", 4, 8),
    15: ("15-parallel-tempering-sghmc", "Parallel Tempering and Stochastic HMC", 4, 8),
    16: ("16-neural-network-regression", "Neural Network Models for Regression", 5, 9),
    17: ("17-black-box-vi", "Black-box Variational Inference", 5, 9),
    18: ("18-automatic-differentiation", "Automatic Differentiation", 5, 10),
    19: ("19-vi-in-context", "Variational Inference in Context", 5, 10),
    20: ("20-variational-autoencoders", "Variational Autoencoders", 5, 11),
    21: ("21-implementing-vaes", "Implementing Variational Autoencoders", 5, 11),
}

# Summary notebooks: (notebook stem, cell index) -> action.
#   ("recap", L)       -> appended to chapter L under "Summary"
#   ("section", L, T)  -> appended to chapter L as its own section titled T
#   ("impact", part)   -> collected into that part's impact chapter
#   ("drop",)          -> course logistics / classroom framing, not book content
# Cells 0-1 of every summary (course header + logo) are always dropped.
SUMMARY_CELLS = {
    ("lecture_1_summary_slides", 2): ("drop",),
    ("lecture_1_summary_slides", 3): ("drop",),
    ("lecture_1_summary_slides", 4): ("drop",),
    ("lecture_1_summary_slides", 5): ("drop",),
    ("lecture_1_summary_slides", 6): ("drop",),
    ("lecture_1_summary_slides", 7): ("drop",),
    ("lecture_1_summary_slides", 8): ("drop",),
    ("lecture_2_summary", 2): ("drop",),
    ("lecture_2_summary", 3): ("recap", 1),
    ("lecture_2_summary", 4): ("impact", 0),
    ("lecture_3_summary", 2): ("recap", 3),
    ("lecture_4_summary", 2): ("recap", 4),
    ("lecture_5_summary", 2): ("recap", 5),
    ("lecture_6_summary", 2): ("recap", 6),
    ("lecture_7_summary", 2): ("recap", 7),
    ("lecture_8_summary", 2): ("recap", 8),  # "Grades!" subsection stripped in the converter
    ("lecture_11_summary", 2): ("recap", 11),
    ("lecture_12_summary", 2): ("recap", 12),
    ("lecture_13_summary", 2): ("recap", 13),
    ("lecture_14_summary", 2): ("recap", 14),
    ("lecture_15_summary", 2): ("section", 14, "Frequently Asked Questions About HMC"),
    ("lecture_16_summary", 2): ("recap", 16),
    ("lecture_16_summary", 3): ("recap", 16),
    ("lecture_16_summary", 4): ("impact", 5),
    ("lecture_16_summary", 5): ("impact", 5),
    ("lecture_16_summary", 6): ("impact", 5),
    ("lecture_16_summary", 7): ("impact", 5),
    ("lecture_16_summary", 8): ("impact", 5),
    ("lecture_17_summary", 2): ("recap", 17),
    ("lecture_19_summary", 2): ("recap", 19),
    ("lecture_19_summary", 3): ("section", 19, "New Developments in Deep Bayes"),
    ("lecture_19_summary", 4): ("section", 19, None),
    ("lecture_19_summary", 5): ("section", 19, None),
    ("lecture_19_summary", 6): ("section", 19, None),
    ("lecture_19_summary", 7): ("section", 19, None),
    ("lecture_19_summary", 8): ("section", 19, None),
    ("lecture_19_summary", 9): ("section", 19, None),
    ("lecture_19_summary", 10): ("section", 19, None),
}

# Summary subsections (by heading text) to strip even inside kept cells.
SUMMARY_DROP_HEADINGS = ["Grades!"]

# Reading-list groups from weekN.md: (week, group title prefix) -> lecture number,
# or ("impact", part index), or None to drop the group.
READING_GROUPS = {
    (1, "Preparatory Readings"): 1,
    (1, "Promises of Machine Learning"): ("impact", 0),
    (1, "Potential Dangers of Machine Learning"): ("impact", 0),
    (1, "Machine Learning and Ethics"): ("impact", 0),
    (1, "Linear Regression"): 1,
    (1, "Bayesian Linear Regression"): 1,
    (2, "Applications and Broader Impact"): ("impact", 0),
    (2, "Optimization"): 2,
    (2, "Statistics"): 3,
    (2, "Other Reference"): 3,
    (3, "Applications and Broader Impact"): ("impact", 0),
    (3, "Bayesian versus Frequentist Inference"): 4,
    (3, "Sampling"): 5,
    (4, "Applications and Broader Impact"): ("impact", 1),
    (4, "Monte Carlo Integration"): 6,
    (4, "Markov Chain Monte Carlo"): 7,
    (5, "Applications and Broader Impact"): ("impact", 1),
    (5, "MCMC Diagnostics"): 8,
    (5, "More on Thinning"): 8,
    (5, "More on Chain Length"): 8,
    (5, "Latent Variable Models"): 9,
    (6, "Applications and Broader Impact"): ("impact", 2),
    (6, "Variational Inference"): 10,
    (6, "Hierarchical Bayes and Model Selection"): 11,
    (6, "pymc3"): None,  # tutorials for a deprecated library
    (7, "Applications and Broader Impact"): ("impact", 3),
    (7, "Gradient Descent and Stochastic Gradient Descent"): 12,
    (7, "Model Selection for Bayesian Models"): 11,
    (7, "Simulated Annealing and Non-Convex Optimization"): 13,
    (8, "Applications and Broader Impact"): ("impact", 4),
    (8, "Hamiltonian Monte Carlo"): 14,
    (8, "For Nice Visualizations of HMC Samplers"): 14,
    (8, "For those really interested in rigor"): 14,
    (8, "Parallel Tempering"): 15,
    (8, "Improvements to HMC and MCMC in General"): 15,
    (9, "Applications and Broader Impact"): ("impact", 5),
    (9, "Variational Inference for Bayesian Neural Networks"): 17,
    (10, "Applications and Broader Impact"): ("impact", 5),
    (10, "Automatic Differentiation"): 18,
    (10, "Approximate Inference for Deep Bayesian Models"): 19,
    (10, "Evaluating Approximate Inference for Deep Bayesian Models"): 19,
    (10, "Alternate Models for Deep Bayesian Networks"): 19,
    (11, "Applications and Broader Impact"): ("impact", 5),
    (11, "Variational Autoencoders"): 20,
}

# Links that readers outside Harvard cannot open.
PRIVATE_LINK_MARKERS = ["canvas.harvard.edu"]

# Homework: (HW number, segment index) -> lecture whose chapter gets the problem set.
# Segments are split at top-level "# Problem Description" headings; HWs without
# such headings are a single segment 0.
HOMEWORK = {
    (0, 0): 1,
    (1, 0): 3,
    (2, 0): 4,
    (3, 0): 6,
    (4, 0): 9,   # EM for data augmentation
    (4, 1): 8,   # MH-in-Gibbs on kidney cancer data
    (5, 0): 10,  # theory of EM and VI
    (5, 1): 11,  # empirical / hierarchical Bayes on kidney cancer data
    (6, 0): 13,
    (7, 0): 14,
    (8, 0): 17,
}

# Lecture-note cells that are course logistics rather than book content:
# lecture -> cell indices to drop. Lecture 1, cells 40-58: "What is AM207?", required
# technology, graded components, policies, office hours, Piazza, advice for the semester.
LECTURE_DROP_CELLS = {
    1: set(range(40, 59)),
}

# Lectures whose "Outline" cell no longer matches the chapter once logistics are dropped.
SKIP_OUTLINE = {1}

# Exact-text fixes applied after conversion: (chapter slug prefix, old, new).
# Each `old` must occur exactly once in that chapter. `[[ps:KEY]]` links to a problem
# set ("Chapter N problem set"); `[[ps:KEY|text]]` uses custom link text. KEY is the
# homework number, plus a/b for homeworks split across two chapters (see HOMEWORK).
TEXT_FIXES = [
    # Homework numbers -> the problem set that now holds that homework.
    ("01", "In HW#0 you will compare", "In the [[ps:0|problem set at the end of this chapter]] you will compare"),
    ("04", "As you have seen in HW0,", "As you have seen in the [[ps:0]],"),
    ("04", "the formula you derived in HW0)", "the formula you derived in the [[ps:0]])"),
    ("08", "**In this homework, we focus on the mechanics", "**In this problem set, we focus on the mechanics"),
    ("08", "In the next homework, we will focus on interpreting", "In the [[ps:5b]], we will focus on interpreting"),
    ("08", "(recall the discussion in Homework #1 about priors)", "(recall the discussion of priors in the [[ps:1]])"),
    ("08", "We are not asking you in this homework to achieve", "We are not asking you in this problem set to achieve"),
    ("11", "Consider the kidney cancer data set from Homework #4:", "Consider the kidney cancer data set from the [[ps:4b]]:"),
    ("11", "**In this homework, we focus on comparing", "**In this problem set, we focus on comparing"),
    ("11", "with your sampler from the previous homework,", "with your sampler from the [[ps:4b]],"),
    ("11", "In Homework #4, we considered the broader impact", "In the [[ps:4b]], we considered the broader impact"),
    ("11", "broader impact analysis from HW#4,", "broader impact analysis from the [[ps:4b]],"),
    ("14", "What happened in HW#5 with your sampler?", "What happened with your sampler in the [[ps:5b]]?"),
    ("14", "In this homework, we evaluate the usefulness", "In this problem set, we evaluate the usefulness"),
    ("14", "Just as in Homework #2, we want", "Just as in the [[ps:2]], we want"),
    ("14", "In Homework #2, we saw that the epistemic", "In the [[ps:2]], we saw that the epistemic"),
    ("16", "analytically (see Homework #0)", "analytically (see the [[ps:0]])"),
    ("17", "Bayesian linear regression, see HW#0)", "Bayesian linear regression, see the [[ps:0]])"),
    ("17", "In this homework you will explore", "In this problem set you will explore"),
    ("19", "In Homework #0, you've seen that", "In the [[ps:0]], you've seen that"),
    ("19", "You've seen in HW#7 that even", "You've seen in the [[ps:7]] that even"),
    ("19", "What did we observe in HW#8?", "What did we observe in the [[ps:8]]?"),
    ("impact-1", "for the dataset in Homework #0.", "for the dataset in the [[ps:0]]."),
    ("impact-1", "preprocessed like in HW#0?", "preprocessed like in the [[ps:0]]?"),
]

# Labs (from ~/Teaching/AM207_Lectures2020): number -> (notebook path relative to the
# labs source folder, slug, title, answer cells). Answer cells are worked solutions to
# the lab's exercise prompts: markdown goes in a collapsed "Solution" dropdown and code
# is collapsed behind "Show code" (outputs stay visible). Solution notebooks/folders
# and Lab_8/alpha_hmc.py (a full HMC implementation not used by the lab) are not included.
LABS = {
    1: ("Lab_1/lab_1.ipynb", "lab-01-scientific-computing",
        "Review of Scientific Computing in Python", set()),
    2: ("Lab_2/lab_2.ipynb", "lab-02-posterior-simulation",
        "Posterior and Posterior Predictive Simulation", {7, 8, 9, 11, 12, 13}),
    3: ("Lab_3/lab_3.ipynb", "lab-03-monte-carlo-integration",
        "Sampling and Monte Carlo Integration", set(range(8, 19))),
    4: ("Lab_4/lab_4.ipynb", "lab-04-gibbs-metropolis-hastings",
        "Gibbs and Metropolis-Hastings Sampling", {5, 6, 7, 8, 10, 11, 13, 14, 15, 16}),
    # lab_5.ipynb in the same folder has an inline worked solution; the slides version
    # is the fuller teaching notebook.
    5: ("Lab_5/Lab_5/lab_5_slides.ipynb", "lab-05-kl-divergence-pymc3",
        "KL-Divergence and Modeling with pymc3", {7}),
    6: ("Lab_6/Lab_6/lab_6.ipynb", "lab-06-logistic-regression",
        "Interpreting and Evaluating Logistic Regression Models", set(range(5, 20))),
    7: ("Lab_7/lab_7.ipynb", "lab-07-nonlinear-regression",
        "Non-Linear Models for Regression", {6, 7, 8, 9, 11, 13, 14, 17, 18, 19, 21, 22, 23}),
    8: ("Lab_8/lab_8.ipynb", "lab-08-vi-vs-hmc",
        "Variational Inference vs HMC", set(range(6, 15))),
    9: ("Lab_9/lab_9.ipynb", "lab-09-hidden-markov-models",
        "Inference and Learning for Discrete-State HMMs", set()),
}

# Data files the labs read (copied into data/).
LAB_DATA = ["Lab_5/Lab_5/kcancer.csv", "Lab_6/Lab_6/lab_6_data.csv", "Lab_7/lab_7_data.csv",
            "Lab_9/Shakespeare_correct.txt", "Lab_9/Shakespeare_typos.txt"]

# In-class exercise and lab references. `[[lab:N]]` links to lab N; `[[ch:L]]` links to
# the chapter made from lecture L. The dated "In-Class Exercise MM.DD" names come from
# an earlier offering and were matched to labs/chapters by topic.
TEXT_FIXES += [
    ("07", "(recall your experiments tuning rejection sampling for the non-conjugate Bayesain model for birth weights in *In-Class Exercise 09.17*)",
     "(recall how difficult it is to tune rejection sampling; see [[ch:5]])"),
    ("13", "Using level curves (see In-Class Exercise #1)", "Using level curves (see [[ch:2]])"),
    ("14", "In the In-Class Exercise 10.14, everyone struggled with", "In class, everyone struggled with"),
    ("14", "give me the solution to the In-Class Exercise 10.19, i.e. GIVE ME YOUR IMPLEMENTATION OF HMC",
     "GIVE ME YOUR IMPLEMENTATION OF HMC"),
    ("14", "In In-Class Exercise 10.13, we studied the problem", "In [[lab:6]], we studied the problem"),
    ("14", "In In-Class Exercise 10.13, we interpreted the output", "In [[lab:6]], we interpreted the output"),
    ("14", "(see In-Class Exercise 10.13)", "(see [[lab:6]])"),
    ("14", "Use your implementation of HMC from In-Class Exercise 10.20 to sample",
     "Use your own implementation of HMC (see the algorithm earlier in this chapter) to sample", 2),
    ("19", "In Lab #5, you explored", "In [[lab:5]], you explored"),
    # The multimodal VI-vs-HMC comparison is Lab 8 in this set of labs.
    ("19", "In Lab #7, you've seen", "In [[lab:8]], you've seen"),
    ("impact-1", "From the first in-class exercise you've already seen", "From the [[ps:0]] you've already seen"),
    # Lecture/homework numbers from the 2019 offering inside the labs.
    ("lab-07", "From Lecture #14, we've seen", "From [[ch:16]], we've seen"),
    ("lab-07", " (this is the same dataset used in HW#7)", ""),
]
