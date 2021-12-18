import pandas
import sample


class Data:
    def __init__(self, path):
        self.path = path
        df = pandas.read_csv(path)
        self.data = df.to_dict(orient="list")

    def create_samples(self):
        """
        Create the sample list. Every sample will receive its label, sample ID, and genes.
        :return:List of samples each containing its attributes.
        """
        gene_list = []
        data_list = []
        for i in range(len(self.data["samples"])):
            sample_id = self.data["samples"][i]
            label = self.data["type"][i]
            for j, gene in enumerate(self.data.keys()):
                if j < 2:
                    continue
                gene_list.append(float(self.data[gene][i]))
            data_list.append(sample.Sample(sample_id, gene_list, label))
            gene_list = []
        return data_list
