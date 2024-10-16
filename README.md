In this project, our group customized a makergear M2 FDM printer into a 3 channel DIW printer with rotational nozzle functions.

![M2_DIW](https://github.com/user-attachments/assets/ed668f07-5c31-4076-995b-2c1e48d0c593)

The work in mainly done by Matthew Sorna from Architected Materials Lab at University of Pennsylvania.
Building on Matthew's work, I have been responsible for maintaining the machine and have made several improvements. Additionally, based on my own requirements, I modified another MakerGear M2 printer into a dual-channel DIW printer.

As the Makergear M2 printer serves as the foundation for this customization, its well-established Python API offers great convenience for us to control the printer using Python. Additionally, the main control board of the printer reserves several ports, allowing direct control of external electronic components through G-code. Based on these conditions, all external components in this customization are controlled via the printer's mainboard, without using other controllers such as Arduino, distinguishing it from the Aerotech project.

**Document Overview:**

**m2py:** A library that interacts with the printer using the Makergear Python API.

**m2pcs_marlin_firmware:** A customized version of Marlin firmware adapted to the modified printer hardware and components.

**movement_tool.py:** A user interface (UI) to directly control the printer's movement and pneumatic control.

**gcode_tool.py:** A UI that loads and executes G-code files for printing.

**rotate_test.py:** A Python script used for testing the rotational nozzle functionality.

**rotate_tensile_bar.py:** A script designed to print tensile bars using the rotational nozzle system.

**[User Guide]:** Documentation providing guidance on the customization process and instructions for usage.

**Sample Codes:** These include our commonly used printing cases, covering both direct printing through Python and G-code-based printing.
