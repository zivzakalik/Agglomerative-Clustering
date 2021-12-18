import cluster


class AgglomerativeClustering:
    def __init__(self, link, samples):
        """
        Create the instance. Added a distance matrix to calculate sample distances faster.
        :param link:Link type to calculate distance of clusters.
        :param samples:Samples used in the algorithm.
        """
        self.samples = samples
        self.link = link
        self.clusters = []
        self.distance_matrix = [[0] * (samples[-1].s_id + 1) for _ in range(samples[-1].s_id + 1)]
        for sample in samples:
            self.clusters.append(cluster.Cluster(sample.s_id, [sample]))
        self.create_distance_matrix(samples)

    def create_distance_matrix(self, samples):
        """
        Create the distance matrix. Used in the init builder.
        :param samples:Samples the classifier will work with.
        :return:Lower triangular matrix of distances between every pair of samples.
        The row and column are the sample pair IDs.
        """
        for sample1 in samples:
            for sample2 in samples:
                if sample2.s_id > sample1.s_id:
                    continue
                self.distance_matrix[sample1.s_id][sample2.s_id] = sample1.compute_euclidean_distance(
                    sample2)

    def compute_silhoeutte(self):
        """
        Calculate the silhoeutte of every sample in the data set.
        :return:A dictionary. Keys: sample ID, Values: sample silhoeutte.
        """
        my_dict = {}
        for sample in self.samples:
            my_in_sum = 0
            my_out_list = []
            for my_cluster in self.clusters:
                if sample in my_cluster.samples:
                    if len(my_cluster.samples) - 1 > 0:
                        my_in_sum = my_cluster.calc_dist(sample, self.distance_matrix) / \
                                (len(my_cluster.samples) - 1)
                else:
                    my_out_list.append(my_cluster.calc_dist(sample, self.distance_matrix) / len(my_cluster.samples))
            my_dict[sample.s_id] = (min(my_out_list) - my_in_sum) / max(my_in_sum, min(my_out_list))
            my_dict[sample.s_id] = 0 if my_dict[sample.s_id] == 1 else my_dict[sample.s_id]
        return my_dict

    def compute_summery_silhoeutte(self):
        """
        First calculate silhoeutte of data set, and set it in the dictionary in key 0.
        Then calculate silhoeutte of each cluster.
        :return:dictionary. Keys: cluster ID, Values: cluster silhoeutte.
        """
        my_dict = self.compute_silhoeutte()
        return_dict = {}
        my_sum = 0
        for value in my_dict.values():
            my_sum += value
        return_dict[0] = my_sum / len(my_dict.keys())
        for my_cluster in self.clusters:
            my_sum = 0
            for sample in my_cluster.s_id_list:
                my_sum += my_dict[sample]
            return_dict[my_cluster.c_id] = my_sum / len(my_cluster.s_id_list)
        return return_dict

    def compute_rand_index(self):
        """
        Calculate Rand Index value of data set, after classification of clusters.
        :return:RI value, as a float.
        """
        my_matrix = []
        label_list = []
        tp = 0
        tn = 0
        """
        Create label set, out of label list.
        Then create an empty matrix using length of label set.
        """
        for my_sample in self.samples:
            label_list.append(my_sample.label)
        label_set = set(label_list)
        for i in range(len(label_set)):
            my_matrix.append([])
        """
        For every label, Calculate a confusion matrix and using that calculate TP and TN.
        TP = sum of every C = coordinate in matrix, sum of all C*(C-1)/2 
        
        for every C = coordinate in matrix, 
        D = sum of all the coordinates in matrix not in the same row of column as C.
        TN = sum of D*C, For all C in matrix.
        """
        for i, label in enumerate(label_set):
            for curr_cluster in self.clusters:
                sum_all = 0
                for curr_sample in curr_cluster.samples:
                    if curr_sample.label == label:
                        sum_all += 1
                my_matrix[i].append(sum_all)
        for label in range(len(label_set)):
            for my_cluster in range(len(label_set)):
                tp += (my_matrix[label][my_cluster] * (my_matrix[label][my_cluster] - 1)) / 2
                tn_temp = 0
                for i in range(len(label_set)):
                    for j in range(len(label_set)):
                        if i != label and j != my_cluster:
                            tn_temp += my_matrix[i][j]
                tn += tn_temp * my_matrix[label][my_cluster]
                my_matrix[label][my_cluster] = 0

        return round((tp + tn) / (len(self.samples) * (len(self.samples) - 1) / 2), 3)

    def run(self, max_clusters):
        """
        Run the classifier.
        :param max_clusters: Number of minimum clusters allowed.
        While the cluster is still not at the minimum allowed, continue merging.
        """
        while len(self.clusters) > max_clusters:
            """
            Create a dictionary.
            Keys: distance of clusters. Values:the two clusters that generated the distance.
            """
            full_dist_dict = {}
            for cluster1 in self.clusters:
                dist_dict = {}
                min_dist = 0
                for cluster2 in self.clusters:
                    if cluster1.c_id == cluster2.c_id:
                        continue
                    curr_dist = self.link.compute(cluster1, cluster2, self.distance_matrix)
                    dist_dict[curr_dist] = cluster2
                    if curr_dist < min_dist or min_dist == 0:
                        min_dist = curr_dist
                full_dist_dict[min_dist] = [cluster1, dist_dict[min_dist]]
            full_min = min(full_dist_dict.keys())
            if full_dist_dict[full_min][0].c_id > full_dist_dict[full_min][1].c_id:
                temp = full_dist_dict[full_min][1]
            else:
                temp = full_dist_dict[full_min][0]
            """
            Find the two clusters with the minimal distance, and merge them.
            Removes the the cluster with the higher ID between the two.
            Sort the rest of the clusters.
            """
            full_dist_dict[full_min][0].merge(full_dist_dict[full_min][1])
            self.clusters.remove(temp)
            self.clusters.sort(key=lambda cluster3: cluster3.c_id)