from astroquery.jplhorizons import Horizons
import os
import pandas as pd

CACHE_DIR = "cache"

# Function to get vectors of a target object
def get_vectors(target_id, start, stop, step, centre="500@10"):
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Creating unique name for cache
    filename = f"cache_{target_id}_{start}_{stop}_{step}_{centre}.csv"
    filename = filename.replace("/", "-").replace("@", "_")  # safe filename
    filepath = os.path.join(CACHE_DIR, filename)

    if os.path.exists(filename):
        df = pd.read_csv(filename)

    else:
        # Fetching data
        obj = Horizons(
            id=target_id,
            location=centre,
            epochs={"start": start,
                    "stop": stop,
                    "step": step},
            id_type="designation"
        )
        df = obj.vectors().to_pandas()

        # Caching data
        df.to_csv(filename, index=False)

    df["datetime"] = pd.to_datetime(
        df["datetime_str"].str.replace("A.D. ", "", regex=False),
        format="%Y-%b-%d %H:%M:%S.%f"
    )
    return df