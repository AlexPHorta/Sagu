# EPITAPH

> Collect nuggets of wisdom from the development of this software, for future reference.

## Commit 6760e85061cc6171831f1c43d68971717392a138

I started to use Hatch for project management. The tests stopped working. Had to copy some configuration from a blank Hatch project. The tests still not working (No combination of relative imports worked.). Then, I stumbled upon a Stack Overflow answer [This one!](https://stackoverflow.com/a/75809691) and had the idea of including `pythonpath` to the test environment configuration. Everything started to work smoothly. Cool!
