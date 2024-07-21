

1. The juice pack is at the bookshelf instead of at the cabinet
```text
start -> listen -> analise -> nav(cabinet) -> lookfor(juice pack) -> pick(juice pack) -> nav(bookshelf) -> place(juice pack, bookshelf) -> end -> waitForNewCmd
```
2. Put an object on the floor in the kitchen
```text
start -> nav(somewhere) -> lookfor(something) -> pick(something) -> nav(kitchen) -> place(something, floor) -> end -> waitforNewCmd
```
3. There is a person at the pantry, their request is:
	say hello to the person wearing a blue jacket in the living room and follow them to the chairs
```text
start -> nav(pantry) -> lookfor(waving hand) -> audio out('Hello, what's your request') -> listen(state finish when get speech recognition topic) -> analise
-> nav(living room) -> lookfor(blue jacket) -> audio out('Hello, I'm here to help you') -> follow -> end -> waitForNewCmd
```

4. There is a person at the storage rack, their request is:
	tell me how many foods there are on the pantry
```text
start -> nav(storage rack) -> lookfor(waving hand) -> audio out('Hello, what's your request') -> listen(state finish when get speech recognition topic) -> analise
-> nav(pantry) -> lookfor(food) -> count(food) -> Nav ->  audio out('There are 5 foods in the pantry') -> end -> waitForNewCmd
```

1. The red wine is at the desk instead of at the cabinet
```text
start -> listen -> analise -> nav(cabinet) -> lookfor(red wine) -> pick(red wine) -> nav(desk) -> place(red wine, desk) -> end -> waitForNewCmd

```
2. Put an object on the floor in the living room
```text

```
3. There is a person at the side tables, their request is:
	tell me how many standing persons are in the office
4. There is a person at the lamp, their request is:
	bring me a bowl from the sink
