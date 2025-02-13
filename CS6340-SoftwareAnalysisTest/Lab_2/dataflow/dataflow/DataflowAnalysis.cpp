#include "DataflowAnalysis.h"

using namespace llvm;

namespace dataflow {
    DataflowAnalysis::DataflowAnalysis(char ID) : FunctionPass(ID){}
    
    bool DataflowAnalysis::runOnFunction(Function &F){
        errs() << "Running " << getAnalysisName() << " on " << F.getName() << "\n";
        for (inst_iterator I = inst_begin(F), E= inst_end(F); I != E; ++I){
            inMap[&(*I)] = new SetVector<Value*>;
            outMap[&(*I)] = new SetVector<Value*>;
        }
        
        doAnalysis(F);
        
        for (inst_iterator I = inst_begin(F), E= inst_end(F); I != E; ++I){
            errs() << "Instruction: " << *I << "\n";
            errs() << "In set: \n";
            SetVector<Value*>* inSet = inMap[&(*I)];
            errs() << "[";
            for(SetVector<Value*>::iterator V = inSet->begin(), VE = inSet->end(); V != VE; ++V){
                errs() << **V << "; ";
            }
            errs() << "]\n";
            errs() << "Out set: \n";
            SetVector<Value*>* outSet = outMap[&(*I)];
            errs() << "[";
            for(SetVector<Value*>::iterator V = outSet->begin(), VE = outSet->end(); V != VE; ++V){
                errs() << **V << "; ";
            }
            errs() << "]\n";
            errs() << "\n";
        }
        
        for (inst_iterator I = inst_begin(F), E= inst_end(F); I != E; ++I){
            delete inMap[&(*I)];
            delete outMap[&(*I)];
        }
        return false;
    }
}
