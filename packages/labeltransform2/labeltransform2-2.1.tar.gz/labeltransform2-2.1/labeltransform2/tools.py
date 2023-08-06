from sklearn.model_selection import train_test_split
from pathlib import Path


def split_dataset(img_dir, out_dir=None, train=8, val=1, test=1):
    img_dir = Path(img_dir)
    out_dir = out_dir or img_dir.parent
    names = [i.stem for i in img_dir.glob("*.jpg") \
        if img_dir.joinpath(i.stem + ".xml").exists()]
    train_ratio = train / (train + val + test)
    val_ratio = val / (val + test)
    train_data, test_val_data = train_test_split(names, train_size=train_ratio)
    val_data, test_data = train_test_split(test_val_data, train_size=val_ratio)
    datas = [train_data, val_data, test_data]
    files = ["train.txt", "val.txt", "test.txt"]

    for file, data in zip(files, datas):
        data = [img_dir.joinpath(i + ".jpg").absolute().__str__() + "\n" for i in data]
        with open(out_dir.joinpath(file), "w")as f:
            f.writelines(data)


