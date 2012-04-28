# gitspork [![endorse](http://api.coderwall.com/modocache/endorsecount.png)](http://coderwall.com/modocache)

Change the origin repository of your submodules 
so you can work on submodule forks easily.

### Installation

    $ pip install git+http://modocache@github.com/modocache/gitspork.git

### Usage

For example, let's say I want to work on my fork 
of [JSONKit](https://github.com/johnezang/JSONKit) in
my app project.

    $ gitspork /Users/modocache/app vendor/JSONKit JSONKit modocache

After I've made my changes and pushed to my fork, I can revert back to
the original owner's repository just as easily:

    $ gitspork /Users/modocache/app vendor/JSONKit JSONKit johnezang

For more help, you can always type:

    $ gitspork --help

### License

Use as you please.
