import torch
from enum import Enum


class Projection:
    def __init__(self, epsilon, clip_min=0.0, clip_max=1.0):
        self.epsilon = epsilon
        self.clip_min = clip_min
        self.clip_max = clip_max

    def __call__(self, x, x_ref=None):
        return x.clamp(self.clip_min, self.clip_max)

    def is_valid(self, x, x_ref=None) -> bool:
        return (x >= self.clip_min).all() and (x <= self.clip_max).all()


class LinfProjection(Projection):
    def __init__(self, epsilon=0.3, clip_min=0.0, clip_max=1.0):
        super().__init__(epsilon, clip_min, clip_max)

    def __call__(self, x, x_ref):
        x = torch.max(torch.min(x, x_ref + self.epsilon), x_ref - self.epsilon)
        return super().__call__(x, x_ref)

    def is_valid(self, x, x_ref, eps=1e-6) -> bool:
        d = abs(x - x_ref).view(len(x), -1).max(1)[0]
        return (d <= self.epsilon + eps).all() and super().is_valid(x, x_ref)


class NoiseType(Enum):
    UNFIFORM = "uniform"
    NORMAL = "normal"
