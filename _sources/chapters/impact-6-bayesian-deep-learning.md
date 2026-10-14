# Applications and Broader Impact: Bayesian Deep Learning

:::{admonition} Draft chapter
:class: warning
This chapter collects the broader-impact discussion and readings that accompanied Part VI in AM207 (Harvard, Fall 2021). It will be expanded into a full chapter.
:::

## Interpretable Deep Learning
We might be tempted to conclude that neural networks are uninterpretable due to their complexity. But just because we can't understand neural networks by inspecting the value of the individual weights, it does not mean that we can't understand them.

In [The Mythos of Model Interpretability](https://arxiv.org/abs/1606.03490), the authors survey a large number of methods for interpreting deep models. 


```{figure} ../figures/cnnviz.jpg
:name: fig-impact-cnnviz
:width: 100%
:align: center
```

## Can Machine Learning Models Make Use of Human Concepts?
***(with Anita Mahinpei, Justin Clark, Ike Lage, Finale Doshi-Velez)***

What if instead building complex non-linear models based on raw inputs, we instead build simple linear models based on human interpretable **concepts**? We use a neural network to predict concepts from inputs and then use a linear model to predict the outcome from the concepts. We interpret the relationship between the outcome and the concepts via the linear model. These models are called **concept bottleneck models**.

In [The Promises and Pitfalls of Black-box Concept Learning Models](https://arxiv.org/abs/2106.13314), we examine the advantages and drawbacks of these models.


```{figure} ../figures/slide15.png
:name: fig-impact-slide15
:width: 583px
:align: center
```

## Can Machine Learning Models Learn to Explore Hypothetical Scenarios?
***(with Michael Downs, Jonathan Chu, Wisoo Song, Yaniv Yacoby, Finale Doshi-Velez)***

Rather than explaining why the model made a decision, it's often more helpful to explain how to change the data in order to change the model's decision. This modified input is a **counter-factual**. In [CRUDS: Counterfactual Recourse Using Disentangled Subspaces](https://finale.seas.harvard.edu/files/finale/files/cruds-_counterfactual_recourse_using_disentangled_subspaces.pdf), we study how to automatically generate counter-factual explanations that can help users achieve a favorable outcome from a decision system.


```{figure} ../figures/slide16.png
:name: fig-impact-slide16
:width: 496px
:align: center
```

## Right for the Right Reasons?
In *An explainable deep-learning algorithm for the detection of acute intracranial haemorrhage from small datasets*, the authors build a neural network model to detect acute intracranial haemorrhage (ICH) and classifies five ICH subtypes. 

Model classifications are explained by highlighting the pixels that contributed the most to the decision. The highlighted regions tends to overlapped with ‘bleeding points’ annotated by neuroradiologists on the images.


```{figure} ../figures/shap.png
:name: fig-impact-shap
:width: 724px
:align: center
```

## The Perils of Explanations
In *How machine-learning recommendations influence clinician treatment selections: the example of antidepressant selection*, the authors found that clinicians interacting with incorrect recommendations paired with simple explanations experienced significant reduction in treatment selection accuracy.


```{figure} ../figures/reliance.png
:name: fig-impact-reliance
:width: 412px
:align: center
```



**Take-away:** Incorrect ML recommendations may adversely impact clinician treatment selections and that explanations are insufficient for addressing overreliance on imperfect ML algorithms.

## Readings

**Applications and Broader Impact**

- [The Mythos of Model Interpretability](https://arxiv.org/pdf/1606.03490.pdf)
- [Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead](https://arxiv.org/pdf/1811.10154.pdf)
- [Risk versus Uncertainty in Deep Learning: Bayes, Bootstrap and the Dangers of Dropout](http://bayesiandeeplearning.org/2016/papers/BDL_4.pdf)
- [It’s Too Easy to Hide Bias in Deep-Learning Systems  Artificial intelligence makes it hard to tell when decision-making is biased](https://spectrum.ieee.org/its-too-easy-to-hide-bias-in-deeplearning-systems)
- [The security threat of adversarial machine learning is real](https://bdtechtalks.com/2020/10/26/adversarial-machine-learning-threat-matrix/)
- [Would you trust a machine to pick a vaccine?](https://review.chicagobooth.edu/economics/2020/article/would-you-trust-machine-pick-vaccine)
- [Remember the ‘deepfake cheerleader mom’? Prosecutors now admit they can’t prove fake-video claims.](https://www.washingtonpost.com/technology/2021/05/14/deepfake-cheer-mom-claims-dropped/)
- [Fighting deepfakes when detection fails](https://www.brookings.edu/research/fighting-deepfakes-when-detection-fails/)
- [Using Generative AI to Accelerate Drug Discovery](https://www.ibm.com/blogs/research/2020/06/accelerated-discovery/)
- [Positive Use Cases of Deepfakes](https://towardsdatascience.com/positive-use-cases-of-deepfakes-49f510056387)
