"""
Reinforcement learning Lens System Design
States Space: Lens1_r1, Lens1_r2, Lens1_n, Lens1_t, Lens2_r1, Lens2_r2, Lens2_n, Lens2_t, Lens3_r1,
Lens3_r2, Lens3_n, Lens3_t,
Action Space: L1B+, L1B-, L2B+, L2B-, L3B+, L3B-
Reward Function: Calculate Aberration is more closing zero, reward is more.

The RL is in RL_brain.py.

"""
import math
import tkinter as tk
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import random


# Coddington Factor

class LensTest(tk.Tk, object):
    def __init__(self):
        super(LensTest, self).__init__()
        self.action_space = ['X+', 'X-', 'Y+', 'Y-', 'Z+', 'Z-']
        self.cF_threshold = 10
        self.abbb_threshold = 0.02

        # Angle limit set to 2 * theta_threshold_radians so failing observation is still within bounds
        high = np.array([
            self.cF_threshold * 2,
            self.cF_threshold * 2,
            self.cF_threshold * 2])

        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        # observation space [cF1, cF2, cF3, lens1_r1, lens1_r2, lens2_r1, lens2_r2, lens3_r1, lens3_r2, d1, d2]
        self.n_actions = len(self.action_space)
        self.n_features = self.observation_space.shape[0]
        # self.title('Viewer')
        # self.geometry('{0}x{1}'.format(800, 500))
        # self._build_viewer()

        self.seed()
        self.state = None
        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        # self.update()
        # time.sleep(0.1)
        # self.canvas.delete(self.curve)
        X = 0
        Y = 0
        Z = 0

        self.state = (X, Y, Z)
        self.steps_beyond_done = None
        # self.curve.drawenv(lens1_r1, lens1_r2, lens1_t, d1, lens2_r1, lens2_r2, lens2_t, d2, lens3_r1, lens3_r2, lens3_t)
        # self.curve.mainloop()
        return np.array(self.state)

    def step(self, action):
        # assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        state = self.state
        X, Y, Z = state
        abbb1 = (X - 4) * (X - 4) + (Y + 5) * (Y + 5) + (Z - 8.4) * (Z - 8.4)

        if action == 0:   # X+
            X += 0.5
        elif action == 1:   # X-
            X -= 0.5
        elif action == 2:   # Y+
            Y += 0.5
        elif action == 3:   # Y-
            Y -= 0.5
        elif action == 4:   # Z+
            Z += 0.5
        elif action == 5:   # Z-
            Z -= 0.5

        abbb2 = (X - 4)*(X - 4) + (Y + 5)*(Y + 5)+(Z - 8.4)*(Z - 8.4)

        self.state = (X, Y, Z)
        done = abbb2 < self.abbb_threshold
        done = bool(done)

        if not done:

            if abbb1 >= abbb2:
                reward = 5.0
            else:
                 reward = -100.0

        elif self.steps_beyond_done is None:

            self.steps_beyond_done = 0

            if abbb1 >= abbb2:
                reward = 100.0
            else:
                reward = -100.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn(
                    "You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 100.0

        return np.array(self.state), reward, done, {}

    def render(self):
        # time.sleep(0.01)
        self.update()

