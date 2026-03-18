from astroquery.jplhorizons import Horizons
import os
import pandas as pd
import numpy as np


def get_ephemeris(target_id, start, stop, step, centre="500@399"):
    cache_dir = "../cache"
    os.makedirs(cache_dir, exist_ok=True)

    # Creating unique name for cache
    filename = f"eph_{target_id}_{start}_{stop}_{step}_{centre}.csv"
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
        df = obj.ephemerides(quantities="1,9,19,20,23,36,37,38,39").to_pandas()

        # Caching data
        df.to_csv(filepath, index=False)

    # Add extra datetime column as fetched data does not have this
    df["datetime"] = pd.to_datetime(
        df["datetime_str"].str.replace("A.D. ", "", regex=False),
        format="%Y-%b-%d %H:%M"
    )
    return df


# Function to get vectors of a target object
def get_vectors(target_id, start, stop, step, centre="500@10", id_type="designation"):
    cache_dir = "../cache"
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
            id_type=id_type
        )
        df = obj.vectors().to_pandas()

        # Caching data
        df.to_csv(filepath, index=False)

    # Add extra datetime column as fetched data does not have this
    df["datetime"] = pd.to_datetime(
        df["datetime_str"].str.replace("A.D. ", "", regex=False),
        format="%Y-%b-%d %H:%M:%S.%f"
    )
    df["v_kms"] = np.sqrt(df["vx"] ** 2 + df["vy"] ** 2 + df["vz"] ** 2) * 1731.46
    return df

def get_vectors_for_3i_from(centre):
    df_approach = get_vectors("3I", "2023-04-01", "2025-04-01", "30d", centre)

    df_inner = get_vectors("3I", "2025-04-01", "2026-04-01", "1d", centre)

    df_outer = get_vectors("3I", "2026-04-01", "2035-04-01", "7d", centre)

    return pd.concat([df_approach, df_inner, df_outer]).drop_duplicates("datetime_jd")



def make_ellipse(ra, dec, smaa, smia, theta_deg):
    """Returns x, y points tracing out the error ellipse"""
    t = np.linspace(0, 2 * np.pi, 100)
    theta_rad = np.radians(theta_deg)

    # Ellipse points
    x = smaa * np.cos(t)
    y = smia * np.sin(t)

    # Rotate by theta
    x_rot = x * np.cos(theta_rad) - y * np.sin(theta_rad)
    y_rot = x * np.sin(theta_rad) + y * np.cos(theta_rad)

    # Offset to actual sky position (convert arcsec to degrees)
    return ra + x_rot / 3600, dec + y_rot / 3600



