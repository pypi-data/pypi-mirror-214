"""Find articles similar to a given text file
"""
import argparse
import os
import pickle
import sys
from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pymongo
from pymongo import MongoClient
from scipy import stats
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from monito_tools import (
    console,
    general_config,
    init_mongodb,
    init_nlp,
    load_general_config,
    log,
    logging_set_up,
    preprocess,
    print_logo,
    set_log_level,
)

N_DEBUG_ARTICLES = 300


# our labeling
LABELS: List[str] = [
    "UNLABELED",
    "politics",
    "local",
    "health",
    "news",
    "sports",
    "security",
    "science",
    "technology",
    "environment",
    "entertainment",
    "economics",
    "local",
    "cdmx",
    "euo",
    "ambiente",
    "culture",
]

# spanish categories provided by websites -> our labels
LABEL_LOOKUP: Dict[str, str] = {
    "UNLABELED": "UNLABELED",
    "policiacar": "politics",
    "consejo": "politics",
    "gobierno": "politics",
    "migracion": "politics",
    "justicia": "politics",
    "morelia": "local",
    "deporte": "sports",
    "mazatlan": "local",
    "salud": "health",
    "seguridad": "security",
    "show": "entertainment",
    "entretenimiento": "entertainment",
    "espectaculo": "entertainment",
    "bolsillo": "entertainment",
    "rojo": "entertainment",
    "cultura": "culture",
    "sociedad": "culture",
    "postura": "culture",
    "politico": "politics",
    "noticia": "news",
    "michoacan": "local",
    "destacado": "news",
    "vandalismo": "news",
    "ciencia": "science",
    "viral": "news",
    "astronomia": "science",
    "tecnologia": "technology",
    "principal": "news",
    "ambiente": "environment",
    "hardnews": "news",
    "mexico": "local",
    "patzcuaro": "local",
    "cdmx": "cdmx",
    "euo": "euo",
    "economia": "economics",
    "zitacuarir": "local",
    "palencia": "local",
    "local": "local",
    "estatal": "local",
    "hora": "news",
    "suceso": "news",
    "mundo": "news",
    "guadalajara": "local",
}


def vae_pipeline(X_train: np.ndarray, Y_train: np.ndarray, X_test: np.ndarray, Y_test: np.ndarray, n_dims=3):
    import torch
    from torch import nn
    from torch.optim import Adam
    from torch.utils.data import DataLoader, TensorDataset

    # Define the Variational Autoencoder
    class VAE(nn.Module):
        def __init__(self, input_shape: int, n_labels: int):
            super(VAE, self).__init__()
            self.encoder = nn.Sequential(nn.Linear(input_shape, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU())

            self.mu = nn.Linear(64, n_dims)
            self.log_var = nn.Linear(64, n_dims)

            self.decoder = nn.Sequential(
                nn.Linear(n_dims, 32),
                nn.ReLU(),
                nn.Linear(32, 32),
                nn.ReLU(),
                nn.Linear(32, n_labels),
                nn.Softmax(dim=1),
            )

        def encode(self, x):
            h = self.encoder(x)
            mu = self.mu(h)
            log_var = self.log_var(h)
            # reparameterize
            std = torch.exp(log_var / 2)
            eps = torch.randn_like(std)
            z = mu + eps * std
            return z, mu, log_var

        def decode(self, z):
            return self.decoder(z)

        def forward(self, x):
            z, mu, log_var = self.encode(x)
            predictions = self.decode(z)
            return predictions, mu, log_var

    # Convert your data to PyTorch tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    # Y_train_tensor = torch.tensor(Y_train, dtype=torch.float32)
    Y_train_tensor = torch.tensor(np.argmax(Y_train, axis=1), dtype=torch.long)

    # Create a DataLoader
    train_dataset = TensorDataset(X_train_tensor, Y_train_tensor)
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # Create the autoencoder, the optimizer and the loss function
    model = VAE(input_shape=X_train_tensor.shape[1], n_labels=len(LABELS))
    optimizer = Adam(model.parameters(), lr=1e-3)

    def loss_fn(predictions, labels, mu, log_var, gamma=1.0):
        CE = nn.functional.cross_entropy(predictions, labels, reduction="sum")
        KLD = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
        return CE + gamma * KLD

    # Train the autoencoder
    epochs = 20
    print(f"Training an AutoEncoder for {epochs} epochs")

    gamma = 1e-10
    for epoch in range(epochs):
        total_loss = 0
        correct_predictions = 0
        total_predictions = 0
        for batch in train_dataloader:
            x, y = batch
            optimizer.zero_grad()
            y_pred, mu, log_var = model(x)
            loss = loss_fn(y_pred, y, mu, log_var, gamma=gamma)
            loss.backward()
            optimizer.step()

            # Calculate accuracy
            _, predicted = torch.max(y_pred.data, 1)
            total_predictions += y.size(0)
            correct_predictions += (predicted == y).sum().item()

            total_loss += loss.item()

        gamma *= 10.0
        accuracy = correct_predictions / total_predictions * 100
        print(f"Epoch: {epoch}, Loss: {total_loss / total_predictions}, Accuracy: {accuracy}%")

    # to visualize z of train set
    representations_train = model.encode(X_train_tensor)[0].detach().numpy()

    # ------ run inference on test data ------

    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    Y_test_tensor = torch.tensor(np.argmax(Y_test, axis=1), dtype=torch.long)

    representations_test = model.encode(X_test_tensor)[0].detach().numpy()
    predictions_test = model(X_test_tensor)[0].detach().numpy()

    test_dataset = TensorDataset(X_test_tensor, Y_test_tensor)
    test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=True)

    # predict on test data
    test_correct_predictions = 0
    test_total_predictions = 0
    for batch in test_dataloader:
        x, y = batch
        y_pred, mu, log_var = model(x)

        _, predicted = torch.max(y_pred.data, 1)
        test_correct_predictions += (predicted == y).sum().item()
        test_total_predictions += y.size(0)

    test_accuracy = test_correct_predictions / test_total_predictions * 100
    print(f"Test accuracy: {test_accuracy:.3f}%")

    return representations_train, representations_test, predictions_test


