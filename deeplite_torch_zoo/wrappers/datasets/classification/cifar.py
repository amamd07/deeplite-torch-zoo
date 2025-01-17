import os
from os.path import expanduser

import torchvision

from deeplite_torch_zoo.src.classification.augmentations.augs import \
    get_vanilla_transforms
from deeplite_torch_zoo.src.classification.augmentations.autoaugment import \
    CIFAR10Policy
from deeplite_torch_zoo.wrappers.datasets.utils import get_dataloader
from deeplite_torch_zoo.wrappers.registries import DATA_WRAPPER_REGISTRY

__all__ = ["get_cifar100", "get_cifar10"]


def _get_cifar(
    cifar_cls, data_root="", batch_size=128, test_batch_size=None, img_size=32, num_workers=4, fp16=False,
    download=True, device="cuda", distributed=False, train_transforms=None, val_transforms=None,
):
    if data_root == "":
        data_root = os.path.join(expanduser("~"), ".deeplite-torch-zoo")

    default_train_transforms, default_val_transforms = get_vanilla_transforms(
        img_size,
        mean=(0.4914, 0.4822, 0.4465),
        std=(0.2023, 0.1994, 0.2010),
        crop_pct=1.0,
        add_train_transforms=CIFAR10Policy(),
        cutout_args={'n_holes': 1, 'length': int(img_size / 1.6)},
    )

    train_transforms = train_transforms if train_transforms is not None else default_train_transforms
    val_transforms = val_transforms if val_transforms is not None else default_val_transforms

    train_dataset = cifar_cls(
        root=data_root,
        train=True,
        download=download,
        transform=train_transforms,
    )

    test_dataset = cifar_cls(
        root=data_root,
        train=False,
        download=download,
        transform=val_transforms,
    )

    train_loader = get_dataloader(train_dataset, batch_size=batch_size, num_workers=num_workers,
        fp16=fp16, distributed=distributed, shuffle=not distributed, device=device)

    test_batch_size = batch_size if test_batch_size is None else test_batch_size
    test_loader = get_dataloader(test_dataset, batch_size=test_batch_size, num_workers=num_workers,
        fp16=fp16, distributed=distributed, shuffle=False, device=device)

    return {"train": train_loader, "test": test_loader}


@DATA_WRAPPER_REGISTRY.register(dataset_name="cifar100")
def get_cifar100(
    data_root="", batch_size=128, test_batch_size=None, img_size=32, num_workers=4,
    fp16=False, download=True, device="cuda", distributed=False,
    train_transforms=None, val_transforms=None, **kwargs,
):
    if len(kwargs):
        import sys
        print(f"Warning, {sys._getframe().f_code.co_name}: extra arguments {list(kwargs.keys())}!")

    cifar_cls = torchvision.datasets.CIFAR100
    return _get_cifar(cifar_cls,
        data_root=data_root,
        batch_size=batch_size,
        test_batch_size=test_batch_size,
        img_size=img_size,
        num_workers=num_workers,
        fp16=fp16,
        download=download,
        device=device,
        distributed=distributed,
        train_transforms=train_transforms,
        val_transforms=val_transforms,
    )


@DATA_WRAPPER_REGISTRY.register(dataset_name="cifar10")
def get_cifar10(
    data_root="", batch_size=128, test_batch_size=None,  img_size=32, num_workers=4,
    fp16=False, download=True, device="cuda", distributed=False,
    train_transforms=None, val_transforms=None, **kwargs,
):
    if len(kwargs):
        import sys
        print(f"Warning, {sys._getframe().f_code.co_name}: extra arguments {list(kwargs.keys())}!")

    cifar_cls = torchvision.datasets.CIFAR10
    return _get_cifar(cifar_cls,
        data_root=data_root,
        batch_size=batch_size,
        test_batch_size=test_batch_size,
        img_size=img_size,
        num_workers=num_workers,
        fp16=fp16,
        download=download,
        device=device,
        distributed=distributed,
        train_transforms=train_transforms,
        val_transforms=val_transforms,
    )
