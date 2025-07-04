# ManimGL German Grammar Project

This project uses [ManimGL](https://github.com/3b1b/manim) to create animations and visualizations for German grammar concepts.

## Setting up the Python path

Before running any scripts, set your project directory as the `PYTHONPATH` so that Python can find all modules in this folder:

```sh
export PYTHONPATH=$(pwd)
```

You can add this line to your `~/.zshrc` or `~/.bash_profile` to make it permanent.

## Running ManimGL scenes

Navigate to your project directory and run:

```sh
cd path/to/your/project
manimgl test.py MyScene
```

Replace `MyScene` with the name of the scene you want to render.