def reduce_dimensionality(
    X,  # array of shape N x D
    method="svd",
    n_dims=3,
):
    assert method in ["svd", "pca", "ae", "vae"]
    if method == "svd":
        svd = TruncatedSVD(n_components=n_dims)
        X_reduced = svd.fit_transform(X)
    elif method == "pca":
        pca = PCA(n_components=n_dims)
        X_reduced = pca.fit_transform(X)
    elif method == "ae":
        import torch
        from torch import nn
        from torch.optim import Adam
        from torch.utils.data import DataLoader, TensorDataset

        # Define the Autoencoder
        class Autoencoder(nn.Module):
            def __init__(self):
                super(Autoencoder, self).__init__()
                D = X.shape[1]
                self.encoder = nn.Sequential(
                    nn.Linear(D, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, n_dims)
                )
                self.decoder = nn.Sequential(
                    nn.Linear(n_dims, 64), nn.ReLU(), nn.Linear(64, 128), nn.ReLU(), nn.Linear(128, D), nn.Sigmoid()
                )  # use a sigmoid for binary features, remove for continuous features

            def forward(self, x):
                x = self.encoder(x)
                x = self.decoder(x)
                return x

        # Convert your data to PyTorch tensors
        X_train_tensor = torch.tensor(X.toarray(), dtype=torch.float32)

        # Create a DataLoader
        dataset = TensorDataset(X_train_tensor)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

        # Create the autoencoder, the optimizer and the loss function
        model = Autoencoder()
        optimizer = Adam(model.parameters(), lr=1e-3)
        loss_fn = nn.MSELoss()

        # Train the autoencoder
        epochs = 100
        print(f"Training an AutoEncoder for {epochs} epochs")

        for epoch in range(epochs):
            for batch in dataloader:
                x = batch[0]
                optimizer.zero_grad()
                output = model(x)
                loss = loss_fn(output, x)
                loss.backward()
                optimizer.step()
            if epoch % 10 == 0:  # print loss every 10 epochs
                print(f"Epoch: {epoch}, Loss: {loss.item()}")

        # Use the encoder to reduce dimensionality
        X_reduced = model.encoder(X_train_tensor).detach().numpy()

    elif method == "vae":
        raise NotImplemented
    else:
        raise NotImplemented
    return X_reduced


def prepare_corpus(
    cursor: pymongo.cursor.Cursor,
    nlp_model,
    debug=False,
):
    unique_labels: List[str] = []
    labels_np: List[np.ndarray] = []
    labels_int: List[int] = []
    corpus: List[str] = []

    n_labels = len(LABELS)

    for j, c in enumerate(cursor):
        # print(f"Processing train doc",j)
        if j > N_DEBUG_ARTICLES and debug:
            break
        string_label = "UNLABELED"
        categories = c.get("category", [])

        categories = [preprocess(nlp_model, cat) for cat in categories]
        print(categories)
        for cat in categories:
            if not type(cat) == str:
                nested_list = False
                try:
                    if type(cat[0]) == str:
                        nested_list = True
                        for c_ in cat:
                            string_label = c_
                            unique_labels.append(c_)
                except IndexError:
                    continue
            else:
                string_label = cat
            if cat not in unique_labels and not nested_list:
                unique_labels.append(cat)
            nested_list = False

        # get the train label for this article (an index of LABELS)
        string_lbl = string_label.strip()
        lbl = LABEL_LOOKUP.get(string_lbl, "UNLABELED")
        # print(f"During labeling of train data, found a new category '{string_lbl}' that must be manually added to monito.similarity.monito_similarity.LABEL_LOOKUP!")
        lbl = LABELS.index(lbl)
        labels_int.append(lbl)
        label_numpy = np.zeros(n_labels)
        # NOTE: only consider one label per datapoint for now
        label_numpy[lbl] = 1  # TODO add multilabels!!! FIXME

        labels_np.append(label_numpy)

        corpus.append(" ".join(preprocess(nlp_model, c["title"] + "\n" + c["text"])))
    print(f"Unique labels: {unique_labels}")
    return corpus, labels_np, labels_int


