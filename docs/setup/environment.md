---
title: "Setting up the conda environment"
---
The easiest way to make sure that everything will run for you is to install that latest version of [Miniconda](https://docs.conda.io/projects/conda/en/latest/index.html) and then utilize the `conda` package manager to install one of the environment files saved inside of the `environments/` directory.

Note that both environment files are should be interchangeable.
Both are offered because they offer different levels of specificity and, as a result, have their own pros and cons.
See the [conda cheatsheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html) for help with `conda`.

Environment files: 
1. `environments/environment_cross_platform.yml` : this file is intended to be cross-platform compatible, however, it contains considerably less information about _exactly_ which packages are being utilized when compared with the second file.

2. `environments/environment_plt_pkg.yml` : this file contains much more information about all the versions of everything utilized in the latest working evironment.

You can set up the environment with the following command from the root directory of this repository.

```bash
conda env create -n top-fibers --file environments/ENVIRONMENT_FILE_NAME.yml
```

> Notes:
> - Replace `ENVIRONMENT_FILE_NAME.yml` with the file you prefer to use to install.
> - Both of the above commands will create an environment called `top-fibers`.
> - To change the name of your environment, replace `top-fibers` with whatever you prefer.