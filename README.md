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

The S of ECS is for System; Systems let you group together Entities for simultaneous updates. I don't really know how threads work right now so this is just a skeleton.

### Why I am writing this package

I need ECS for my [text adventure framework] (https://github.com/astrosilverio/hogwarts). More specifically, I need ECS where, instead of having to look up particular instances of component classes, I can access the component class's attributes from the entities.

## Usage

```
> cat = Entity(0)
> catliving = Living()
> cat.components.add(catliving)

> cat.alive
  True
> cat.die()
> cat.alive
  False
```




