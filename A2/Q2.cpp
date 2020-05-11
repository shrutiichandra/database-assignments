#include <iostream>
#include <cstdlib>
#include <fstream>
#include <queue>
#include <cmath>

using namespace std;

class Block {


    vector<int> records;
    Block *overflow;
    unsigned int bufferSize;
    public:
    Block(unsigned int n) {
        overflow = NULL;
        records.clear();
        bufferSize = n;
    }

    bool isPresentBlock(int x) {
        Block *node = this;
        while(node) {
            for(auto i=node->records.begin(); i!= node->records.end(); i++) {
                if(*i == x) {
                    return true;
                }
            }
            node = node->overflow;
        }
        return false;
    }

    void add(int x) {
        
        if(records.size() < (bufferSize / sizeof(int))) {
            records.push_back(x);
        }
        else {
            if(overflow == NULL) {
                overflow = new Block(bufferSize);
            }
            overflow->add(x);
        }
    }

    void clearElements(vector<int> &v) {
        for(auto i = records.begin(); i!= records.end(); i++) {
            v.push_back(*i);
        }
        records.clear();
        if(overflow) {
            overflow->clearElements(v);
            delete overflow;
            overflow = NULL;
        }
    }


};

class HashTable {
    int numRecords, numBits;
    vector<Block *> buckets;
    unsigned int bufferSize;
    public:
    HashTable(unsigned int n) {
        // initial configuration of Hash table
        bufferSize = n;
        numRecords = 0;
        numBits = 1;
        buckets.push_back(new Block(bufferSize));
        buckets.push_back(new Block(bufferSize));
        
    }

    unsigned int hash(int x) {
        unsigned int mod = (1 << numBits);
        unsigned int r = (unsigned int)(x % mod + mod) % mod;

        if(r >= buckets.size()) {
            r -= (1 << (numBits - 1));
        }
        return r;
    }

    int occupancy() {
        double ratio = float (numRecords) / buckets.size();
        return (int)(100 * (ratio / (bufferSize / sizeof(int))));
    }

    bool isPresent(int x) {
        unsigned int k = hash(x);
        
        if(buckets[k]->isPresentBlock(x)) {
            return true;
        }
        return false;
    }

    void insert(int x) {
        unsigned int k = hash(x);
        buckets[k]->add(x);
        numRecords++;
        while(occupancy() >= 75) {
            buckets.push_back(new Block(bufferSize));
            numBits = ceil(log2((double)buckets.size()));
            
            k = buckets.size() - 1 - (1 << (numBits - 1));
            vector<int> v;
            buckets[k]->clearElements(v);
            for(auto i = v.begin();i!= v.end(); i++) {
                buckets[hash(*i)]->add(*i);
            }
        }
    }

    

};

void clearOutput(queue<int>& q, vector<int>& out) {
    int ox;
    while(!q.empty()) {
        ox = q.front();
        q.pop();
        out.push_back(ox);
        cout<<ox<<"\n";
    }
}

void clearInput(queue<int>& in, queue<int>& out, HashTable& h, int outsize, vector<int>& v) {
    int ix;
    while(!in.empty()) {
        ix = in.front();
        in.pop();
        if(!h.isPresent(ix)) {
            h.insert(ix);
            if(out.size() == outsize) {
                clearOutput(out, v);
            }
            out.push(ix);
        }
    }
}
void put_output(vector<int> &v){
    
    ofstream outfile("output.txt", std::ios_base::app);

    for(auto i= v.begin(); i!= v.end(); ++i)
        outfile<<*i<<endl;
    v.clear();  
    outfile.close();

}
int main(int argc, char *argv[]) {
    

    unsigned int numBuffers, bufferSize;
    queue<int> inputBuffer, outputBuffer;
    unsigned int inputSize, outputSize;
    vector<int> v;
    string filename;
    filename = argv[1];

    ifstream input_file(filename);
    numBuffers = atoi(argv[2]); 
    bufferSize = atoi(argv[3]); 
    HashTable h(bufferSize);
    // h = new HashTable(bufferSize);
    
    inputSize = (numBuffers - 1) * (bufferSize / 4);
    outputSize = bufferSize / 4;
    int x;
    while(input_file >> x) {
        if(inputBuffer.size() < inputSize) {
            inputBuffer.push(x);
        }
        else {
            clearInput(inputBuffer, outputBuffer, h, outputSize, v);
            inputBuffer.push(x);
        }
    }
    clearInput(inputBuffer, outputBuffer, h, outputSize, v);
    clearOutput(outputBuffer, v);
    // put_output(v);
    return 0;
}
