from .langevin import Langevin
from advertorch.attacks import LinfPGDAttack
from .utils import LinfProjection
from enum import Enum
import argparse
import torch.nn as nn


class Attacker(Enum):
    PGD = 'pgd'
    LANGEVIN = 'langevin'

    @classmethod
    def add_arguments(cls, parser=None):
        if parser is None:
            parser = argparse.ArgumentParser()

        parser.add_argument('--attacker_type', default=cls.LANGEVIN, type=cls, choices=cls)
        parser.add_argument('--nb_iter', default=10, type=int)
        parser.add_argument('--eps_iter', default=1., type=float)
        parser.add_argument('--sign_flag', action="store_true")
        parser.add_argument('--noise_scale', default=1, type=float)

        return parser

    @classmethod
    def load_attacker(cls, classifier, args):
        projection = LinfProjection()
        loss_fn = nn.CrossEntropyLoss()
        if args.attacker_type == cls.PGD:
            attacker = LinfPGDAttack(classifier, loss_fn=loss_fn, eps=projection.epsilon, nb_iter=args.nb_iter, eps_iter=args.eps_iter, clip_min=projection.clip_min,
                                     clip_max=projection.clip_max)
            attacker.projection = projection
        elif args.attacker_type == cls.LANGEVIN:
            attacker = Langevin(classifier, loss_fn=loss_fn, projection=projection, nb_iter=args.nb_iter, eps_iter=args.eps_iter, sign_flag=args.sign_flag,
                                 noise_scale=args.noise_scale)
        
        return attacker