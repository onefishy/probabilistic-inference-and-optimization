# Applications and Broader Impact: Foundations of Inference

:::{admonition} Draft chapter
:class: warning
This chapter collects the broader-impact discussion and readings that accompanied Part I in AM207 (Harvard, Fall 2021). It will be expanded into a full chapter.
:::

## Broader Impact
From the {ref}`Chapter 1 problem set <ps-hw0>` you've already seen that model evaluation is far more than just computing the MSE or, indeed, any metric. Interpreting the model in the domain application is equally important:

1. "Gut checking" the clinical meaning of the slope and y-intercept of a linear model can tell us if the model is appropriate.

  - Why is it hard to "gut check" model for the dataset in the {ref}`Chapter 1 problem set <ps-hw0>`. What does this say about our typical ML model building pipeline?<br><br>
  
  - What if the model is not easy to interpret by looking at the parameters themselves? How do we know that our interpretations of models are accurate and objective? What is an "accurate" interpretation of a model anyways? Can models be "objectively" interpreted? (*Reading:  Towards A Rigorous Science of Interpretable Machine Learning*)<br><br>
  
  - What if the data has been preprocessed like in the {ref}`Chapter 1 problem set <ps-hw0>`? What does this say about ML development pipelines where the ML experts are removed from the data cleaning, preprocessing step?
  
2. We've also seen that for risk-averse applications it's crucial to get predictive uncertainty from our models.

  - Why is predictive uncertainty useful? 
  - What is predictive uncertainty useful for?
  - Under what real-life conditions would we need predictive uncertainty?
  
  *(Reading: Second opinion needed: communicating uncertainty in medical machine learning, Uncertainty as a Form of Transparency: Measuring, Communicating, and Using Uncertainty)*

## Readings

**Promises of Machine Learning**

- (Introductory) [From Diagnosis to Holistic Patient Care, Machine Learning is Transforming Healthcare](https://www.wired.com/wiredinsider/2019/10/from-diagnosis-to-holistic-patient-care-machine-learning-is-transforming-healthcare/)
- (Introductory) [The future of agriculture is computerized](https://news.mit.edu/2019/algorithm-growing-agriculture-0403)
- (In-Depth) [Tackling Climate Change with Machine Learning](https://arxiv.org/pdf/1906.05433.pdf)
- (In-Depth) [Machine Learning for the Developing World](https://www.ri.cmu.edu/wp-content/uploads/2020/05/3210548.pdf)
- (In-Depth) [AI for social good: unlocking the opportunity for positive impact](https://www.nature.com/articles/s41467-020-15871-z)

**Potential Dangers of Machine Learning**

- (Introductory) [Predictive policing algorithms are racist. They need to be dismantled.](https://www.technologyreview.com/2020/07/17/1005396/predictive-policing-algorithms-racist-dismantled-machine-learning-bias-criminal-justice/)
- (Introductory) [When Good Algorithms Go Sexist: Why and How to Advance AI Gender Equity](https://ssir.org/articles/entry/when_good_algorithms_go_sexist_why_and_how_to_advance_ai_gender_equity)
- (Introductory) [Millions of black people affected by racial bias in health-care algorithms](https://www.nature.com/articles/d41586-019-03228-6)
- (Introductory) [Medicine's Machine Learning Problem](https://bostonreview.net/science-nature/rachel-thomas-medicines-machine-learning-problem)
- (Introductory) [Algorithms Are Making Economic Inequality Worse](https://hbr.org/2020/10/algorithms-are-making-economic-inequality-worse)
- (Introductory) [AI needs to face up to its invisible-worker problem](https://www.technologyreview.com/2020/12/11/1014081/ai-machine-learning-crowd-gig-worker-problem-amazon-mechanical-turk/)
- (In-Depth) [A case study of algorithm-assisted decision making in child maltreatment hotline screening decisions](https://proceedings.mlr.press/v81/chouldechova18a/chouldechova18a.pdf)

**Machine Learning and Ethics**

- (Introductory) [Artificial Intelligence in Health: Ethical Considerations for Research and Practice](https://www.himss.org/resources/artificial-intelligence-health-ethical-considerations-research-and-practice)
- (In-Depth) [Ethical principles in machine learning and artificial intelligence: cases from the field and possible ways forward](https://www.nature.com/articles/s41599-020-0501-9)
- (In-Depth) [Data Science as Political Action: Grounding Data Science in a Politics of Justice](https://arxiv.org/pdf/1811.03435.pdf)

**Applications and Broader Impact**

- (Introductory) [Second opinion needed: communicating uncertainty in medical machine learning](https://www.nature.com/articles/s41746-020-00367-3)
- (Introductory) [Uncertainty as a Form of Transparency: Measuring, Communicating, and Using Uncertainty](https://arxiv.org/pdf/2011.07586.pdf)
- (Introductory) [Interpretability (Chapter 2 of Interpretable Machine Learning: A Guide for Making Black Box Models Explainable)](https://christophm.github.io/interpretable-ml-book/interpretability.html)
- (In-Depth) [Towards A Rigorous Science of Interpretable Machine Learning](https://arxiv.org/pdf/1702.08608.pdf)
- [Bayesian Modeling of Uncertainty in Ensembles of Climate Models](https://www.jstor.org/stable/40591903?seq=1#metadata_info_tab_contents)
- [All together now: the most trustworthy covid-19 model is an ensemble](https://www.technologyreview.com/2021/05/28/1025478/covid-ensemble-model-forecast-trustworthy/)
