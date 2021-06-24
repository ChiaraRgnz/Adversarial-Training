from torchvision.datasets import MNIST
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from adv_train.model.dataset import DatasetParams


def load_mnist_dataset(params: DatasetParams = DatasetParams(), train: bool = True) -> MNIST:
    transform = transforms.Compose([transforms.ToTensor()])
    return MNIST(root=params.data_dir, train=train, transform=transform, download=params.download)


def create_mnist_loaders(params: DatasetParams = DatasetParams()) -> (DataLoader, DataLoader):
    trainset = load_mnist_dataset(params, True)
    testset = load_mnist_dataset(params, False)

    train_loader = DataLoader(trainset, batch_size=params.batch_size, shuffle=params.shuffle, num_workers=params.num_workers)
    test_loader = DataLoader(testset, batch_size=params.test_batch_size, num_workers=params.num_workers)

    return train_loader, test_loader