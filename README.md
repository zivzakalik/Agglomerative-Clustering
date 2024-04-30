# Agglomerative Clustering

## Distance Measurement

We employ the Euclidean distance to determine which clusters should be merged. This metric helps in assessing the proximity between different clusters effectively.

## Algorithm Quality

The performance of our clustering algorithm is evaluated based on its purity. This metric helps in determining the accuracy with which the algorithm groups samples into the correct clusters.

## Algorithm Overview

### Purpose

The algorithm aims to cluster samples based on their features to identify specific types of cancer accurately.

### Stopping Criterion

The clustering process is halted once the number of clusters reaches seven. This stop condition ensures that the clusters remain meaningful and manageable.

### Methods Employed

We utilize two variants of agglomerative clustering:
- **Single Link**: This method considers the minimum distance between clusters for merging decisions.
- **Complete Link**: In contrast, this method considers the maximum distance between clusters to guide the merging process.

## Implementation Classes

1. **Cluster**: Represents a single cluster containing grouped samples.
2. **Data**: This class is responsible for organizing the data and computing the initial distance matrix, essential for the clustering process.
3. **Link**: This superclass contains three subclasses:
   - **Link**: The base class for linkage criteria.
   - **SingleLink**: Implements the single link clustering method.
   - **CompleteLink**: Implements the complete link clustering method.
4. **AgglomerativeClustering**: This class updates the clusters and oversees the execution of the algorithm, ensuring that the clustering process adheres to the specified methods and stopping criteria.
