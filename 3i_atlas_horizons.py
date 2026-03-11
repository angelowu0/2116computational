import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_vectors
import numpy as np

# Part 1 - Get the vectors of the comet

df_approach = get_vectors("3I", "2023-04-01","2025-04-01","30d")

df_inner = get_vectors("3I", "2025-04-01","2026-04-01","1d")

df_outer = get_vectors("3I", "2026-04-01","2035-04-01","7d")

df_comet = pd.concat([df_approach, df_inner, df_outer])

df_inner["v_kms"] = np.sqrt(df_inner.vx**2 + df_inner.vy**2 + df_inner.vz**2) * 1731.46

print(df_comet.columns)
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,8))    # create a figure with one set of axes

ax1.plot(df_comet["datetime"], df_comet["range"])               # draw on those axes
ax1.set_title("Comet 3I Distance From Sun 2024-2034")
ax1.set_xlabel("Datetime")
ax1.set_ylabel("Distance From Sun (AU)")

ax2.plot(df_inner["datetime"], df_inner["range"])               # draw on those axes
ax2.set_title("Comet 3I Distance From Sun 2025/4/1-2026/4/1")
ax2.set_xlabel("Datetime")
ax2.set_ylabel("Distance From Sun (AU)")

fig1, ax3 = plt.subplots()
ax3.plot(df_inner["datetime"], df_inner["v_kms"])               # draw on those axes
ax3.set_title("Comet 3I Velocity Relative to Sun 2025/4/1-2026/4/1")
ax3.set_xlabel("Datetime")
ax3.set_ylabel("Velocity Relative to Sun (km/s)")


plt.show()