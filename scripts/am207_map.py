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
# is collapsed behind "Show code" (outputs stay visible). scripts/add_solutions.py then
# merges each question's answer cells into one collapsed dropdown (see solutions_map.py).
# Lab_8/alpha_hmc.py (a full HMC implementation not used by the lab) is not included.
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
    ("14", "In the In-Class Exercise 10.14, everyone struggled with finding `pymc3` documentation on how to compare models "
     "using WAIC and **no one caught the `pymc3` error about the WAIC computation**",
     "It is hard to find `pymc3` documentation on how to compare models using WAIC, and **the `pymc3` error about "
     "the WAIC computation is easy to miss**"),
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

# Course framing ("in lecture", "this class", "today", "last week", "Problem N", ...) -> book wording.
TEXT_FIXES += [
    ("01", "## What is this course about?", "## What is this book about?"),
    ("01", "*(Material covered in CS109A or equivalent)*\n\n", ""),
    ("01", "*(Material covered in CS109 B or equivalent)*\n\n", ""),
    ("02", "Recall that in Lecture #1 we gave", "Recall that in [[ch:1]] we gave"),
    ("03", "using the $\\alpha$'s you chose in Problem 1.", "using the $\\alpha$'s you chose in Question 1.", 3),
    ("04", "This will become a very important idea during the second half of the course!",
     "This will become a very important idea in the second half of the book!"),
    ("04", "The goal in this assignment is to explore", "The goal in this problem set is to explore"),
    ("04", "The ideas developed in this assignment will become a major focus in the latter part of the course",
     "The ideas developed in this problem set will become a major focus in the latter part of the book"),
    ("04", "How do we compute the posterior distribution? From Piazza: \"is there a standard procedure?\"",
     "How do we compute the posterior distribution? Is there a standard procedure?"),
    ("04", "**(Model Selection)** Later in the course, we will study", "**(Model Selection)** In [[ch:13]], we will study"),
    ("04", "in Problem 1", "in Question 1", 2),
    ("04", "in Problem 2", "in Question 2", 3),
    ("04", "Read Problem 3 before implementing Problem 2", "Read Question 3 before implementing Question 2"),
    ("04", "**Extra Credit:** When the feature map", "**Optional:** When the feature map"),
    # The book does not cover Gaussian processes.
    ("04", " We will revisit the connection between Bayesian kernel regression and Gaussian processes in the latter part of the course.", ""),
    ("05", "Now that we can sample from any distribution, this class is over right?",
     "Now that we can sample from any distribution, we're done, right?"),
    ("05", "the info in this class?", "the info in this book?"),
    ("05", "**the big-picture story** of the class,", "**the big-picture story** of the book,"),
    ("06", "Last week we studied ways of", "In [[ch:5]] we studied ways of"),
    ("06", "properties of these samplers discussed in class", "properties of these samplers discussed in [[ch:5]] and this chapter", 3),
    ("06", "Based on the discussions in lecture,", "Based on the discussion in this chapter,"),
    ("07", "find out in Lecture #9 that MLE inference be just as difficult",
     "find out in [[ch:9]] that MLE inference can be just as difficult"),
    ("08", "(recall the discussion in Lecture #3)", "(recall the discussion in [[ch:3]])"),
    ("08", "Today, rather than directly proving", "In this chapter, rather than directly proving"),
    ("09", "The KL-divergence has information theoretic interpretations that we will explore later in the course.",
     "The KL-divergence also has information theoretic interpretations."),
    ("09", " We will use them later in the course.", ""),
    ("09", "Today, we will study models with one type of interaction:",
     "In this chapter, we will study models with one type of interaction:"),
    ("09", "derive EM via the ELBO in this lecture because", "derive EM via the ELBO in this chapter because"),
    ("09", "when we cover non-convex optimization later in the course.", "when we cover non-convex optimization in [[ch:13]]."),
    ("10", "Today we will maximize the $ELBO$", "In this chapter, we will maximize the $ELBO$"),
    ("10", "Two of the major development we will cover later in the semester address",
     "Two of the major developments we will cover in [[ch:17]] address"),
    ("10", "You'll need to refer to relevant lecture notes on the derivations of EM and the derivation of the variational inference objective.",
     "You'll need to refer to the derivation of EM in [[ch:9]] and the derivation of the variational inference objective earlier in this chapter."),
    ("10", "latent variable models we studied in lecture:", "latent variable models we studied in [[ch:9]]:"),
    ("10", "Gaussian Mixture Models in Lecture 7 to help", "Gaussian Mixture Models in [[ch:9]] to help"),
    ("10", "In the notes for Lecture 8, we introduce a way", "Earlier in this chapter, we introduced a way"),
    ("10", "Gaussian Mixture Models in Lecture 8 to help", "Gaussian Mixture Models earlier in this chapter to help"),
    ("10", "Gaussian Mixture Models in Lecture 8 and predict", "Gaussian Mixture Models earlier in this chapter and predict"),
    ("10", "Gaussian Mixture Models in Lecture 9 and predict", "Gaussian Mixture Models in [[ch:9]] and predict"),
    ("11", "The questions we ask today are", "The questions we ask in this chapter are"),
    ("12", "Today, we will re-examine the", "In this chapter, we will re-examine the"),
    ("12", "in our logistic model on the previous slide,", "in our logistic model above,"),
    ("12", "our logistic regression model in the previous slide was", "our logistic regression model above was"),
    ("12", " (think about when you were frustrated with the concept quizzes!)", ""),
    ("13", "other hard optimization problem we've seen in this class?", "other hard optimization problems we've seen in this book?"),
    ("14", "(see this weeks readings). Futhermore,", "(see the readings at the end of this chapter). Furthermore,"),
    # Exercise numbers in the problem set (the source skipped 9 and referred to its own earlier numbering).
    ("14", "In Exercise 2 and 3, we examined one source", "In Exercises 1 and 2, we examined one source"),
    ("14", "model you trained in Exercise 3.", "model you trained in Exercise 2."),
    ("14", "**Exercise 10: (Is OOD Detection", "**Exercise 9: (Is OOD Detection"),
    ("14", "application you identified in Exercise 1,", "application you identified in Exercise 7,"),
    ("15", "(see this weeks readings). Futhermore,", "(see the readings at the end of this chapter). Furthermore,"),
    ("17", "**See course project papers:**", "**Further reading:**"),
    ("17", "Today, instead, we will adopt", "In this chapter, we will instead adopt"),
    ("17", "Bayesian neural network in Exercise 1 with 1 hidden layer", "Bayesian neural network in Question 1 with 1 hidden layer"),
    ("17", "See Lecture #17 or the example code", "See the derivation earlier in this chapter or the example code"),
    ("17", "you implemented in Exercise 1 and 2,", "you implemented in Part I, Questions 1 and 2,"),
    ("19", "We've argued in this course that", "We've argued in this book that"),
    ("19", "**What this class is not:** This class is not", "**What this book is not:** This book is not"),
    ("19", "You don't remember everything from the class,", "You don't remember everything from the book,"),
    ("19", "**What is this class:** This class is a map", "**What this book is:** This book is a map"),
    ("19", "Using the structure of this class you can", "Using the structure of this book you can"),
    ("19", "This class is a foundation for you to build on, future classes in ML",
     "This book is a foundation for you to build on; future courses in ML"),
    ("20", "Earlier this semester, we studied models", "In [[ch:9]], we studied models"),
    ("20", "In Lectures #9 and #10, we concentrated on Gaussian Mixutre Models. But in Lecture #9, we introduced",
     "In [[ch:9]] and [[ch:10]], we concentrated on Gaussian Mixture Models. But in [[ch:9]], we also introduced"),
    ("20", "The deep generative model we will study today,", "The deep generative model we will study in this chapter,"),
    ("lab-01", "## Tools for the Course", "## Computing Tools"),
    ("lab-01", "In all computation in this course, we will be using", "In all computation in this book, we will be using"),
    ("lab-01", "The course website contains readings, cheatsheets and tutorials for mastering",
     "Many readings, cheatsheets and tutorials are available online for mastering"),
    ("lab-04", "Recall the mixture of two univariate Gaussian example in class where",
     "Recall the mixture of two univariate Gaussians example in [[ch:8]], where"),
    ("lab-06", "3. in the lecture notes for logistic regression, we showed", "3. In [[ch:12]], we showed"),
    ("lab-06", "from the many examples from lecture and homework that", "from the many examples in this book that"),
    ("lab-09", "In class, we've only considered examples of sequential data with continuous values. ", ""),
    ("lab-01", "the average score for the final examis:", "the average score for the final exam is:"),
    ("lab-03", "Monte Carlo Estimation of a Gener Integral", "Monte Carlo Estimation of a General Integral"),
    ("lab-06", "approximately 2,000 new borns in California", "approximately 2,000 newborns in California"),
    ("impact-1", "We've also see that for risk-adverse", "We've also seen that for risk-averse"),
    ("01", "risk-adverse domains", "risk-averse domains"),
    ("14", "risk-adverse applications. Be concrete", "risk-averse applications. Be concrete"),
    ("14", "(Is OOD Detection Enough for Risk Adverse Applications?)", "(Is OOD Detection Enough for Risk-Averse Applications?)"),
    ("14", "In the risk adverse real-life application", "In the risk-averse real-life application"),
    ("impact-5", "The Cloud is a Factory (Chapter 1 from Your Computer is on Fire, available through Hollis)",
     "The Cloud is a Factory (Chapter 1 of *Your Computer Is on Fire*, MIT Press, 2021)"),
]

