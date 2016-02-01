# Braga

An Entity-Component-System system. 

## Prerequisites
Python 2.7

## Installation

`pip install braga`

## What is this?

### ECS In a Nutshell

Entities represent whole "things"--like a cat. Components are groups of attributes or methods that represent abilities or qualities of things. For example, `Location` could be a component class; or `Portable`, or `Container` or `CanBeSwitchedOn` or `Flying` or something else of the sort.

To give an entity, like a cat, abilities, the cat needs to be associated with components, specifically instances of components. For example, to give the cat the quality of being alive, give the cat an instance of the `Alive` component class; that `Alive` instance will store whether on not the cat is alive.

The S of ECS is for System; Systems let you group together Entities for simultaneous updates, and provide a service interface for making changes to Entities with a specified Component profile.

### Why I am writing this package

I need ECS for my [text adventure framework] (https://github.com/astrosilverio/hogwarts). More specifically, I need ECS where, instead of having to look up particular instances of component classes, I can access the component class's attributes from the entities.

### Included Classes
* Entity -- represents an object
* Component -- represents an ability or trait of an object
* System -- manage changes to objects' Components
* Assemblage -- factory to make objects with preset combination of Components
* Aspect -- selects Entities with a particular combination of Components
* World -- collects all Entities and Systems for a given project

## Usage
### Entities
If you intend to make an Entity for use in a particular project, make the Entity and add Components through the World for your project (see below). If you are just messing around, instantiate an Entity with `Entity()`. Entities are created with a uuid.

### Components
My Component class is intended to be used as a base class for user-defined classes that store information and describe actions that can be performed on or by a particular Entity. For example, you might want some entities (cats or trees, for example) to be alive, and others, like filing cabinets or books, to not be alive.
Your `Alive` component might look something like this:

```
class Alive(Component):

	def __init__(self, alive=True):
		self.alive = alive

	def die(self):
		self.alive = False
```
Here, the `Alive` component type stores an attribute that indicates whether the cat or tree or other biological entity is living or dead, as well as a method that will allow the cat or tree to expire.

The attributes and methods that are on components are accessible from the entities that the components are attached to via...

#### Fake Object-Orientation

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

Then the entity will search through all of its components to see if any of them have the attribute before throwing up its hands to say "I don't have that attribute". The result? I can access attributes that are stored in the entity's components as if they were actually stored on the entity itself. Fake object orientation! For example, in the case of a cat with an Alive component attached to it...

```
> cat = Entity()
> cat.components.add(Alive())
> cat.alive
  True
> cat.die()
> cat.alive
  False
```

### Systems

A simple component type like Alive does not need to know about other components or entities or even the entity that particular Alive instances belong to. However, sometimes you should not be able to make changes without applying some logical checks that maybe require knowledge about the component-owning entities. For example, perhaps some entities can pick up and carry other entities. However, a human should not be able to carry more than two things, one in each hand, unless they are wearing a backpack, and a cat should not be able to carry more than one thing, in its mouth. (Obviously this an extremely simplified version of the world. Welcome to game design.)

This example is a use case for a System. In the spirit of layered design, individual Components should not know about other Components or Entities, or even their parent Entity. The point of Systems is to manage the logic involved with modifying Components.

Systems must be initialized with a World (see below). The point of a System is to be responsible for a particular collection of Entities (usually a group of Entities with a particular set of Components), so it doesn't make sense to have a System without a World, which defines all of the Entities in a game, thus providing boundaries for each System.

Besides containing logic, Systems are used to automatically perform an action on or relating to a group of components at a user-defined frequency. Say you had a game with graphics and needed to render the game at a given frequency. You might find it helpful to write a System to gather and export information about the positions of various entities. Each System must have an `update` method that will be called every tick of a clock (whose frequency you define).

### Assemblages

ECS is kinda clunky if you have to separately define each component for each entity. Braga comes with an `Assemblage` class that can be used to make factories. Assemblages store the component types that you want this kind of Entity to have, and their `make` method returns an Entity with that particular combination of Components. Assemblages can be initialized with either a list of component types or a dictionary of component types plus initial parameters. For example:

```
# give component set as a list
> cat_factory = Assemblage([Alive, Portable])
> cat = cat_factory.make()
> new_cat = cat_factory.make()
# give component set as a dictionary
> dead_cat_factory = Assemblage({Alive: {'alive': False}, Portable: {}})
> dead_cat = dead_cat_factory.make()
> dead_cat.alive
  False
```

If you forget a component type, you can add component types to an Assemblage with `add_component`.

You can also pass initial values for specific components in via kwargs to the `make` method:

```
> pet_cat_factory = Assemblage([Name, Alive, Portable])
> former_cat = pet_cat_factory.make(name='Stallion', alive=False)
> new_cat = pet_cat_factory.make(name='Grep')
> former_cat.name
  'Stallion'
> new_cat.alive
  True
```

### Aspects

Aspects are primarily intended to be used by Systems to determine which Entities in the World are relevant to the System in question. Aspects are initialized, like Assemblages, with component types, and have an `is_interested_in` method that, when called with an Entity, will return True if the Entity has a set of component types consistent with the Aspect's.

Aspects can select Entity that _must_ have particular component types, _must not_ have particular component types, _can_ have particular component types, or any combination of the above. Aspects are initialized with sets of components that an entity must have `all_of`, have `some_of`, or `exclude`. For example,

```
# a tree:
#  * must be alive (or have been alive)
#  * must not be able to talk
#  * may or may not have leaves
> tree_aspect = Aspect(all_of=set([Alive]), exclude=set([Conversant]), some_of=set([Deciduous]))
> dead_tree = Assemblage([Alive, Deciduous]).make(alive=False, has_leaves=False)
> ent = Assemblage([Alive, Conversant, Deciduous]).make()
> tree_aspect.is_interested_in(dead_tree)
  True
> tree_aspect.is_interested_in(ent)
  False
```

### Worlds

Worlds are intended to keep track of all the Entities and Systems in a game. If you are using Braga to define objects and abilities and systems for a particular game, you are **strongly** encouraged to only create Entities through the World for your game. Worlds have a `make_entity` method that optionally takes an assemblage and initial kwargs, so you can use `make_entity` just as you would an assemblage's `make` -- only `make_entity` will automatically set your entity up as part of your World.