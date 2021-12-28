# Configuration

First, you need to compile all the tools that will be used in the framework. You can do this using the following commands:

    $ make all

After that, I recommend you to create a conda environment and install all dependencies inside it. 

    $ conda create --name <env_name> --file requirements.txt

In case you get any errors, then try using the following command:

    $ conda create --name <env_name> -f requirements.yml

Now you are ready to use the framework. The main script its called *main_compare.py*. This script can be used to compare a list of generators. Parameters of this script can be listed using ``python main_compare.py -h``. These are the parameters:

* **-r**: Path where results will be saved after comparison.
* **-o**: Path to original formulas (family directory).
* **-s**: List of paths where the generated formulas are stored. One directory for each generator you want to compare.
* **-l**: When you are working with big formulas, it can cause memory issues in your computer. In order to prevent that, you can use this option to make a low memory consuming execution (slower than the original, but less memory will be used).
* **--ignore_solvers**: Use this flag if you want to skip solvers execution.

You can use this script like this:

    $ python main_compare.py -o <family_path> -s <generator_paths_list> -r <results_path> [-l] [--ignore_solvers]