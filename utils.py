from astroquery.jplhorizons import Horizons
import os
import pandas as pd

# Function to get vectors of a target object
def get_vectors(target_id, start, stop, step, centre="500@10"):
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)

    # Creating unique name for cache
    filename = f"cache_{target_id}_{start}_{stop}_{step}_{centre}.csv"
    filename = filename.replace("/", "-").replace("@", "_")  # safe filename
    filepath = os.path.join(cache_dir, filename)

    if os.path.exists(filepath):
        df = pd.read_csv(filepath)

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
        df.to_csv(filepath, index=False)

    # Add extra datetime column as fetched data does not have this
    df["datetime"] = pd.to_datetime(
        df["datetime_str"].str.replace("A.D. ", "", regex=False),
        format="%Y-%b-%d %H:%M:%S.%f"
    )
    return df

def get_vectors_for_3i_from(centre):
    df_approach = get_vectors("3I", "2023-04-01", "2025-04-01", "30d", centre)

    df_inner = get_vectors("3I", "2025-04-01", "2026-04-01", "1d", centre)

    df_outer = get_vectors("3I", "2026-04-01", "2035-04-01", "7d", centre)

    return pd.concat([df_approach, df_inner, df_outer]).drop_duplicates("datetime_jd")
