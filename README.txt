Course:	     CS-131-Artificial Intelligence
Assignment: Behavior Tree in Cleaner
Name: 	     Yige Sun

I assume:
	1)Cleaner will stop docking and start to do other things when its battery is 100.
	2)During doing tasks, the battery will drop.
	3)Since when cleaner do nothing will not perform any action, the battery will drop slower i.e. every task will coster 10, but do nothing will only cost 1.
	4)The path to home is randomly generated. Besides, the dusty spot location is also randomly given.
 	5)Cleaner can move in vertical and horizontal ways, just like robots in Amazon video shown in class.
	6)In order to make the process visible, use print to show what the cleaner is doing.
	7)Every time cleaner finishes an entire task(like dock, go home etc), it will rest for 2s.
	8)Each time cleaner finishes a sub-task(like turn 90 degrees, detect spot etc), it will rest for 1s.
	9)Since there's no real device, I let the program rest for 3s instead of doing nothing.
	10)To activate or not to activate the spot clean, general clean and dusty spot clean depends on the 
	     random number. There are some situations for now:
		a) Spot clean activated, general clean not activated.
		b) Spot clean not activated, general clean activated.
			i.) Dusty spots exist.
		               ii.) Dusty spots not exist.
		c) Spot clean activated, general clean activated.
			i.) Dusty spots exist.
		               ii.) Dusty spots not exist.
		d) Spot clean not activated, general clean not activated.
	     If action is not activated, this action will be passed and move on to next priority action. Which action is
	     activated will be shown. In order to make cleaner 'smarter', whether or not can be modified in Cleaner.run().
	11) Although actions can be activated. However, once the battery is low, cleaner will go back home to 
 	      charge after charging finished, new actions command will be generated.
	12) Cleaner will keep running till key board interruption is performed.
	13) Cleaner will check battery when one task is finished.

Following the instruction, I use a proper object-oriented design and a hierarchy of class definitions for different
node types as:
	Node->Composite-->Squence, Selection, Priority
	         ->Decorator-->Negation, doUntil, doTime
	         ->Condition-->checkBattery, checkSpot, checkGeneral, checkDustySpot
	         ->Task-->findHome, goHome, Dock, cleanSpot, cleanDustySpot, doneSpot. doneDustySpot, Clean,
		          doneGeneral, doNothing