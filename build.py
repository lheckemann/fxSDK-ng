#!/usr/bin/python

import os
import subprocess

class UserQuit(Exception):
  pass

class AutoQuit(Exception):
  pass

def getyn():
  ans = raw_input("[ynq] ").lower().strip()
  while ans not in ('y', 'n', 'q'):
    ans = raw_input("Please enter [y]es, [n]o or [q]uit. ").lower().strip()
  if ans == 'q':
    raise UserQuit()
  return ans == 'y'    

def main():
  print "WARNING! This script may not work! It's a mockup for a possible build process, but I'm not sure I'm going to keep it."
  print "Proceed?"
  if not getyn():
    raise UserQuit()
  print

  print "Hi! It would seem that you want to build fxSDK-ng! That's lovely. Let's get down to business, shall we?"
  print "Answer q or press Ctrl-C at any time to abort."
  print "Are you following my tutorial, OR do you know what you are doing?"
  if not getyn():
    print "Please follow my tutorial at https://github.com/Anonymooseable/fxSDK-ng/ . :)"
    raise AutoQuit()
  print "Have you already built a GCC toolchain for the SH3 architecture (required for compiling the library)?"
  if getyn():
    toolchain_path = raw_input("Where is it located? (default for crosstool-ng is $HOME/x-tools/tuple where tuple is sh3eb-casio-elf if you're following my instructions)")
    while not os.path.isdir(os.path.join(toolchain_path, "bin")):
      toolchain_path = raw_input("That path does not seem to contain a directory named 'bin'. Please enter another (or type 'q' to quit): ")
      if toolchain_path == 'q':
        raise UserQuit()
    target_tuple = raw_input("Please enter the tuple used to prefix the toolchain exectuables (sh3eb-casio-elf if you're following my tutorials)")
    while not os.path.isfile(os.path.join(toolchain_path, "bin", target_tuple+"-gcc")):
      target_tuple = raw_input("Could not find gcc (expected to be found under the name %s at %s). Please enter the correct tuple (or 'q' to quit): " % (target_tuple + "-gcc", os.path.join(toolchain_path, "bin")))
      if target_tuple == 'q':
        raise UserQuit()
    install_to = raw_input("Where do you want to install the tools to? ")
    success = False
    while not success:
      if install_to == 'q':
        raise UserQuit()
      try:
        os.makedirs(install_to)
      except OSError:
        install_to = raw_input("Could not create the destination directory. Please try entering a new one. ")
      else:
        success = True
    print "OK, ready for building! Are you?"
    if getyn():
      os.mkdir("build")
      os.chdir("build")
      cmake_tools = subprocess.Popen(('cmake', '-DCMAKE_INSTALL_PREFIX=%s' % install_to, '..'))
      os.chdir("..")
      os.chdir("libfxsys")
      os.mkdir("build")
      os.chdir("build")
      cmake_lib = subprocess.Popen(('cmake', '-DCMAKE_INSTALL_PREFIX=%s' % toolchain_path, '-DSH3_TOOLCHAIN_ROOT=%s' % toolchain_path, '-DSH3_TOOLCHAIN_TUPLE=%s' % target_tuple, '..'))
      
      ret_tools = cmake_tools.wait()
      ret_lib = cmake_lib.wait()
      fail = False
      if ret_tools != 0:
        print "Could not run cmake for the tools."
        fail = True
      if ret_lib != 0:
        print "Could not run cmake for the library."
        fail = True
      if fail:
        raise Exception("Compilation preparation failed.")
      
      os.chdir(os.path.join("..", ".."))
      build_tools = subprocess.Popen(('make', 'install'))
      os.chdir("libfxsys")
      os.chdir("build")
      build_lib = subprocess.Popen(('make', 'install'))
      ret_tools = build_tools.wait()
      ret_lib = build_lib.wait()
      if ret_tools != 0:
        print "Could not compile the tools."
        fail = True
      if ret_lib != 0:
        print "Could not compile the library."
        fail = True
      if fail:
        raise Exception("Compilation failed.")
        
  else:
    print "Please build a toolchain. Instructions can be found at https://github.com/Anonymooseable/fxSDK-ng/"
    
if __name__ == "__main__":
  try:
    main()
  except UserQuit:
    print "Bye!"
  except AutoQuit:
    pass
  except KeyboardInterrupt:
    pass