def classify(
    cursor_train: pymongo.cursor.Cursor,
    cursor_test: pymongo.cursor.Cursor,
    nlp_model,  # spacy.lang.es.Spanish
    vectorizer: TfidfVectorizer,
    debug: bool = False,
    dimensionality_reduction: str = "svd",
    n_dims: int = 3,
    outlier_threshold: float = 2.0,
    visualize: bool = False,
):
    """
    Classify unseen data using clustering and label propagation.

    :param cursor_train: mongodb cursor containing the documents the vectorizer was already fitted to.
    :param cursor_test: mongodb cursor containing the documents that are to be labeled
    :param nlp_model: The SpaCy language model to use for preprocessing.
    :param vectorizer: The TfidfVectorizer
    :param debug: If True, only do a short run with N_DEBUG_ARTICLES documents for each of train/test
    :param dimensionality_reduction: One method out of ("svd", "pca", "ae", "vae")
    :param n_dims: number of dimensions to reduce to
    :param outlier_threshold: the number of standard deviations away from the mean from whereon outliers are ignored (in the reduced space)
    """

    train_corpus, train_labels_np, train_labels_int = prepare_corpus(cursor_train, nlp_model, debug=debug)
    train_labels_np = np.stack(train_labels_np)
    test_corpus, test_labels_np, test_labels_int = prepare_corpus(cursor_test, nlp_model, debug=debug)
    test_labels_np = np.stack(test_labels_np)

    X_train = vectorizer.transform(train_corpus).toarray()
    X_test = vectorizer.transform(test_corpus).toarray()

    repr_train, repr_test, predictions = vae_pipeline(X_train, train_labels_np, X_test, test_labels_np, n_dims=n_dims)
    # # Reduce dimensionality
    # X_train_reduced = reduce_dimensionality(
    #     X_train, method=dimensionality_reduction
    # )
    # X_test_reduced = reduce_dimensionality(
    #     X_test, method=dimensionality_reduction
    # )

    # Outlier removal
    # calculate z-scores
    # z_scores = np.abs(stats.zscore(X_train_reduced.numpy()))

    # # remove outliers
    # X_train_reduced = X_train_reduced[
    #     (z_scores < outlier_threshold).all(axis=1)
    # ]

    if visualize:
        fig = plt.figure(figsize=(16, 12))
        ax_train = fig.add_subplot(121, projection="3d")
        ax_test = fig.add_subplot(122, projection="3d")

        scatter_train = ax_train.scatter(repr_train[:, 0], repr_train[:, 1], repr_train[:, 2], c=train_labels_int)
        scatter_test = ax_test.scatter(repr_test[:, 0], repr_test[:, 1], repr_test[:, 2], c=test_labels_int)
        plt.title(f"3D {dimensionality_reduction.upper()} of train, test")
        plt.show()

    # sim_matrix = cosine_similarity(matrix_old, matrix_new)

    # print(sim_matrix)

    # count = len(texts)
    # count_groups = 0
    # already_processed = set()
    # for i in range(count):
    #     printed_first = False
    #     if i in already_processed:
    #         continue
    #     for j in range(count):
    #         if i == j:
    #             continue
    #         if j in already_processed:
    #             continue
    #         if sim_matrix[i][j] > args.sensitivity:
    #             if not printed_first:
    #                 print(f"\n{i}\t{outlets[i]:30} {titles[i]} {urls[i]}")
    #                 count_groups += 1
    #                 printed_first = True
    #             # print(round(sim_matrix[i][j], 3), i, j)
    #             print(f"{j}\t{outlets[j]:30} {titles[j]} {urls[j]}")
    #             already_processed.add(j)
    #     already_processed.add(i)

    # print("\n", count_groups)


