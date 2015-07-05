#Command line TODO-Lists.
[NEW] Gamified Todo-lists. Plus Firebase Support for syncing.

Manage your todos from command line.

Current Version is 0.5alpha3 called "Warbler".

### Features (DONE)
- Add Todos + bounty
- Get All Todos
- Get Todos by name
- Mark the todos done.
- Command line coloring.
- Tags
- Filters
- Rewards.
- Due Dates/ times.
- Folders/Project Categorization.
- Snooze by Edit.
- time-logging.
- Snoozes.
- timers.
- User Dashboard in command line.
- dynamic folders.


##Usage
> This part of document is for main commands in the cmd-todo Suite.

###1.Add a Todo/ Reward.
> Adding a todo/task or Reward.

- Quick Add ( fast add via command line.)
 > --add/-a with 2 args, task and bounty
```bash
python todo.py -a/--add [task] [bounty]
```

__Note__: Quick Add still doesn't support due dates, tags and folders. [In works.]

- Add with a flow (Series of Questions like task, bounty etc.)
 > --add/-a with no argument
```bash
python todo.py -a/--add
```
 > Will end up in resonsive addflow.


- Add a reward
 > --add/-a with 2 args then with --reward/-r argument
 ```bash
 python todo.py -a/--add [reward][bounty] -r/--reward
 ```

###2.Print tasks/ rewards
 > How to go about printing/getting task, by tag, by folders etc.

- Print All Tasks.

 > --get/-g with no arguments.
 ```bash
 python todo.py -g/--get
 ```

  __Format of the Output__: Output of all get commands is displayed in certain way so you get to the todo you want fast. Basic format is like this:
  ```bash
  [name]:[bounty]:[task][optional tick sign]
  ```
  __name__: this and crucial and important field, this is unique to each task. This is field that you can use to communicate to the system about which task are you talking about. System ensures that its easy to type.

  __bounty__: This is heart and soul of our gamified todo listing app. You can assign different bounty to each task to convey its importance/ or its rewards.[Priority lists are in development.]

  __task__: string describing what needs to be done.

  __optional tick sign__: appears only to indicate if something is completed or not.

  example:
  ```bash
  todo395 : 90 : Coffee With Lara
  ```
  name = todo395<br/>
  bounty = 90<br/>
  task = Coffee with Lara <br/>

- Print tasks by name.
 > --get/-g with one argument that is name of the todo.
 ```bash
 python todo.py -g/--get task_name
 ```

- Print tasks by tags.
 > --get/-g with --tag/-t with one or more arguments.
 ```bash
 python todo.py -g/--get -t/--tag tag [tag...]
 ```

__Note__: atleast one argument must be specified to for above to filter by tag.

- Print tasks by folder.
 > --get/-g with --folder/-f with one argument that is foldername
 ```bash
 python todo.py -g/--get -f/--folder foldername
 ```

- Print tasks filtered by both folder and tags.
 > --get/-g with --folder/-f with one argument that is the foldername, and --tag/-t with one or more arguments which are filtering tags.
 ```bash
 python todo.py -g/--get -f/--folder foldername -t/--tag tag [tag...]
 ```

- Print All Rewards.
 > --get/-g with --reward/-r
 ```bash
 python todo.py -g/--get -r/--reward
 ```

 __Format of the Reward Output__: Output of all get commands is displayed in certain way so you get to the todo you want fast. Basic format is like this:
 ```bash
 [name]:[bounty_req]:[reward]->[Redeemed n times]
 ```
 __name__: unique name for each reward. this is how the system knows about this rewards' existense.

 __bounty_req__: Minimum bounty required to redeem this reward.

 __reward__: text describing the reward.

 __redeemed times__: indicates how many times this particular reward has been redeemed in the past.

 example:
 ```bash
 rw367 : 5 : 15 mins break -> redeemed 5 times
 ```
 name = rw367<br/>
 bounty_req = 5<br/>
 reward = 15 mins break<br/>
 redeemed_times = redeemed 5 times<br/>

- Print Reward by name.
 > --get/-g with --reward/-r with reward_name argument.
 ```bash
 python todo.py -g/--get -r/--reward reward_name
 ```

### Features (TODO)
- Assigning to the other people.
- Offline Support
- Team project Management.
- Wiki Help.
- Testing.
- User Accounts
- Team Accounts.
- Quadant System for Task Management.
- Task Search.




Many of the cool stuff coming soon. (Airbase.IO)

&copy; 2015 Airbase
