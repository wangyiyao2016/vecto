import os
import pandas
from pandas.io.json import json_normalize
from matplotlib import pyplot as plt
from vecto.utils.data import load_json


def df_from_file(path):
    data = load_json(path)
    meta = [["experiment_setup", "subcategory"], ["experiment_setup", "method"], ["experiment_setup", "embeddings"]]
    dframe = json_normalize(data, meta=meta)
    # df["reciprocal_rank"] = 1 / (df["rank"] + 1)
    return dframe


def df_from_dir(path):
    dfs = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            dfs.append(df_from_file(os.path.join(dirpath, filename)))
    dframe = pandas.concat(dfs)
    return dframe


def plot_accuracy(path="tests/data/benchmarks_results/analogy/",
                  group_xaxis=['experiment_setup.embeddings.foldername',
                               'experiment_setup.method'][0]):
    df = df_from_dir(path)
    group = df.groupby(["experiment_setup.subcategory", group_xaxis])
    means = group.mean()
    means.reset_index(inplace=True)
    means = means.loc[:, ["experiment_setup.subcategory", group_xaxis, "result"]]
    unstacked = means.groupby(['experiment_setup.subcategory', group_xaxis])['result'].aggregate(
        'first').unstack()
    unstacked.plot(kind="bar")
    # plt.show()


# def run_results(path_embeds=["tests/data/embeddings/text/plain_with_file_header",
#                                "tests/data/embeddings/text/plain_no_file_header", ],
#                   path_analogy_dataset="./tests/data/benchmarks/analogy/",
#                   methods=[LRCos, LinearOffset]):
#     for method in methods:
#         for path_embed in path_embeds:
#             embs = load_from_dir(path_embed)
#             analogy = method()
#             results = analogy.run(embs, path_analogy_dataset)
#             print(results)
#             save_json(results, os.path.join("/tmp/tests/data/benchmarks_results/analogy/", datetime.datetime.now().isoformat()))


def main():
    plot_accuracy()


if __name__ == "__main__":
    main()
