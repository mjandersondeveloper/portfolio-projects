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
#include "CBIInstrument.h"

using namespace llvm;

namespace instrument {

static const char *CBIBranchFunctionName = "__cbi_branch__";
static const char *CBIReturnFunctionName = "__cbi_return__";

/*
 * Implement instrumentation for the branch scheme of CBI.
 */
void instrumentCBIBranches(Module *M, Function &F, BranchInst &I) {
  /* Add your code here */
  std::vector<Value*> params;
  if (I.isConditional()) {
    // Source: https://stackoverflow.com/questions/63842936/converting-i1-type-to-integer-value
    IRBuilder<> irbuilder(&I);
    Value* condition = irbuilder.CreateIntCast(I.getCondition(), Type::getInt32Ty(M->getContext()), false);
  
    Instruction* debugInst = dyn_cast<Instruction>(&I);
    DebugLoc debug = debugInst->getDebugLoc();

    if (debug && condition) {
      Constant* lineNum = ConstantInt::get(IntegerType::get(F.getContext(),32), debug.getLine());
      Constant* colNum = ConstantInt::get(IntegerType::get(F.getContext(),32), debug.getCol());

      params.push_back(lineNum);
      params.push_back(colNum);
      params.push_back(condition);

      Constant* cbi_branch = M->getOrInsertFunction(CBIBranchFunctionName, Type::getVoidTy(M->getContext()), IntegerType::get(M->getContext(), 32), IntegerType::get(M->getContext(), 32), IntegerType::get(M->getContext(), 32));
      Function* cbiBranchFunc = cast<Function>(cbi_branch);
      CallInst::Create(cbiBranchFunc, params, "", &I);
    }
  }
}

/*
 * Implement instrumentation for the return scheme of CBI.
 */
void instrumentCBIReturns(Module *M, Function &F, CallInst &I) {
  /* Add your code here */
  std::vector<Value*> params;
  
  Instruction* debugInst = dyn_cast<Instruction>(&I);
  DebugLoc debug = debugInst->getDebugLoc();

  if (debug) {
    Constant* lineNum = ConstantInt::get(IntegerType::get(F.getContext(),32), debug.getLine());
    Constant* colNum = ConstantInt::get(IntegerType::get(F.getContext(),32), debug.getCol());

    params.push_back(lineNum);
    params.push_back(colNum);
    params.push_back(&I);

    Constant* cbi_return = M->getOrInsertFunction(CBIReturnFunctionName, Type::getVoidTy(M->getContext()), IntegerType::get(M->getContext(), 32), IntegerType::get(M->getContext(), 32), IntegerType::get(M->getContext(), 32));
    Function* cbiReturnFunc = cast<Function>(cbi_return);
    CallInst::Create(cbiReturnFunc, params, "", I.getNextNonDebugInstruction());
  }
}

bool CBIInstrument::runOnFunction(Function &F) {
  /* Add your code here */
   for (auto &B : F) {    
    for (auto &I : B) {
      if (isa<BranchInst>(I)) {
        BranchInst* branchInst = dyn_cast<BranchInst>(&I);
        instrumentCBIBranches(F.getParent(),F,*branchInst);
      } 
      if (isa<CallInst>(I) && I.getType()->isIntegerTy(32)) {
        CallInst* callInst = dyn_cast<CallInst>(&I);
        instrumentCBIReturns(F.getParent(),F,*callInst);
      }
    }    
  } 
  return true;
}

char CBIInstrument::ID = 1;
static RegisterPass<CBIInstrument> X("CBIInstrument",
                                     "Instrumentations for CBI", false, false);

} // namespace instrument