# Exact-text fixes to code cells, applied like TEXT_FIXES.
CODE_FIXES = [
    ("lab-05", "#the default sampler for pymc3 is a type of MCMC sampler called No-U-turn HMC, \n"
     "#which we have not covered in class\n",
     "#the default sampler for pymc3 is the No-U-Turn Sampler (NUTS), a type of HMC\n"),
]

# Misspellings in the course text: word (lower case) -> correction. Applied to prose only (not to
# code, math, URLs or HTML) in the converted pages and in the worked solutions; a capitalized word
# keeps its capital.
TYPO_FIXES = {
    "acurately": "accurately", "afriad": "afraid", "aggregtaion": "aggregation", "aleotoric": "aleatoric",
    "althhough": "although", "antidiscrimnatory": "antidiscriminatory", "artifcial": "artificial",
    "artisenal": "artisanal", "asympotically": "asymptotically", "asymptoptically": "asymptotically",
    "baesed": "based", "bayeisan": "Bayesian", "baye's": "Bayes'", "becaues": "because", "benifits": "benefits",
    "berstein": "Bernstein", "beter": "better", "binomal": "binomial", "bith": "birth", "boostrap": "bootstrap",
    "bootstraping": "bootstrapping", "centeral": "central", "certaint": "certain", "chekcks": "checks",
    "choise": "choice", "chunch": "chunk", "comparision": "comparison", "compliancenb": "compliance",
    "consdiered": "considered", "contrained": "constrained", "convient": "convenient",
    "correpsonding": "corresponding", "corrlated": "correlated", "covaraiates": "covariates", "cruicial": "crucial",
    "defintions": "definitions", "demogaphics": "demographics", "dervied": "derived", "descreases": "decreases",
    "differen": "different", "differentiaition": "differentiation", "dirichelet": "Dirichlet",
    "disasterous": "disastrous", "disparaties": "disparities", "dissimlar": "dissimilar", "dissmilar": "dissimilar",
    "distirbution": "distribution", "distribtutions": "distributions", "distribuion": "distribution",
    "doens't": "doesn't", "dynmaics": "dynamics", "ecnode": "encode", "elemtary": "elementary",
    "ellipitical": "elliptical", "emprical": "empirical", "emprirical": "empirical", "emprirically": "empirically",
    "epstemic": "epistemic", "espected": "expected", "estimatation": "estimation", "estimte": "estimate",
    "estmiate": "estimate", "euclidea": "Euclidean", "exepectation": "expectation",
    "exprimentally": "experimentally", "follwing": "following", "frequnetist": "frequentist", "gardient": "gradient",
    "gaurantee": "guarantee", "guaratee": "guarantee", "gendery": "gender", "geomtrically": "geometrically",
    "guassian": "Gaussian", "hamiltonia": "Hamiltonian", "hiearchical": "hierarchical", "hierachical": "hierarchical",
    "hiearchy": "hierarchy", "highligthed": "highlighted", "hypothese": "hypotheses",
    "implemenation": "implementation", "importnce": "importance", "impplementing": "implementing",
    "incoporating": "incorporating", "increasinglly": "increasingly", "infered": "inferred",
    "inferenec": "inference", "infering": "inferring", "influency": "influence", "instaneous": "instantaneous",
    "intellegence": "intelligence", "interated": "iterated", "interchageably": "interchangeably",
    "intial": "initial", "intialization": "initialization", "intialize": "initialize", "intitial": "initial",
    "intitialize": "initialize", "justic": "justice", "landsacapes": "landscapes", "langrangian": "Lagrangian",
    "leanring": "learning", "liklelihood": "likelihood", "liklihood": "likelihood", "maximimizing": "maximizing",
    "maximimum": "maximum", "maximium": "maximum", "mayb": "may", "meand": "means", "mixutre": "mixture",
    "movment": "movement", "neccessarily": "necessarily", "necssarily": "necessarily", "nerual": "neural",
    "netoworks": "networks", "nontheless": "nonetheless", "ouput": "output", "outputed": "output",
    "paramters": "parameters", "parial": "partial", "percieved": "perceived", "ploting": "plotting",
    "poential": "potential", "poseterior": "posterior", "posteior": "posterior", "possibile": "possible",
    "potenial": "potential", "practics": "practices", "practiioners": "practitioners", "preceeding": "preceding",
    "predcitive": "predictive", "prective": "predictive", "predictve": "predictive", "predictves": "predictives",
    "probabilites": "probabilities", "probabiliy": "probability", "problemmatic": "problematic",
    "proceedure": "procedure", "prodcues": "produces", "programmming": "programming",
    "questionaire": "questionnaire", "quicklly": "quickly", "randomn": "random", "randomnly": "randomly",
    "redudant": "redundant", "regulartory": "regulatory", "repect": "respect", "resurces": "resources",
    "secretely": "secretly", "sensitve": "sensitive", "seting": "setting", "shoud": "should", "simliar": "similar",
    "simplyfying": "simplifying", "sinusoical": "sinusoidal", "stinchombe": "Stinchcombe",
    "stochastoic": "stochastic", "subcomunities": "subcommunities", "subtlties": "subtleties",
    "suceeding": "succeeding", "sufficintly": "sufficiently", "supoose": "suppose", "sympletic": "symplectic",
    "synethic": "synthetic", "synethtic": "synthetic", "tasts": "tasks", "theorm": "theorem",
    "thinnning": "thinning", "througbh": "through", "trignometric": "trigonometric",
    "uncertatinty": "uncertainty", "uncertianty": "uncertainty", "vaue": "value", "varaitional": "variational",
    "varational": "variational", "varibles": "variables", "visualizaion": "visualization",
    "visualiztaion": "visualization", "vunerable": "vulnerable", "weigths": "weights",
}
