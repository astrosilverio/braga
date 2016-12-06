"""
Contains the Assemblages and Systems required for a simple Potions game.

Sample game:

You are in the potions classroom. An empty cauldron is on your desk, as well as some mistletoe berries, a bezoar, and shavings of unicorn horn.
> put lacewing flies in cauldron
I'm sorry, I don't see any lacewing flies here.
> put berries in cauldron
Your cauldron now contains mistletoe berries.
> look
You are in the potions classroom. A partly-full cauldron is on your desk, as well as a bezoar and shavings of unicorn horn.
> look in cauldron
Your cauldron now contains mistletoe berries.
> stir
Nothing happens.
> heat cauldron
Your cauldron steams gently.
> wait
You are in the potions classroom. There is a partly-full cauldron steaming gently on your desk, as well as a bezoar and shavings of unicorn horn.
> stir
Nothing happens.
> put bezoar in cauldron
Your cauldron now contains mistletoe berries and a bezoar.
> look in cauldron
Your cauldron now contains mistletoe berries and a bezoar. It is steaming gently.
> put shavings in cauldron
Your cauldron now contains mistletoe berries, a bezoar, and shavings of unicorn horn.
> remove bezoar from cauldron
You try to remove the bezoar (with magic, of course, it's much to hot to handle). However, it's already partly...congealed? Maybe someday you will have mastered potions well enough to remove ingredients from them, but for now you'll have to leave the bezoar in the cauldron.
> stir
Your cauldron hums softly and harmoniously as you stir it.
> look in cauldron
Your cauldron contains a brewing potion. It is steaming gently.
> wait
You are in the potions classroom. There is a potion brewing in the cauldron steaming gently on your desk.
> stir
Your cauldron hums softly and harmoniously as you stir it.
> stop brewing
With a flick of your wand, you stop heating the cauldron.
> look
You are in the potions classroom. There is a cauldron full of Antidote for Common Poisons on your desk.
"""

# not generator
def firstn(n):
    num, nums = 0, []
    while num < n:
        nums.append(num)
        num += 1
    return nums

# generator
def firstn(n):
    num = 0
    while num < n:
        yield num
        num += 1