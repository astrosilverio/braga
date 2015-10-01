# Entity-Component-System and Text Adventures

The most recent development in my text adventure framework process is that 

## Testing!
Programmers are perfectionists. I get it. There's a not-so-tiny voice in my head that tells me constantly that I can't possibly integrate my ECS package with the text adventure framework until the ECS system is finished and the text adventure is done except for the state.

**THIS VOICE IS WRONG!**

Yeah, my ECS system is skeletal right now. *BUT* the main reason I'm working on it is so it can be useful to the text adventure. If I don't test how they fit together, and test that frequently, I'll have more trouble making them work together later on. I won't know which features I should build and which I should scrap.

Also, finishing a software project is daunting. It's basically impossible for a project to be complete--there's always another feature you could add, some old bits to refactor, some documentation to do, etc. If I wait until braga is done before I integrate it with hogwarts, they will never be integrated.

Fine. Enough of the evangelizing. How does it actually work?

The task I'm setting myself is to build a two-room map, with a player and at least one portable and one non-portable object. Things that should work:

1. Player can move between rooms (`go` behaves properly)
2. Player can pick up portable object and cannot pick up non-portable object (`take` works and integrates with the `Portable` component)
3. Room inventory changes when portable object is removed from / added to it
4. Player inventory changes when portable object is removed from / added to it
5. [stretch goal] Room description changes when portable object is removed from / added to it

The first four items are confirmation that Entities and Components behave as expected, and can interact with Commands. I've been testing Entities and Components a fair bit, so I'm not too worried about that. I suspect that the integration with Commands will not be totally seamless, but I expect that it will be possible.

Descriptions are a stretch goal because they will be dynamically changing throughout the game. In a text adventure, the text descriptions of the stateful things are a bit like the renderings of a graphics game--they represent the state of the game to the user, and they need to change as the state changes. Therefore, I think I should treat descriptions like the graphics part of an ECS-modeled game and have a System that takes care of modifying descriptions. I have a verrrrry basic proof of concept, but getting it actually right will probably take a while.

### 11am-3:30pm: Proof of concept for description changes

I spent the entire early afternoon adding bits to braga in preparation for the description system rabbit hole. Now, entities optionally have descriptions, and I wrote a System that changes descriptions, proving that in a very very simple way I can "render" my objects. Leaving off there because the next steps are going to be a lot of work: R had a brilliant idea back in June that descriptions could be written in a kind of markdown, for example you could make a room description like this:

	You are in a small, spotless office. A {{cat.description}} 
	{{cat.alive? "hisses discontedly at you from" : "lies crumpled on"}} the floor.
	
	{{office.portable_inventory}}

And assuming that the cat is alive and the office also contains an invisibility cloak and a sweater, the description would read:

	You are in a small, spotless office. A scrawny, dust-colored cat with lamplike eyes
	hisses discontentedly at you from the floor.
	
	There is a shiny, shimmery cloak here!
	A thick, ugly sweater with an "R" on it is here.

This method just seems so clean and extensible and easily customizable, I'm really looking forward to making it work.

### 3:30pm-4pm: Write this doc

### 4pm-5pm: Make a toy game!