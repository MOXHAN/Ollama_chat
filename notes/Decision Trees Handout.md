---
tags:
  - DataScience
  - MachineLearning
---
## Basics

### Basic Idea
- Decision trees are used to find explicit knowledge and provide explanations for their decisions, contrasting with methods like k-Nearest Neighbors (kNN), which lack explanatory power.

### Rooted Trees
- **Definition**: A tree is a graph that is connected and acyclic.
- **Rooted Tree**: A graph with one designated root node, all edges point away from the root.

### Further Notions
- **Level**: Number of steps from the root.
- **Width**: Number of nodes on a level.
- **Depth**: Highest level.
- **Breadth**: Number of leaf nodes.

### Decision Trees Basics
- **Structure**: Binary rooted trees where each inner node represents a test/question on one feature, and each leaf represents a decision for a class.
- **Classification**: Follow the tree from the root to a leaf to predict the class of a data instance.

## Construction

### Algorithm
1. Create a root node with the full training dataset.
2. Select a split based on a split strategy (categorical or continuous features).
3. Partition the data and create child nodes.
4. Repeat steps 2 and 3 recursively until stopping criteria are met.

### Example
- An example with the Iris dataset is provided, demonstrating how a decision tree can be constructed based on petal length and width.

### Split Types
- **Categorical Features**: Splits based on feature values or subsets.
- **Numerical Features**: Splits based on thresholds (e.g., feature < threshold).

### Measuring Split Quality
- **Misclassification Error**: Probability of error if the node votes for its most frequent class.
- **Information Gain**: Reduction in entropy after a split.
- **Gini Coefficient**: Measures the expected risk of misclassification, with lower values indicating more pure splits.

### Example – Tennis Dataset
- An example comparing splits by humidity and wind in a tennis dataset is used to illustrate split strategies.

## Overfitting

### Problem
- Overfitting occurs when a decision tree is too complex, capturing noise in the training data and performing poorly on new, unseen data.

### Avoiding Overfitting
- **During Construction**: Use minimum support, minimum information gain, and minimum confidence to stop splitting early.
- **Pruning**: Techniques like error-reduction pruning and minimal cost-complexity pruning help reduce overfitting by removing parts of the tree that do not generalize well.

## Decision Trees in Python

### Implementation
- **Library**: `sklearn.tree.DecisionTreeClassifier` supports decision tree construction with numerical attributes.
- **Graphical Output**: Visualization of decision trees using `graphviz`.

## Additional Topics and Questions
- **Hyperparameter Tuning**: Explore how different hyperparameters affect decision tree performance.
- **Feature Importance**: Investigate which features are most important in decision tree construction.
- **Comparison with Other Algorithms**: Compare decision trees with other machine learning algorithms like random forests and gradient boosting.
- **Real-world Applications**: Discuss the application of decision trees in various domains 
- such as healthcare, finance, and marketing.