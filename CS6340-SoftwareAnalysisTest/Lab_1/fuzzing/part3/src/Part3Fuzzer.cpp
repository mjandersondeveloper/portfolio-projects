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
#include <iostream>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <cstdio>

#include "Mutate.h"
#include "Utils.h"

#include <time.h>

double currentTime;
double runtime = 0;
std::vector<std::string> coverage;

std::string CampaignToStr(Campaign &FuzzCamp) {
  switch (FuzzCamp) {
    case MutationA:
        return "MutationA";
    case MutationB:
        return "MutationB";
    case MutationC:
        return "MutationC";
  }
}

enum Campaign randomCampaign(int num) {
  switch (num) {
    default:
        return MutationA;
    case 1:
        return MutationB;
    case 2:
        return MutationC;
  }
}

std::string returnMutantAndCalculateExecutionTime(std::string origin,Campaign campaign) {
  // Source: https://www.geeksforgeeks.org/measure-execution-time-with-high-precision-in-c-c/
  clock_t start, end;
  start = clock();
  auto Mutant = mutate(origin, campaign);
  end = clock();
  double time_taken = double(end - start) / double(CLOCKS_PER_SEC);
  currentTime = time_taken;
  
  return Mutant;
}

bool isExecutionTimeLonger(Campaign campaign) {
  if (currentTime > runtime) {
    runtime = currentTime;
    return true;
  }
  return false;
}

bool isAdditionalCoverage(Campaign campaign, std::string target) {
  std::string coverageFile = target + ".cov";
  if(FILE *file = fopen(coverageFile.c_str(), "r")) {
    std::vector<std::string> currentCoverage;
    std::ifstream infile(coverageFile);
    std::string line;
    bool additionalCov = false;

    // Source: https://stackoverflow.com/questions/13035674/how-to-read-a-file-line-by-line-or-a-whole-text-file-at-once
    while (std::getline(infile, line)) {
      currentCoverage.push_back(line);
    }
    if (coverage.empty()) {
      coverage = currentCoverage;
      additionalCov = true;
    } else if (currentCoverage != coverage) {
      for (auto currentLine : currentCoverage) {
        if(std::find(coverage.begin(), coverage.end(), currentLine) != coverage.end()) {
          continue;
        } else {
          coverage.push_back(currentLine);
          additionalCov = true;
        }
      }
    }
    fclose(file);
    if (additionalCov) {
      return true;
    }
  }
  return false;  
}

/*
 * Implement your feedback-directed seed update algorithm.
 */
std::pair<std::string,Campaign> selectSeedAndCampaign(int num) {
  auto campaignNum = randomCampaign(num);
  std::string Seed = SeedInputs[campaignNum].back();
  Campaign FuzzCamp = campaignNum;
  return std::make_pair(Seed,FuzzCamp);
}

/*
 * Implement your feedback-directed seed update algorithm.
 */
void updateSeedInputs(std::string &Target, std::string &Mutated, Campaign &FuzzCamp, bool Success) {
  bool additionalCoverage = isAdditionalCoverage(FuzzCamp, Target);
  bool executionTime = isExecutionTimeLonger(FuzzCamp);
  
  if(Success && (additionalCoverage || executionTime)) {
    SeedInputs[FuzzCamp].push_back(Mutated);    
  }
}

int Freq = 1000;
int Count = 0;

bool test(std::string &Target, std::string &Input, Campaign &FuzzCamp, std::string &OutDir) {
  Count++;
  int ReturnCode = runTarget(Target, Input);
  switch (ReturnCode) {
  case 0:
    if (Count % Freq == 0)
      storePassingInput(Input, CampaignToStr(FuzzCamp), OutDir);
    return true;
  case 256:
    storeCrashingInput(Input, CampaignToStr(FuzzCamp), OutDir);
    fprintf(stderr, "%d crashes found\n", failureCount);
    return false;
  case 127:
    fprintf(stderr, "%s not found\n", Target.c_str());
    exit(1);
  }
}

// ./fuzzer [exe file] [seed input dir] [output dir]
int main(int argc, char **argv) { 
  if (argc < 4) { 
    printf("usage %s [exe file] [seed input dir] [output dir]\n", argv[0]);
    return 1;
  }

  srand(time(NULL));
  
  struct stat Buffer;
  if (stat(argv[1], &Buffer)) {
    fprintf(stderr, "%s not found\n", argv[1]);
    return 1;
  }

  if (stat(argv[2], &Buffer)) {
    fprintf(stderr, "%s not found\n", argv[2]);
    return 1;
  }

  if (stat(argv[3], &Buffer)) {
    fprintf(stderr, "%s not found\n", argv[3]);
    return 1;
  }

  if (argc >= 5) {
    Freq = strtol(argv[4], NULL, 10);
  }

  std::string Target(argv[1]);
  std::string SeedInputDir(argv[2]);
  std::string OutDir(argv[3]);

  initialize(OutDir);

  if (readSeedInputs(SeedInputDir)) {
    fprintf(stderr, "Cannot read seed input directory\n");
    return 1;
  }
  
  while (Count < maxTests && failureCount < maxCrashes) {
      // NOTE: You should feel free to manipulate this run loop 
      int randomCampaign = rand() % 3;
      if (Count % Freq == 0) {
        std::cerr << "Count is " << Count << std::endl;
      }
      std::pair<std::string,Campaign> SC = selectSeedAndCampaign(randomCampaign);
      auto Mutant = returnMutantAndCalculateExecutionTime(SC.first, SC.second);
      auto Success = test(Target, Mutant, SC.second, OutDir);
      updateSeedInputs(Target, Mutant, SC.second, Success);
  }
  return 0;
}
