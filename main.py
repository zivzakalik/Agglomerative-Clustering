import sys
import data
import agglomerative_clustering
import link


def main(argv):
    """
    Create Data from csv
    Turn data into list of samples
    Create link objects and the agglomerative clustering objects.
    """
    my_data = data.Data(argv[1])
    sample_list = my_data.create_samples()
    single_link = link.SingleLink()
    complete_link = link.CompleteLink()
    agc = agglomerative_clustering.AgglomerativeClustering(single_link, sample_list)
    agc2 = agglomerative_clustering.AgglomerativeClustering(complete_link, sample_list)
    """
    Run the agglomerative clustering objects, and create silhoeutte dictioneries and RI values.
    """
    agc.run(7)
    agc2.run(7)
    silhoeutte_dict = agc.compute_summery_silhoeutte()
    silhoeutte_dict2 = agc2.compute_summery_silhoeutte()
    ri1 = agc.compute_rand_index()
    ri2 = agc2.compute_rand_index()
    """
    Prints according to demands.
    """
    print("single link:")
    for cluster in agc.clusters:
        print("Cluster " + str(cluster.c_id) + ": " + str(cluster.s_id_list) + ", dominant label = "
              + cluster.calc_my_label() + ", silhouette = " + str(round(silhoeutte_dict[cluster.c_id], 3)))
    print("Whole data: silhouette = " + str(round(silhoeutte_dict[0], 3)) + ", RI = " + str(ri1))
    print("\ncomplete link:")
    for cluster in agc2.clusters:
        print("Cluster " + str(cluster.c_id) + ": " + str(cluster.s_id_list) + ", dominant label = "
              + cluster.calc_my_label() + ", silhouette = " + str(round(silhoeutte_dict2[cluster.c_id], 3)))
    print("Whole data: silhouette = " + str(round(silhoeutte_dict2[0], 3)) + ", RI = " + str(ri2))


if __name__ == '__main__':
    main(sys.argv)
