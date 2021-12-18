class Cluster:
    """
    Added s_id attribute - which is a list of ints of the sample IDs the cluster contains.
    """
    def __init__(self, c_id, samples):
        self.c_id = c_id
        self.samples = samples
        self.s_id_list = []
        for sample in samples:
            self.s_id_list.append(sample.s_id)
        sorted(self.s_id_list)
    """
    Merges clusters and sort the sample list, and the s_id list.
    """
    def merge(self, other):
        for sample1 in other.samples:
            self.samples.append(sample1)
            self.s_id_list.append(sample1.s_id)
        self.c_id = self.c_id if self.c_id < other.c_id else other.c_id
        self.samples.sort(key=lambda sample1: sample1.s_id)
        self.s_id_list.sort()
    """
    Print cluster details. The samples it contains and most common label.
    """
    def print_details(self, silhouette):
        label_list = []
        print(self.s_id_list)
        for sample in self.samples:
            label_list.append(sample.label)
        print(max(label_list, key=label_list.count()))
        print(silhouette)
    """
    Receives a sample, and returns the combined sum of distance from the sample to all the samples
    in this cluster.
    """
    def calc_dist(self, sample, distance_matrix):
        my_sum = 0
        for col in self.s_id_list:
            if col > sample.s_id:
                my_sum += distance_matrix[col][sample.s_id]
            else:
                my_sum += distance_matrix[sample.s_id][col]
        return my_sum
    """
    Find most common label.
    """
    def calc_my_label(self):
        label_list = []
        for sample in self.samples:
            label_list.append(sample.label)
        return max(set(label_list), key=label_list.count)
