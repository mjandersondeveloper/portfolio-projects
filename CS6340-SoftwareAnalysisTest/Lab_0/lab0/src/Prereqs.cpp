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

#include "Prereqs.h"

using namespace llvm;

namespace prereqs
{

  bool Prereqs::runOnModule(Module &M)
  {
    int numOfFunctions = 0;
    int numOfInstructions = 0;
    int numOfSDivInstructions = 0;

    /* TODO Add your code here */
    for (auto &F : M) {
      numOfFunctions++;
      for (auto &B : F) {
        for (auto &I : B) {
          numOfInstructions++;
          if(I.getOpcode() == I.SDiv) { numOfSDivInstructions++; }
        }
      }     
    }
    /* DO NOT EDIT BELOW THIS LINE */
    print_module_info(M.getName(),
                      numOfFunctions,
                      numOfInstructions,
                      numOfSDivInstructions);
    return false;
  }

} // namespace prereqs
