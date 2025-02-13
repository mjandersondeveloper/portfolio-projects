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
#include <cstdlib>
#include <string>
#include <unistd.h>

#include "Utils.h"

State getState(int num, std::string type) {
  if (type == "branch") {
   if (num == 0) {
      return State::BranchFalse;
    } else {
        return State::BranchTrue;
    }
  } else {
    if (num == 0) {
      return State::ReturnZero;
    } else if (num > 0) {
      return State::ReturnPos;
    } else {
      return State::ReturnNeg;
    }
  }
}

std::vector<std::string> getElements(std::string s, char delim, bool newline) {
  std::stringstream ss(newline ? readOneFile(s) : s);
  std::vector<std::string> elems;
  std::string item;
  while (std::getline(ss, item, delim)) {
    elems.push_back(item);
  }
  return elems;
}

void countSuccessAndFailurePredicates() {
// Set S(P)
  for (auto s : SuccessLogs) {
    for (auto x : getElements(s, '\n', true)) {
      std::vector<std::string> succs = getElements(x, ',', false);    
      std::tuple <int, int, State> succKey(std::stoi(succs[1]), std::stoi(succs[2]), getState(std::stoi(succs[3]), succs[0]));

      if (S.find(succKey) == S.end()) {
        S[succKey] = 1;
      } else {
        S[succKey]++;
      }
    }
  }

  // Set F(P)
  for (auto f : FailureLogs) {
    for (auto y : getElements(f, '\n', true)) {
      std::vector<std::string> fails = getElements(y, ',', false);    
      std::tuple <int, int, State> failKey(std::stoi(fails[1]), std::stoi(fails[2]), getState(std::stoi(fails[3]), fails[0]));

      if (F.find(failKey) == F.end()) {
        F[failKey] = 1;
      } else {
        F[failKey]++;
      }
    }
  }
}

void calculateFailure(std::map<std::tuple<int, int, State>, double> SP, std::map<std::tuple<int, int, State>, double> FP) {
  for (auto f : FP) {
    if (SP.find(f.first) == SP.end()) {
      Failure[f.first] = 1;
    } else {
      for (auto s : SP) {
        if (s.first == f.first) {
          double divisor = f.second + s.second;
          if (divisor == 0) {
            Failure[f.first] = 0;
          } else {
            Failure[f.first] = f.second / divisor;
          }
        }
      }
    }
  }
}

void populateObservedPredicates(std::map<std::tuple<int, int, State>, double> SP, std::map<std::tuple<int, int, State>, double> FP) {
  // Set SObs(P)
  for (auto s : SP) {        
    SObs[s.first] = s.second;
    State succState = std::get<2>(s.first);
    if (succState == State::BranchTrue || succState == State::BranchFalse) {
      std::tuple <int, int, State> succBranch(std::get<0>(s.first), std::get<1>(s.first), State::BranchTrue);
      std::tuple <int, int, State> failBranch(std::get<0>(s.first), std::get<1>(s.first), State::BranchFalse);
      if (SP.find(succBranch) == SP.end()) {
        SObs[succBranch] = 0;
      } else if (SP.find(failBranch) == SP.end()) {
        SObs[failBranch] = 0;
      } 
    } else {
      std::tuple <int, int, State> zeroBranch(std::get<0>(s.first), std::get<1>(s.first), State::ReturnZero);
      std::tuple <int, int, State> posBranch(std::get<0>(s.first), std::get<1>(s.first), State::ReturnPos);
      std::tuple <int, int, State> negBranch(std::get<0>(s.first), std::get<1>(s.first), State::ReturnNeg);
      if (SP.find(zeroBranch) == SP.end()) {
        SObs[zeroBranch] = 0;
      } else if (SP.find(posBranch) == SP.end()) {
        SObs[posBranch] = 0;
      } else if (SP.find(negBranch) == SP.end()) {
        SObs[negBranch] = 0;
      }
    }
  }

  // Set FObs(P)
  for (auto f : FP) {        
    FObs[f.first] = f.second;
    State failState = std::get<2>(f.first);
    if (failState == State::BranchTrue || failState == State::BranchFalse) {
      std::tuple <int, int, State> succBranch(std::get<0>(f.first), std::get<1>(f.first), State::BranchTrue);
      std::tuple <int, int, State> failBranch(std::get<0>(f.first), std::get<1>(f.first), State::BranchFalse);
      if (FP.find(succBranch) == FP.end()) {
        FObs[succBranch] = 0;
      } else if (FP.find(failBranch) == FP.end()) {
        FObs[failBranch] = 0;
      } 
    } else {
      std::tuple <int, int, State> zeroBranch(std::get<0>(f.first), std::get<1>(f.first), State::ReturnZero);
      std::tuple <int, int, State> posBranch(std::get<0>(f.first), std::get<1>(f.first), State::ReturnPos);
      std::tuple <int, int, State> negBranch(std::get<0>(f.first), std::get<1>(f.first), State::ReturnNeg);
      if (FP.find(zeroBranch) == FP.end()) {
        FObs[zeroBranch] = 0;
      } else if (FP.find(posBranch) == FP.end()) {
        FObs[posBranch] = 0;
      } else if (FP.find(negBranch) == FP.end()) {
        FObs[negBranch] = 0;
      }
    }
  }
}
    
