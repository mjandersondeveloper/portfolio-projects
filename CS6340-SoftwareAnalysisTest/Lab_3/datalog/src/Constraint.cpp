/*
 * Copyright Â© 2021 Georgia Institute of Technology (Georgia Tech). All Rights Reserved.
 * Template code for CS 6340 Software Analysis
 * Instructors: Mayur Naik and Chris Poch
 * Head TAs: Kelly Parks and Joel Cooper
 *
 * Georgia Tech asserts copyright ownership of this template and all derivative
 * works, including solutions to the projects assigned in this course. Students
 * and other users of this template code are advised not to share it with others
 * or to make it available on publicly viewable websites including repositories
 * such as GitHub and GitLab. This copyright statement should not be removed
 * or edited. Removing it will be considered an academic integrity issue.
 *
 * We do grant permission to share solutions privately with non-students such
 * as potential employers as long as this header remains in full. However, 
 * sharing with other current or future students or using a medium to share
 * where the code is widely available on the internet is prohibited and 
 * subject to being investigated as a GT honor code violation.
 * Please respect the intellectual ownership of the course materials 
 * (including exam keys, project requirements, etc.) and do not distribute them 
 * to anyone not enrolled in the class. Use of any previous semester course 
 * materials, such as tests, quizzes, homework, projects, videos, and any other 
 * coursework, is prohibited in this course. */
#include "llvm/IR/InstIterator.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/SourceMgr.h"
#include <fstream>
#include "llvm/AsmParser/Parser.h"
#include "llvm/IRReader/IRReader.h"
#include "Extractor.h"

using namespace llvm;

void exitWithUsage() {
  std::cerr << "Usage: constraint <-ReachDef|-Liveness> [--debug] <filename.bc>" << std::endl;
  exit(1);
}

int main(int argc, char **argv) {
  if (argc < 3 || argc > 4) {
    exitWithUsage();
  }

  std::string ModeString;

  Extractor::AnalysisMode Mode;
  if (!strcmp("-ReachDef", argv[1])) {
    Mode = Extractor::AnalysisMode::ReachDef;
    ModeString = "ReachDef";
  }
  else if (!strcmp("-Liveness", argv[1])) {
    Mode = Extractor::AnalysisMode::Liveness;
    ModeString = "Liveness Analysis";
  }
  else {
    exitWithUsage();
  }
  
  int FilenameAtIndex = 2;
  bool verbose = false;
  if (argc == 4 && !strcmp(argv[2], "--debug")) {
    verbose = true;
    FilenameAtIndex = 3;
  }
  else if (argc == 4 && strcmp(argv[3], "--debug")) {
    exitWithUsage();
  }

  LLVMContext Context;
  SMDiagnostic Err;
  StringRef FileName(argv[FilenameAtIndex]);

  std::unique_ptr<Module> Mod = parseIRFile(FileName, Err, Context);

  if (!Mod) {
    Err.print(argv[0], errs());
    return 1;
  }

  // matches lab2
  std::cout << "Running " << ModeString << " on main" << std::endl;

  /**
   * Set up an Extractor. You will set up the neccessary Z3 rules for reaching definitions
   * in Extractor.initialize().
   */
  Extractor Ext;
  Ext.initialize(Mode);
  z3::fixedpoint *Solver = Ext.getSolver();
  z3::context &C = Ext.getContext();

  /**
   * Map every instruction to an auto-incrementing integer ID, stored in InstMap.
   * All Z3 constraints about Instructions will be expressed with these IDs.
   */
  InstMapTy InstMap;
  unsigned int Counter = 0;
  std::vector<Value *> OrderSeen;
  for (auto &F : *Mod) {
    for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E; I++) {
      InstMap[&*I] = Counter++;
      OrderSeen.push_back(&*I);
    }
  }

  /**
   * Create Z3 facts about each instruction. You will populate several input relations based on what you
   * can determine about Instructions. You will implement that in Extractor.extractConstraints().
   */
  for (auto &F : *Mod) {
    for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E; I++) {
      Ext.extractConstraints(InstMap, &*I, Mode);
    }
  }

  
  Ext.print(InstMap, verbose, OrderSeen);
}
