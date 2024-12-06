# check if torch is installed, if yes, from . import cnn, if not, do not import cnn
if __name__ == '__main__':
    try:
        import torch
        from . import cnn
    except ImportError:
        print('Torch is not installed, cnn module will not be imported.')
        pass