void calculateContext(std::map<std::tuple<int, int, State>, double> succObs, std::map<std::tuple<int, int, State>, double> failObs) {
  for (auto sO : succObs) {
    if (failObs.find(sO.first) != failObs.end() && Context.find(sO.first) == Context.end()) {
      State obsState = std::get<2>(sO.first);
      if (obsState == State::BranchTrue || obsState == State::BranchFalse) {
        std::tuple <int, int, State> succBranch(std::get<0>(sO.first), std::get<1>(sO.first), State::BranchTrue);
        std::tuple <int, int, State> failBranch(std::get<0>(sO.first), std::get<1>(sO.first), State::BranchFalse);
        double branchSOb = SObs[succBranch] + SObs[failBranch];
        double branchFOb = FObs[succBranch] + FObs[failBranch];
        double divisor = branchFOb + branchSOb;
        
        if (divisor == 0) {
          Context[succBranch] = Context[failBranch] = 0;
        } else {
          Context[succBranch] = Context[failBranch]  = branchFOb / divisor;
        }
      } else {
        std::tuple <int, int, State> zeroBranch(std::get<0>(sO.first), std::get<1>(sO.first), State::ReturnZero);
        std::tuple <int, int, State> posBranch(std::get<0>(sO.first), std::get<1>(sO.first), State::ReturnPos);
        std::tuple <int, int, State> negBranch(std::get<0>(sO.first), std::get<1>(sO.first), State::ReturnNeg);
        double returnSOb = SObs[zeroBranch] + SObs[posBranch] + SObs[negBranch];
        double returnFOb = FObs[zeroBranch] + FObs[posBranch] + FObs[negBranch];
        double divisor = returnSOb + returnFOb;
        
        if (divisor == 0) {
          Context[zeroBranch] = Context[posBranch] = Context[negBranch] = 0;
        } else {
          Context[zeroBranch] = Context[posBranch] = Context[negBranch] = returnFOb / divisor;
        }
      }
    }
  }
}

void calculateIncrease() {
  for (auto context : Context) {
    if (Failure.find(context.first) == Failure.end()) {
      Increase[context.first] = 0 - context.second;
    } else {
      Increase[context.first] = Failure[context.first] - context.second;
    }
  }
}

/*
 * Implement your CBI report generator.
 */
void generateReport() { 
  /* Add your code here */
  
  // Set S(P) and F(P)
  countSuccessAndFailurePredicates();

  // Calclate Failure(P)
  calculateFailure(S, F);

  // Set-up Observables
  populateObservedPredicates(S, F);
 
  // Calculate Context(P)
  calculateContext(SObs, FObs);

  // Calculate Increase(P)
  calculateIncrease();
}

// ./CBI [exe file] [fuzzer output dir]
int main(int argc, char **argv) {
  if (argc != 3) {
    fprintf(stderr, "Invalid usage\n");
    return 1;
  }

  struct stat Buffer;
  if (stat(argv[1], &Buffer)) {
    fprintf(stderr, "%s not found\n", argv[1]);
    return 1;
  }

  if (stat(argv[2], &Buffer)) {
    fprintf(stderr, "%s not found\n", argv[2]);
    return 1;
  }

  std::string Target(argv[1]);
  std::string OutDir(argv[2]);

  generateLogFiles(Target, OutDir);
  generateReport();
  printReport();
  return 0;
}
