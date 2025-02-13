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
#include "Mutate.h"

#include <cstring>
#include <map>

std::map<std::string, Campaign> to_campaign = 
  {{"MutationA", MutationA}, {"MutationB", MutationB}, {"MutationC", MutationC}};

bool toCampaign(std::string Str, Campaign& FuzzCampaign) {
  auto I = to_campaign.find(Str);
  if (I == to_campaign.end()) {
    fprintf(stderr, "\"%s\" not a valid fuzz campaign, choice options are: ", Str.c_str());
    for (auto &I2 : to_campaign) {
      fprintf(stderr, "%s ", I2.first.c_str());
    }
    fprintf(stderr, "\n");
    return false;
  }
  FuzzCampaign = I->second;
  return true;
}

/*
 * Implement your mutation algorithms.
 */
std::string mutateA(std::string Origin) {
  if (Origin.length() > 0) {
    int numberOfDeletions = rand() % Origin.length();
    for (int i = 0; i < numberOfDeletions; i++) {
      int position = rand() % Origin.length();
      Origin.erase(Origin.begin() + position); 
    }
  } 
  return Origin;
}

std::string mutateB(std::string Origin) {
  if(Origin.length() > 0) {
    for (int i = 0; i < Origin.length(); i++) {
      std::string c(1, Origin[i]);
      if(c == "\n") {
        Origin.erase(Origin.begin() + Origin[i]); 
      }
    }
    int position = rand() % Origin.length();
    Origin.insert(position,"\n");
  }
  return Origin;
}

std::string mutateC(std::string Origin) {
  if(Origin.length() > 0) {
    int numberOfSwaps = rand() % 50;
    for (int i = 0; i < numberOfSwaps; i++) {
      int swap1 = rand() % Origin.length();
      int swap2 = rand() % Origin.length();
      std::swap(Origin[swap1], Origin[swap2]);
    }
  }
  return Origin;
}

std::string mutate(std::string Origin, Campaign& FuzzCampaign) {
  std::string Mutant;
  switch (FuzzCampaign) {
    case MutationA:
        return mutateA(Origin);
    case MutationB:
        return mutateB(Origin);
    case MutationC:
        return mutateC(Origin);
  }
}