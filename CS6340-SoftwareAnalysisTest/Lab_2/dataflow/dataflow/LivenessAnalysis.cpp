#include "DataflowAnalysis.h"
namespace dataflow{
    struct LivenessAnalysis: public DataflowAnalysis{
        static char ID;
        LivenessAnalysis() : DataflowAnalysis(ID){}
    protected:
        /**
         *  Implement your analysis in this function. Store your results in DataflowAnalysis::inMap and
         *  DataflowAnalysis:outMap.
         */
        void doAnalysis(Function &F) override{
            // Source: http://www.cs.cornell.edu/courses/cs4120/2011fa/lectures/lec21-fa11.pdf
            SetVector<Instruction*>* nodes = getAllNodes(F);
            std::vector<Instruction*> changedNodes;
            // Put all nodes in changed set            
            changedNodes.assign(nodes->begin(), nodes->end());
            while(!changedNodes.empty()) {                
                // Get node
                Instruction* node = changedNodes.back();
                // Remove node n from changed set
                changedNodes.pop_back();
                // Calculate OUT[n] from successors' IN[s]
                std::vector<Instruction*> succs = getSuccessors(node);
                std::vector<Value*> succsVector;
                SetVector<Value*>* succsSet = new SetVector<Value*>;
                for(auto s : succs) {
                    succsVector.assign(inMap[s]->begin(), inMap[s]->end());
                }
                succsSet = convertToSetVector(succsVector);
                succsSet->insert(outMap[node]->begin(), outMap[node]->end());
                outMap[node] = succsSet;
                // Store original IN[n]
                std::vector<Value*> oldInVector;
                SetVector<Value*>* oldInSet = new SetVector<Value*>;
                oldInVector.assign(inMap[node]->begin(), inMap[node]->end());
                oldInSet = convertToSetVector(oldInVector);
                // Update OUT[n] with USE[n] U (OUT[n]-DEF[n])                            
                std::vector<Value*> tempOutVector;
                SetVector<Value*>* tempOutSet = new SetVector<Value*>;
                SetVector<Value*>* useSet = new SetVector<Value*>;
                tempOutVector.assign(outMap[node]->begin(), outMap[node]->end());
                tempOutSet = convertToSetVector(tempOutVector);
                if(isDef(node)) {
                    removeDefSet(tempOutSet, node);
                }
                useSet = generateUses(node);
                useSet->insert(tempOutSet->begin(), tempOutSet->end());
                inMap[node] = useSet;
                // If there was a change
                if(isSetChanged(inMap[node], oldInSet)) {
                    std::vector<Instruction*> preds = getPredecessors(node);
                    // Update changedNodes
                    for(auto p : preds) {
                        changedNodes.push_back(p);
                    }
                } 
            }  
        }
        SetVector<Instruction*>* getAllNodes(Function &F) {
            SetVector<Instruction*>* nodes =  new SetVector<Instruction*>;
            for(inst_iterator I = inst_begin(F), E = inst_end(F); I != E; ++I) { 
                Instruction* instr = &*I;
                nodes->insert(instr);
            }
            return nodes;               
        }
        SetVector<Value*>* generateUses(Instruction* I) {
            SetVector<Value*>* useSet = new SetVector<Value*>;
            for (Use& U : I->operands()){
				Value* v = U.get();
				if(isa<Instruction>(v))
					useSet->insert(v);
			}	
            return useSet;
        }
        void removeDefSet(SetVector<Value*>* tempOutSet, Instruction* node) {
            for(auto t : *tempOutSet) {                
                if (t == node) {            
                    auto def = std::find(tempOutSet->begin(), tempOutSet->end(), t);                        
                    if(def != tempOutSet->end()) {
                        tempOutSet->erase(def);
                    }                                            
                }
            }  
        }
        SetVector<Value*>* convertToSetVector(std::vector<Value*> vector) {
            SetVector<Value*>* sv = new SetVector<Value*>;
            for(auto e : vector) {
                sv->insert(e); 
            }
            return sv;
        }
        SetVector<Instruction*>* convertToInstructionSetVector(std::vector<Instruction*> vector) {
            SetVector<Instruction*>* sv = new SetVector<Instruction*>;
            for(auto e : vector) {
                sv->insert(e); 
            }
            return sv;
        }
        bool isSetChanged(SetVector<Value*>* inMap, SetVector<Value*>* oldInSet) {
            if(inMap->size() == oldInSet->size()) {
                int count = 0;
                for(auto o : *oldInSet) {
                    if(std::find(inMap->begin(), inMap->end(), o) != inMap->end()) {
                        count++;
                    }
                }
                if(count == oldInSet->size()) {
                    return false;
                }
            }
            return true;
        }
        virtual std::string getAnalysisName() override{
            return "Liveness Analysis";
        }
    };
    char LivenessAnalysis::ID = 1;
    static RegisterPass<LivenessAnalysis> X("Liveness", "Liveness Analysis",
                                            false /* Only looks at CFG */,
                                            false /* Analysis Pass */);
}
