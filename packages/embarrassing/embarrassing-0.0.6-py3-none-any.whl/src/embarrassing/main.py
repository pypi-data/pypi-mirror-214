from tqdm import tqdm
from joblib import Parallel, delayed


def embarrassing(contents, callback, n_jobs=8):
    with tqdm(total=len(contents)) as progress_bar:

        def uuu(q):
            ret = callback(q)
            progress_bar.update()
            return ret

        return Parallel(n_jobs=n_jobs, prefer="threads")(
            delayed(uuu)(i) for i in contents
        )
