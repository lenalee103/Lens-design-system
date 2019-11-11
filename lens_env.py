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
from curvedrawing import drawcurve
from CalculateAberration import cfunc
from CalculateBending import cBending
from CalculateDistances import cDistances
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import random


# Coddington Factor

# Customer defining parameters (Test Data from cpp)
wavelength = 1.064
h = 2
h_in = 2.
h_out = 1.0 / 2.8 * 2.0

# d1 & d2 can be calculated by Cailing's cpp file.

# Initial parameters:

lens1_n = 1.50663348492911
lens1_t = 7.74
lens2_n = 1.75389272961219
lens2_t = 2
lens3_n = 1.50663348492911
lens3_t = 4.1


class Lens(tk.Tk, object):
    def __init__(self):
        super(Lens, self).__init__()
        self.action_space = ['L1B+', 'L1B-', 'L2B+', 'L2B-', 'L3B+', 'L3B-']
        self.cF_threshold = 4

        # Angle limit set to 2 * theta_threshold_radians so failing observation is still within bounds
        high = np.array([
            self.cF_threshold * 2,
            self.cF_threshold * 2,
            self.cF_threshold * 2,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max])

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

    # def _build_viewer(self):
        # self.canvas = tk.Canvas(self, bg='white', height=500, width=800)

        # create curves
     #   self.curve = drawcurve()
     #   d1 = 17.0197423589288
     #   d2 = 7.74878708722231
     #   lens1_r1 = 29.52
     #   lens1_r2 = -29.52
     #   lens2_r1 = -7
     #   lens2_r2 = 1 / 1e+12
     #   lens3_r1 = 38.6
     #   lens3_r2 = 1 / 1e+12
     #   self.curve.drawenv(lens1_r1, lens1_r2, lens1_t, d1, lens2_r1, lens2_r2, lens2_t, d2, lens3_r1, lens3_r2, lens3_t)
     #   self.curve.mainloop()

        # pack all
     #  self.canvas.pack()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        # self.update()
        # time.sleep(0.1)
        # self.canvas.delete(self.curve)
        cF1 = 0
        cF2 = 0
        cF3 = 0
        d1 = random.uniform(0, 100)
        d2 = random.uniform(0, 100)
        lens1_r1 = 29.5
        lens1_r2 = -29.5
        lens2_r1 = -7
        lens2_r2 = 1e+12
        lens3_r1 = 38.6
        lens3_r2 = 1e+12


        self.state = (cF1, cF2, cF3, lens1_r1, lens1_r2, lens2_r1, lens2_r2, lens3_r1, lens3_r2, d1, d2)
        self.steps_beyond_done = None
        # self.curve.drawenv(lens1_r1, lens1_r2, lens1_t, d1, lens2_r1, lens2_r2, lens2_t, d2, lens3_r1, lens3_r2, lens3_t)
        # self.curve.mainloop()
        return np.array(self.state)

    def step(self, action):
        # assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        state = self.state
        cF1, cF2, cF3, lens1_r1, lens1_r2, lens2_r1, lens2_r2, lens3_r1, lens3_r2, d1, d2 = state
        if action == 0:   # L1B+
            cF1 += 0.05
        elif action == 1:   # L1B-
            cF1 -= 0.05
        elif action == 2:   # L2B+
            cF2 += 0.05
        elif action == 3:   # L2B-
            cF2 -= 0.05
        elif action == 4:   # L3B+
            cF3 += 0.05
        elif action == 5:   # L3B-
            cF3 -= 0.05

        lens1_r1_ = cBending(cF1, lens1_n, lens1_r1, lens1_r2)[0]
        lens1_r2_ = cBending(cF1, lens1_n, lens1_r1, lens1_r2)[1]
        lens2_r1_ = cBending(cF2, lens2_n, lens2_r1, lens2_r2)[0]
        lens2_r2_ = cBending(cF2, lens2_n, lens2_r1, lens2_r2)[1]
        lens3_r1_ = cBending(cF3, lens3_n, lens3_r1, lens3_r2)[0]
        lens3_r2_ = cBending(cF3, lens3_n, lens3_r1, lens3_r2)[1]

        d1_ = cDistances(h_in, h_out, lens1_r1_, lens1_r2_, lens1_n, lens1_t, lens2_r1_, lens2_r2_, lens2_n, lens2_t,
                        lens3_r1_, lens3_r2_, lens3_n, lens3_t)[0]
        d2_ = cDistances(h_in, h_out, lens1_r1_, lens1_r2_, lens1_n, lens1_t, lens2_r1_, lens2_r2_, lens2_n, lens2_t,
                        lens3_r1_, lens3_r2_, lens3_n, lens3_t)[1]

        self.state = (cF1, cF2, cF3, lens1_r1_, lens1_r2_, lens2_r1_, lens2_r2_, lens3_r1_, lens3_r2_, d1_, d2_)
        abb1 = cfunc(wavelength, h, d1, d2, lens1_r1_, lens1_r2, lens1_n, lens1_t, lens2_r1, lens2_r2, lens2_n,
                     lens2_t, lens3_r1, lens3_r2, lens3_n, lens3_t)
        abb2 = cfunc(wavelength, h, d1_, d2_, lens1_r1_, lens1_r2_, lens1_n, lens1_t, lens2_r1_, lens2_r2_, lens2_n,
                     lens2_t, lens3_r1_, lens3_r2_, lens3_n, lens3_t)
        done1 = cF1 < -self.cF_threshold \
               or cF1 > self.cF_threshold \
               or cF2 < -self.cF_threshold \
               or cF2 > self.cF_threshold \
               or cF3 < -self.cF_threshold \
               or cF3 > self.cF_threshold \
               or d1 < 0 \
               or d2 < 0.5\

        done = abb2 < 0.5
        done = bool(done)
        done1 = bool(done1)
        if done1:
            reward = -200.00
        else:
            if not done:
                if abb1 >= abb2:
                    reward = 50.0
                else:
                    reward = -100.0
            elif self.steps_beyond_done is None:
                self.steps_beyond_done = 0
                if abb1 >= abb2:
                    reward = 50.0
                else:
                    reward = -150.0
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



