from dataset import get_data 


if __name__ == "__main__":
    X, y, features = get_data("accident", 'CA', False, root_dir='./datasets/US_Accidents_Dec21_updated.csv')
    print(X.shape, y.shape)