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

#include "Instrument.h"

using namespace llvm;

namespace instrument {
static const char *SanitizerFunctionName = "__dbz_sanitizer__";
static const char *CoverageFunctionName = "__coverage__";

/*
 * Implement divide-by-zero sanitizer.
 */
void instrumentSanitizer(Module *M, Function &F, Instruction &I) {
  /* Add your code here */ 
  std::vector<Value *> params;
  BinaryOperator* divInst = dyn_cast<BinaryOperator>(&I);
  if (divInst) {
    Value* denomValue = divInst->getOperand(1);
    Instruction* debugInst = dyn_cast<Instruction>(&I);
    DebugLoc debug = debugInst->getDebugLoc();
    if (debug) {
      Constant* lineNum = ConstantInt::get(IntegerType::get(F.getContext(),32), debug.getLine());
      Constant* colNum = ConstantInt::get(IntegerType::get(F.getContext(),32), debug.getCol());
      params.push_back(denomValue);
      params.push_back(lineNum);
      params.push_back(colNum);

      Constant* dbz_san = M->getOrInsertFunction(SanitizerFunctionName, Type::getVoidTy(M->getContext()), IntegerType::get(M->getContext(), 32), IntegerType::get(M->getContext(), 32), IntegerType::get(M->getContext(), 32));
      Function* sanFunc = cast<Function>(dbz_san);
      CallInst::Create(sanFunc, params, "", &I);
    }
  }
}

/*
 * Implement code coverage instrumentation.
 */

void instrumentCoverage(Module *M, Function &F, Instruction &I) {
  /* Add your code here */
  std::vector<Value *> params;
  Instruction* debugInst = dyn_cast<Instruction>(&I);
  DebugLoc debug = debugInst->getDebugLoc();
  if(debug) {
    Constant* lineNum = ConstantInt::get(IntegerType::get(F.getContext(),32), debug.getLine());
    Constant* colNum = ConstantInt::get(IntegerType::get(F.getContext(),32), debug.getCol());
    params.push_back(lineNum);
    params.push_back(colNum); 

    Constant* coverage = M->getOrInsertFunction(CoverageFunctionName, Type::getVoidTy(M->getContext()), IntegerType::get(M->getContext(), 32), IntegerType::get(M->getContext(), 32));
    Function* covFunc = cast<Function>(coverage);
    CallInst::Create(covFunc, params, "", &I);
  }
}

bool Instrument::runOnFunction(Function &F) {
  /* Add your code here */
  for (auto &B : F) {    
    for (auto &I : B) {
      if (I.getOpcode() == I.SDiv || I.getOpcode() == I.UDiv) {
          instrumentSanitizer(F.getParent(),F,I);
      }
      instrumentCoverage(F.getParent(),F,I);
    }    
  } 
  return true;
}

char Instrument::ID = 1;
static RegisterPass<Instrument>
    X("Instrument", "Instrumentations for Dynamic Analysis", false, false);
} // namespace instrument