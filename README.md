# Adversarial Training

## Requirements:
To be able to use Madry models, you need to run:
`./install_madry_challenge.sh -d /home/mila/b/berardhu/share/AdversarialTraining/pretrained_models`
where -d specifies the folder where to save the models.

You also need to install tensorflow and advertorch.

If you run a version of pytorch that is >= 1.0.0, I would advise to install the following fork:
```
git clone git@github.com:hugobb/advertorch.git
cd advertorch
python setup.py install
```


## To test the Langevin dynamic on a classifier:
`python -m adv_train.scripts.test_langevin --nb_iter 10 --noise_scale 0.4 --sign_flag --model_dir /home/mila/b/berardhu/share/AdversarialTraining/pretrained_models`

By default this should achieve around 98% error.
To be able to run this command you need to have access to `/home/mila/b/berardhu/share/AdversarialTraining/pretrained_models` on the mila cluster. Let me know if you don't have access to it !

To change the model against which you want to evaluate the attacker simply use the flag: `--name train_0`.


## To train a robust classifier using Langevin:
`python -m adv_train.scripts.train_adv --nb_iter 1 --noise_scale 0.4 --sign_flag --eval_clean_flag --eval_name train_0 --model_dir /home/mila/b/berardhu/share/AdversarialTraining/pretrained_models`

This will train a classifier using langevin. It will also report the error of the adversarial dataset agains a PGD robust model, and it will report the error of the trained classifier on the clean data.

To be able to run this command you need to have access to `/home/mila/b/berardhu/share/AdversarialTraining/pretrained_models` on the mila cluster. Let me know if you don't have access to it !

To change the model against which you want to evaluate the attacker simply use the flag: `--eval_name train_0`.


### Baselines

|   Model A: PGD_ATTACK_train_0                | nb_iter | eps_iter | noise_scale | Training Error | Time   |
|:--------------------------------------------:|:-------:|:--------:|:-----------:|:--------------:|:------:|
| PGD                                          | 100     | 0.2      |             | 31.85%         | 3min32 |
| Langevin (sign_flag = True, noise = normal)  | 100     | 0.2      | 0.1         | 34.63%         | 3min27 |
| Langevin (sign_flag = True, noise = uniform) | 100     | 0.2      | 0.2         | 33.00%         | 3min27 |
| Langevin (sign_flag = True, noise = uniform) | 100     | 0.2      | 0.1         | 33.00%         | 3min27 |

