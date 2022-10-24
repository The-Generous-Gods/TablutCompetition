# TablutCompetition
Software for the Tablut Students Competition

## Installation on Ubuntu/Debian 

From console, run these commands to install JDK 11 and ANT (the -y options enables is used to skip
the installation confirmation):

```
sudo apt update
sudo apt install default-jre -y
sudo apt install ant -y
```

Now, clone the project repository:

```
git clone https://github.com/AGalassi/TablutCompetition.git
```

## Run the Server without Eclipse

The easiest way is to utilize the ANT configuration script from console.
Go into the project folder (the folder with the `build.xml` file):
```
cd TablutCompetition/Tablut
```

Compile the project:

```
ant clean
ant compile
```

The compiled project is in  the `build` folder.
Run the server with:

```
ant server
```

Check the behaviour using the random players in two different console windows:

```
ant randomwhite

ant randomblack
```

At this point, a window with the game state should appear.

To be able to run other classes, change the `build.xml` file and re-compile everything


## Replay function

Used to replay a game using the logfile.

Firstly, generate the server.jar file by running

```
ant server-jar
```

Finally, you can run it as follows:

```
java -jar .\server.jar -g -R .\logs\[log_file_name].txt
```

Here, the -g option enables the GUI, and the -R option is for replaying a game with the log located in the specified path.

To check all the available options for ant server, a help text is displayed when you run

```
ant server
```

Also, if you want to find all the options available to run with ant, you can check the following file:

```
Tablut/build.xml
```
