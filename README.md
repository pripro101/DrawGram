# DrawGram
Programming But Drawing???!!

DrawGram User Manual
1. Introduction
DrawGram is a unique programming tool that converts 2D drawings into executable code. By drawing shapes, colors, and special symbols on the DrawGram canvas, you create commands in Python, Java, or Linux shell languages.

This manual will guide you through installation, usage, command mappings, and practical drawing examples.

2. System Requirements
Windows, Linux, or Mac (Linux or WSL recommended for best experience)

Python 3.7+ installed

Required Python packages: PyQt5, PIL (Pillow), OpenCV, numpy

Basic command line knowledge

3. Installation
On Windows (Using WSL):
Open Microsoft Store and search for Ubuntu.

Install Ubuntu and launch it.

Create your Linux user profile.

Run the following commands inside Ubuntu terminal:

bash
Copy
Edit
sudo apt update && sudo apt upgrade -y
sudo apt install git python3 python3-pip -y
git clone https://github.com/pripro101/DrawGram
cd DrawGram
python3 drawgramlivepyth5.py
Now you can start DrawGramming!

On Linux:
bash
Copy
Edit
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
git clone https://github.com/pripro101/DrawGram
cd DrawGram
python3 drawgramlivepyth5.py
4. Running DrawGram
Launch the program with Python.

A loading screen with the DrawGram logo appears.

After loading, the drawing board opens.

Use the palette on the bottom to select colors.

Draw on the canvas with the mouse.

Use buttons for Erase, Clear Drawing, or Run DrawGram.

5. User Interface
Canvas: Large white area to draw your commands.

Color Palette: Up to 50 color buttons representing your command colors (shown as @0000, @0001, etc.).

Buttons:

Erase: Draw in white (erase).

Clear Drawing: Clears all drawing.

Run DrawGram: Saves the drawing and interprets it into code shown next to the canvas.

6. How to Draw Commands
DrawGram interprets your drawing by detecting:

Symbols that trigger language modes:

! → Python mode

^ → Java mode

) → Linux shell mode

Shapes mapped to code structures:

Circle → Functions, calls

Square → Control structures (if, loops)

Triangle → Loops or conditions

Star → Return or special keywords

Colors matched to a palette of 1500+ colors, each color code like @0000, @0001, ..., linked to specific commands.

7. Color Palette Convention
Colors are saved in folder coloursdrawgram as color_0.png to color_1499.png.

Each color corresponds to a code command.

Colors shown in UI palette as buttons; their code is printed as @0000, @0001, etc.

8. Command Mappings
Language	Symbol	Shape	Color Code	Command / Meaning
Python	!	Circle	@0000	def (function definition)
Circle	@0001	print()
Square	@0002	if statement
Triangle	@0003	for loop
Circle	@0004	import
Star	@0005	return
Java	^	Circle	@0000	public or def equivalent
Circle	@0001	System.out.println()
Square	@0002	if statement
Triangle	@0003	for loop
Circle	@0004	import
Star	@0005	return
Linux Shell	)	Square	@0000	sudo
Circle	@0001	echo
Square	@0002	test / condition
Triangle	@0003	for loop
Circle	@0004	apt commands (update/install)
Star	@0005	exit / return

9. Running Your Drawn Code
Click Run DrawGram to:

Save the drawing as drawing_capture.png.

Interpret shapes/colors/symbols into commands.

Display the generated code next to the canvas.

10. Examples of DrawGram Drawings and Commands
10.1 Python Example — Print Hello
Draw symbol: ! (Python mode)

Draw a red circle (@0001)

Output:

python
Copy
Edit
print('Hello from DrawGram!')
10.2 Java Example — Print Hello
Draw symbol: ^ (Java mode)

Draw a red circle (@0001)

Output:

java
Copy
Edit
System.out.println("Hello from DrawGram!");
10.3 Linux Example — List Directory
Draw symbol: ) (Linux mode)

Draw a circle with color representing ls -la (@0001)

Output:

bash
Copy
Edit
ls -la
pwd
10.4 Python Function and If Statement
Draw ! symbol

Draw black circle (@0000) for def

Draw green square (@0002) for if

Output:

python
Copy
Edit
def my_function():
    if condition:
        pass
10.5 Linux Update Commands
Draw ) symbol

Draw colors representing commands sudo apt update and sudo apt upgrade -y

Output:

bash
Copy
Edit
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-pyqt5 python3-pil python3-opencv
11. Tips and Tricks
Start every new code block by drawing the mode symbol (!, ^, or )).

Use simple shapes with specific colors for clarity.

Limit palette size per drawing to avoid UI lag.

Combine shapes/colors to express complex commands.

Save drawings often.

Use erase and clear buttons to adjust your work.

12. Troubleshooting
If colors do not appear, run generate_colours_palette() again.

If packages are missing, use install_python_packages() or manually pip install.

For errors in running Linux commands, check your terminal or sudo rights.

If drawing interpretation looks wrong, check if correct symbols and shapes were used.

13. Future Extensions
Expand palette beyond 1500 colors.

Add more shapes for control flow and data structures.

Integrate output saving to files or direct code execution.

Improve AI-based shape and symbol recognition.

14. Contact and Support
GitHub: https://github.com/pripro101/DrawGram

Issues: Use GitHub Issues page for bug reports or feature requests.

Email: priprothezpro101@gmail.com

Enjoy creating code by drawing with DrawGram!
Turn your creativity into real programs visually.

