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

/* Note: this file is not submitted; if you need additional
 * includes, please do so in your ../src/Prereqs.cpp file.
 */
#include "llvm/IR/Module.h"

using namespace llvm;

namespace prereqs {

struct Prereqs : public ModulePass {
  static char ID;
  Prereqs();

  bool runOnModule(Module &M);
  void print_module_info(std::string moduleName,
                         int numOfFunctions,
                         int numOfInstructions,
                         int numOfSDivInstructions);
};

Prereqs::Prereqs() : ModulePass(ID) {}
char Prereqs::ID = 1;
static RegisterPass<Prereqs> X("Prereqs", "Prereqs", false, false);

void Prereqs::print_module_info(std::string moduleName,
                                int numOfFunctions,
                                int numOfInstructions,
                                int numOfSDivInstructions) {
  outs() << "Analytics of Module " << moduleName
         << "\n  # Functions    : " << numOfFunctions
         << "\n  # Instructions : " << numOfInstructions
         << "\n  # Signed Division Instructions : " << numOfSDivInstructions << "\n";
}

} // namespace prereqs

