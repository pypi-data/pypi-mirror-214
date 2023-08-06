from foreverbull.cli import cli
from multiprocessing import set_start_method

if __name__ == "__main__":
    set_start_method("spawn")
    cli()
