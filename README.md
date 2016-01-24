# Braga

An Entity-Component-System system. 

## Prerequisites
Python 2.7

## Installation

`pip install braga`

## What is this?

### My understanding of ECS

Entities represent whole "things"--like a cat. Components are groups of attributes or methods that represent abilities or qualities of things. For example, `Living` could be a component class; or `Portable`, or `Container` or `CanBeSwitchedOn` or `Flying` or something else of the sort.

To give an entity, like a cat, abilities, the cat needs to be associated with components, specifically instances of components. For example, to give the cat the quality of being alive, give the cat an instance of the `Living` component class; that `Living` instance will store whether on not the cat is alive.

The S of ECS is for System; Systems let you group together Entities for simultaneous updates, and provide a service interface for making changes to Entities with a specified Component profile.

### Why I am writing this package

I need ECS for my [text adventure framework] (https://github.com/astrosilverio/hogwarts). More specifically, I need ECS where, instead of having to look up particular instances of component classes, I can access the component class's attributes from the entities.

## Usage

```
> cat = Entity(0)
> catalive = Alive()  # user-defined Component
> cat.components.add(catalive)

> cat.alive
  True
> cat.die()
> cat.alive
  False
```

### Fake Object-Orientation

When I started playing with ECS, the first thing I noticed was that I was annoyed that attributes did not belong to entities. While that is the design feature that makes ECS so extensible / unique / useful, it is also really irritating if every time you want to check if the cat is alive, you have to check that attribute on a _component_ on the cat instead of the cat itself.

Besides making it annoying for me to mess around with entities in the repl, I realized that the extra overhead required to access attributes would complicate my text adventure code. I don't want hogwarts to know how its Rooms and Things and Players work under the hood. So I violated the guiding principle of ECS a bit and am faking object orientation by rewriting `__getattr__` on Entities.

The familiar way of accessing attributes with dots, like `cat.components`, is just sugar for `getattr(cat, 'components')`. Normally, `__getattr__` will raise an `AttributeError` if an attribute is not found. If I wasn't faking object-orientation, then `cat.components` would not raise an `AttributeError` but `cat.alive` would, because the `cat` Entity does not have an attribute `alive`. But if you hack the Entity's `__getattr__` like so:

```
    def __getattr__(self, name):
        for component in self.components:
            try:
                attr = getattr(component, name)
            except AttributeError:
                pass
            else:
                return attr
        raise AttributeError
```

Then the entity will search through all of its components to see if any of them have the attribute before throwing up its hands to say "I don't have that attribute". The result? I can access attributes that are stored in the entity's components as if they were actually stored on the entity itself. Fake object orientation!

### Assemblages

ECS is kinda clunky if you have to separately define each component for each entity. Braga comes with an `Assemblage` class that can be used to make factories. For example:

```
# factory setup work
> cat_factory = Assemblage([Alive, Portable])
> cat_factory.add_component(Container)

# start using factory to make cats
> cat = cat_factory.make()
> new_cat = cat_factory.make()
```