def _parse_arguments(argv=None):
    # parse the command line options
    argparser = argparse.ArgumentParser(
        description="monito.similarity: a tool for monitoring and filtering news feeds. "
        "Please have a look at the documentation (https://monito.readthedocs.io/en/latest/) "
        "for further information on how tho use this software.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    argparser.add_argument(
        "-g",
        "--general-config",
        type=str,
        default="monito_config.toml",
        help="The general configuration file.",
    )
    argparser.add_argument(
        "-l",
        "--log-to-stdout",
        action="store_true",
        default=False,
        help="Write to stdout instead to the logfile set in the general config file.",
    )
    argparser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Switch off text output except for error messages. This will overwrite -v.",
    )
    argparser.add_argument("--verbose", action="store_true", help="more verbose text output")
    argparser.add_argument(
        "--reduction",
        type=str,
        help="Dimensionality Reduction Technique. One of 'svd', 'pca', 'ae', 'vae'",
        choices=["svd", "pca", "ae", "vae"],
    )
    argparser.add_argument("--n-dims", type=int, help="Dimensionality to code for.", default=3)

    argparser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="switch on debug mode.",
    )
    argparser.add_argument(
        "--since",
        type=str,
        default="2023-04-01",
        help="The start date for vectorizer creation in ISO format",
    )
    argparser.add_argument(
        "--till",
        type=str,
        default="2023-04-06",
        help="The end date for vectorizer creation in ISO format",
    )

    argparser.add_argument(
        "-s",
        "--start",
        type=str,
        default="2023-04-07",
        help="The start date for classification in ISO format",
    )
    argparser.add_argument(
        "-e",
        "--end",
        type=str,
        default="2023-04-08",
        help="The end date for classification in ISO format",
    )
    argparser.add_argument(
        "-f",
        "--file",
        type=str,
        default="data/vectorizer_2023-01-06_35087.pk",
        help="The vectorizer file to use for classification.",
    )
    argparser.add_argument("-y", "--sensitivity", type=float, default=0.99, help="The sensitivity TODO")
    argparser.add_argument(
        "-c", "--classify", action="store_true", default=False, help="Whether to classify new articles"
    )
    argparser.add_argument(
        "-v", "--create-vectorizer", action="store_true", default=False, help="Whether to create a new vectorizer"
    )

    return argparser.parse_args(argv)


def run(argv: list = None):
    """the command line tool. Please use the ``--help`` option to get help."""

    # parse the command line options
    args = _parse_arguments(argv)

    # load the general configuration
    log_msgs = load_general_config(args.general_config)

    # set up the output channel
    logging_set_up(args.log_to_stdout)

    # print log messages from loading the general config file
    # for level, msg in log_msgs:
    #     print(level, msg)
    #     log.log(getattr(logging, level), msg)

    # print the logo and version
    if not args.quiet:  # pragma: no cover
        print_logo()

    # set quiet mode
    general_config["_MONITO_QUIET_MODE"] = args.quiet

    # set debug mode
    general_config["_MONITO_DEBUG_MODE"] = args.debug

    # set verbosity level
    set_log_level(args.quiet, args.verbose, args.debug)

    # init data base
    articles_db = init_mongodb()

    if not (args.create_vectorizer or args.classify):
        print(f"Nothing to do (either --create-vectorizer or --classify must be passed.).")
        exit()

    nlp = init_nlp()

    cursor_old = articles_db.find({"published": {"$gte": args.since, "$lte": args.till}})

    # Create a vectorizer or load it from file
    if args.create_vectorizer:
        print(f"Creating Vectorizer with articles from {args.since} to {args.till}")
        corpus_to_compare_to = [preprocess(nlp, c["title"] + "\n" + c["text"]) for c in cursor_old]

        vectorizer = TfidfVectorizer()
        vectorizer.fit(corpus_to_compare_to)

        filename = f"vectorizer_{datetime.today().strftime('%Y-%m-%d')}_{len(corpus_to_compare_to)}.pk"
        with open(filename, "wb") as f:
            pickle.dump(vectorizer, f)

            print(f"{datetime.today().strftime('[%Y-%m-%d %H:%M:%S]')} saved the vectorizer as {filename}")
            vectorizer_file = filename
        print(f"Saved vectorizer as {filename}.")
    else:
        with open(args.file, "rb") as f:
            print(f"Attempting to load vectorizer from {args.file}")
            vectorizer = pickle.load(f)
            print(f"Successfully loaded vectorizer from {args.file}")

    if args.classify:
        print(f"Running Classification for new articles from {args.start} to {args.end}")
        print(f"by comparing to old articles from {args.since} to {args.till}")
        print(f"using the previously created vectorizer at '{args.file}'")

        cursor_new = articles_db.find({"published": {"$gte": args.start, "$lte": args.end}})

        classify(
            cursor_old,
            cursor_new,
            nlp,
            vectorizer,
            debug=args.debug,
            dimensionality_reduction=args.reduction,
            n_dims=args.n_dims,
        )


if __name__ == "__main__":
    import sys

    try:
        run(sys.argv[1:])
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(2)
        except SystemExit:
            os._exit(2)
    finally:
        if "log_filename" in general_config:
            console.save_html(f"{general_config['log_filename']}.html", clear=False)
