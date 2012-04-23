# Submodule Switcher

Change the origin repository of your submodules 
so you can work on submodule forks easily.

### Usage

For example, let's say I want to work on my fork 
of [JSONKit](https://github.com/johnezang/JSONKit) in
my app project.

    $ ./submodule_switcher.py /Users/modocache/app vendor/JSONKit JSONKit modocache

After I've made my changes and pushed to my fork, I can revert back to
the original owner's repository just as easily:

    $ ./submodule_switcher.py /Users/modocache/app vendor/JSONKit JSONKit johnezang

For more help, you can always type:

    $ ./submodule_switcher.py --help

### License

Use as you please.
