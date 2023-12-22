import matplotlib.pyplot as plt

# Data
innings = list(range(1, 10))
outs = [44, 50, 27, 42, 27, 34, 17, 25, 61]
balls = [37, 44, 21, 52, 42, 14, 16, 14, 45]
strikes = [31, 33, 28, 50, 48, 31, 15, 12, 32]

# Plotting
fig, ax1 = plt.subplots()

# Plotting outs
color = 'tab:red'
ax1.set_xlabel('Inning')
ax1.set_ylabel('Outs', color=color)
ax1.plot(innings, outs, color=color, marker='o', label='Outs')
ax1.tick_params(axis='y', labelcolor=color)

# Creating a second y-axis for balls and strikes
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Balls', color=color)
ax2.plot(innings, balls, color=color, marker='o', linestyle='--', label='Balls')
ax2.tick_params(axis='y', labelcolor=color)

ax3 = ax1.twinx()
color = 'tab:green'
ax3.spines['right'].set_position(('outward', 60))
ax3.set_ylabel('Strikes', color=color)
ax3.plot(innings, strikes, color=color, marker='o', linestyle='-.', label='Strikes')
ax3.tick_params(axis='y', labelcolor=color)

# Title and legend
plt.title('Frequency of Outs, Balls, and Strikes in Each Inning')
fig.tight_layout()
fig.legend(loc='upper right')

plt.show()
