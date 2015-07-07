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

### 1.Add a Todo/ Reward.
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

### 2.Print tasks/ rewards
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

### 3. Editing Todos.
 - Edit a todo
 > --edit/-e with one argument that is the name of the todo to be edited.
 ```bash
 python todo.py -e/--edit name
 ```
 
 - Move to different folder
 > --edit/-e with one argument that is the name of the todo to be edited and --folder/-f 
 with one argument that is the name of the destination folder.
 ```bash
 python todo.py -e/--edit name -f/--folder foldername
 ```
 
### 4. Snoozing a Task.
 > --snooze with two argument, first is the todo name and second one is the snooze string(due time String).
 ```bash
 python todo.py --snooze name duetime_string
 ``` 
 
 __Duetime Strings__: They form an integral part of how we represent due times in more human ways in our system.
 like you can write "+9h" as duetime_string if something is due in 9 hours. or you can use combination of duetime strings
 to represent more complex due time, like for example, "+3w-2d+7h-20M" means 3 weeks ahead, then 2 days behind, then 7 hours ahead, and
 finally -20 minutes behind. We also accept dates so you don't have to calculate time delta if you already have the due dates.
 
 - Duetime string should either be a date string of the format "YYYY-mm-dd"(eg. 2015-07-05) or our own duetime strings like "+9h" or "+60M"
 - Duetime string should either start with "+" or "-". "+" stands for ahead in time and "-" stands for behind in time.
 - eg. duetimestring should have final time_classifier like "h", "m" etc to signify units of time.
 - Acccepted time Units are:
    * M - minutes.
    * h - hours.
    * d - days
    * w - weeks (7 days)
    * m - months (30 days)
    * y - years (365 days)

### 5. Deleting a todo/ reward/ folder.
__NOTE__: Delete doesn't have short flag like "-d"("-d" is actually for marking something done.), Since delete is considered 
a dangerous operation. You can't get back anything that is deleted.

1. Deleting todos. (one or many)
  > --delete with one or more arguments that are names of todos to be deleted.
  ```bash
  python todo.py --delete todo [todo...]
  ```   

2. Deleting rewards( one or many)
  > --delete with one or more arguments that are name of rewards to be deleted, with --reward/-r command.
  ```bash
  python todo.py --delete reward [reward...] -r/--reward
  ```

3. Deleteting a folder.
  > --delete wth one argument that is the name of the folder to be deleted, with --folder/-f command.
  ```bash
  python todo.py --delete foldername -f/--folder
  ```

__NOTE__: You can't delete multiple folders in delete a folder command, and that is by design.

### 6. Marking a todo done.
 > -d/--done command with one or more arguments that are name of the todos that are to be marked done.
 ```bash
 python todo.py -d/--done todo [todo...]
 ```
 
 (* Done and delete command is also in works.)
 
### 7. Redeeming a Reward.
 > --redeem/-x command with one argument that is the name of the reward and second is optional times argument.
 ```bash
 python todo -x/--redeem reward [times]
 ```
 
 - By Default times will be 1. This "times" field is important to take smaller rewards multiple times, for eg. "15 minutes break" reward
 redeemed 3 times is actually 45 minutes break.
 
### 8. User Profile/Dashboard
- Viewing Dashboard/Profile
 > --me/-m command to view your profile/dashboard
 ```bash
 python todo.py -m/--me
 ```
 
- Updating Email and Name.( And other info in future)
 > --me/-m command with --editinfo command.
 ```bash
 python todo.py -m/--me --editinfo
 ```
 



### Features (TODO)
- Assigning to the other people.
- Offline Support
- Team project Management.
- Wiki Help.
- Testing.
- User Accounts
- Team Accounts.
- Quadant System for Task Management
- Task Search.




Many of the cool stuff coming soon. (Airbase.IO)

&copy; 2015 Airbase
