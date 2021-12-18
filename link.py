class Link:
    def compute(self, cluster, other, size_matrix):
        raise NotImplementedError("Subclass must implement abstract method")


class SingleLink(Link):
    """
    Compute the size between the clusters, using the distance matrix and Single link methode.
    since the matrix we created is a lower triangular matrix, check if the row is bigger then column.
    """
    def compute(self, cluster, other, size_matrix):
        temp_list = []
        for c_s_id in cluster.s_id_list:
            for o_s_id in other.s_id_list:
                if c_s_id > o_s_id:
                    temp_list.append(size_matrix[c_s_id][o_s_id])
                else:
                    temp_list.append(size_matrix[o_s_id][c_s_id])
        return min(temp_list)


class CompleteLink(Link):
    """
    Compute the size between the clusters, using the distance matrix and Complete link methode.
    since the matrix we created is a lower triangular matrix, check if the row is bigger then column.
    """
    def compute(self, cluster, other, size_matrix):
        temp_list = []
        for c_s_id in cluster.s_id_list:
            for o_s_id in other.s_id_list:
                if c_s_id > o_s_id:
                    temp_list.append(size_matrix[c_s_id][o_s_id])
                else:
                    temp_list.append(size_matrix[o_s_id][c_s_id])
        return max(temp_list)
