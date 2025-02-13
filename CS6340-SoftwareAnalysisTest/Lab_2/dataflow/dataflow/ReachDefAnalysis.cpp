#include "DataflowAnalysis.h"
namespace dataflow{
    struct ReachDefAnalysis: public DataflowAnalysis{
        static char ID;
        ReachDefAnalysis() : DataflowAnalysis(ID){}
    protected:
        /**
         *  Implement your analysis in this function. Store your results in DataflowAnalysis::inMap and
         *  DataflowAnalysis:outMap.
         */
        void doAnalysis(Function &F) override {
            // Source: https://en.wikipedia.org/wiki/Reaching_definition#Worklist_algorithm
            SetVector<Instruction*>* nodes = getAllNodes(F);
            std::vector<Instruction*> changedNodes;
            // Put all nodes in changed set            
            changedNodes.assign(nodes->begin(), nodes->end());
            while(!changedNodes.empty()) {                     
                // Get node 
                Instruction* node = changedNodes.front();
                // Remove node n from changed set
                changedNodes.erase(changedNodes.begin());
                // Calculate IN[n] from predecessors' OUT[p]
                std::vector<Instruction*> preds = getPredecessors(node);
                std::vector<Value*> predsVector;
                SetVector<Value*>* predsSet = new SetVector<Value*>;
                for(auto p : preds) {
                    predsVector.assign(outMap[p]->begin(), outMap[p]->end());
                }
                predsSet = convertToSetVector(predsVector);
                predsSet->insert(inMap[node]->begin(), inMap[node]->end());
                inMap[node] = predsSet;
                // Store original OUT[n]
                std::vector<Value*> oldOutVector;
                SetVector<Value*>* oldOutSet = new SetVector<Value*>;
                oldOutVector.assign(outMap[node]->begin(), outMap[node]->end());
                oldOutSet = convertToSetVector(oldOutVector);
                // Update IN[n] with USE[n] U (IN[n]-DEF[n])                            
                std::vector<Value*> tempInVector;
                SetVector<Value*>* tempInSet = new SetVector<Value*>;
                SetVector<Value*>* useSet = new SetVector<Value*>;
                tempInVector.assign(inMap[node]->begin(), inMap[node]->end());
                tempInSet = convertToSetVector(tempInVector);
                if(isDef(node)) {
                    removeDefSet(tempInSet, node);
                }
                useSet = generateUses(node);
                useSet->insert(tempInSet->begin(), tempInSet->end());
                outMap[node] = useSet;
                // If there was a change
                if(isSetChanged(outMap[node], oldOutSet)) {
                    std::vector<Instruction*> succs = getSuccessors(node);
                    // Update changedNodes
                    for(auto s : succs) {
                        changedNodes.push_back(s);
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
            // Source: https://llvm.discourse.group/t/how-to-get-the-value-of-a-result-of-an-instruction/235
            SetVector<Value*>* useSet = new SetVector<Value*>;
            for (Use& U: I->uses()) {
                User* user = U.getUser();
                auto n = U.getOperandNo();
                Instruction* inst = dyn_cast<Instruction>(user);
                Value* value = inst->getOperand(n);
                useSet->insert(value);
            }
            return useSet;
        }
        void removeDefSet(SetVector<Value*>* tempInSet, Instruction* node) {
            for(auto t : *tempInSet) {                
                if (t == node) {            
                    auto def = std::find(tempInSet->begin(), tempInSet->end(), t);                        
                    if(def != tempInSet->end()) {
                        tempInSet->erase(def);
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
        bool isSetChanged(SetVector<Value*>* outMap, SetVector<Value*>* oldOutSet) {
            if(outMap->size() == oldOutSet->size()) {
                int count = 0;
                for(auto o : *oldOutSet) {
                    if(std::find(outMap->begin(), outMap->end(), o) != outMap->end()) {
                        count++;
                    }
                }
                if(count == oldOutSet->size()) {
                    return false;
                }
            }
            return true;
        }
        virtual std::string getAnalysisName() override{
            return "ReachDef";
        }
    };
    char ReachDefAnalysis::ID = 1;
    static RegisterPass<ReachDefAnalysis> X("ReachDef", "Reach Definition Analysis",
                                            false /* Only looks at CFG */,
                                            false /* Analysis Pass */);
}