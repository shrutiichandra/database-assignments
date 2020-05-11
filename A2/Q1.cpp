#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include <fstream>
#include <sstream>
#include <climits>
#include <algorithm> //upper_bound


#define pinf INT_MAX
#define ninf INT_MIN

using namespace std;

struct Node{
	Node* parent;
	vector<int> keys;
	vector<Node*> pointer;
	Node* buffer;
	bool flag_arr[2]; //<dead, eaf>
};

class Tree{
	public:
	Node* createNode(int n, bool isLeaf){
		Node* node = new Node;
		node->parent = NULL;
		node->buffer = NULL;

		node->keys = vector<int>(n, pinf);
		node->pointer = vector<Node*>(n+1);
		

		node->flag_arr[0] = false;
		node->flag_arr[1] = isLeaf;
		
		return node;
	}

	void makeAlive(Node* parent, Node* child, int value){
		int idx=0;
		if(parent != NULL){
			bool flag = false;
			for (auto i = parent->pointer.begin()+1; i!= parent->pointer.end(); i++){
				idx++;
				if(*i == child){
					flag = true;
					parent->keys[idx] = value;
				}
			}
			if(parent->flag_arr[0] && flag == true)
				makeAlive(parent->parent, parent, value);
		}
	}

	int getUpperBound(vector<int>&v, int val){
		int upper_bnd = upper_bound(v.begin(), v.end(), val) - v.begin();
		return upper_bnd;
	}

	Node* insert(Node* node, int value)	{
		
		int node_size = node->keys.size();
		bool isFull = false;
		
		Node* root = NULL;
		
		if(node->keys[node_size - 1] != pinf)
			isFull = true;
		int idx;
		if(isFull == false){
			bool insert_flag = false;
			int tempKey = pinf;
			Node* tempPointer = NULL;
			idx = -1;
			
			for (auto i= node->keys.begin(); i!= node->keys.end(); i++){
				idx++;
				if(insert_flag == true){
					swap(*i, tempKey);
					if(node->flag_arr[1] == false)
						swap(node->pointer[idx + 1], tempPointer);
				}
				else{
					if(value < *i || *i == pinf){
						insert_flag = true;
						tempKey = *i;
						*i = value;
						if(!node->flag_arr[1]){
							tempPointer = node->pointer[idx + 1];
							node->pointer[idx + 1] = node->buffer;
						}
					}
					if(value != node->keys[0] && node->flag_arr[0]){
						node->flag_arr[0] = false;
						makeAlive(node->parent, node, value);
					}
				}
			}
		}
		else{
			vector<int> temp_keys_vec = node->keys;
			vector<Node*> temp_ptr_vec = node->pointer;
			
			int tempIndex =  getUpperBound(temp_keys_vec, value);
			int u, new_val;
			double x;
			temp_keys_vec.insert(temp_keys_vec.begin() + tempIndex, value);
			
			if(node->flag_arr[1] == false)
				temp_ptr_vec.insert(temp_ptr_vec.begin() + tempIndex + 1, node->buffer);
			
			Node* new_node = createNode(node_size, node->flag_arr[1]);
			new_node->parent = node->parent;
			
			if(node->flag_arr[1] == true){
				new_node->pointer[node_size] = node->pointer[node_size];
				node->pointer[node_size] = new_node;

				x = node_size + 1;
				u = (int)ceil(x/2);
			}
			else{
				x = node_size + 2;
				u = (int)ceil((x)/2);
				idx = -1;
				for (auto i = temp_ptr_vec.begin(); i!= temp_ptr_vec.end(); i++){
					idx ++;
					if(idx < u)
						node->pointer[idx] = *i;
					else{
						new_node->pointer[idx - u] = *i;
						new_node->pointer[idx - u]->parent = new_node;
						if(idx <= node_size)
							node->pointer[idx] = NULL;
					}
				}

				u--;
				new_val = temp_keys_vec[u];
				temp_keys_vec.erase(temp_keys_vec.begin() + u);
			}
			idx = -1;
			for (auto i = temp_keys_vec.begin(); i!= temp_keys_vec.end(); i++){
				idx++;
				if(idx < u)
					node->keys[idx] = *i;
				else{
					new_node->keys[idx - u] = *i;
				
					if(idx < node_size)
						node->keys[idx] = pinf;
				}
			}

			if(node->flag_arr[0] && value != node->keys[0] && tempIndex < u){
				node->flag_arr[0] = false;
				makeAlive(node->parent, node, value);
			}

			tempIndex = getUpperBound(new_node->keys, node->keys[u-1]);
			if(new_node->keys[tempIndex] == pinf){
				new_val = new_node->keys[0];
				new_node->flag_arr[0] = true;
			}
			else if(node->flag_arr[1])
				new_val = new_node->keys[tempIndex];

			if(node->parent != NULL){
				
				node->parent->buffer = new_node;
				root = insert(node->parent, new_val);
			}
			else{
				root = createNode(node_size, false);

				root->keys[0] = new_val;
				root->pointer[0] = node;
				node->parent = root;
				root->pointer[1] = new_node;
				new_node->parent = root;
			}
			
		}
		return root;
	}

	Node* lookup(Node* node, int value, bool up){
		while(!node->flag_arr[1]){
			int lower_bnd = ninf, upper_bnd, node_size = node->keys.size(), index;
			for (int i = 0; i < node_size; i++){
				if(node->keys[i] == pinf){
					index = i;
					break;
				}
				upper_bnd = node->keys[i];

				if(lower_bnd <= value && value < upper_bnd){
					index = i;
					break;
				}

				else if(lower_bnd <= value && value == upper_bnd && !up && node->pointer[i + 1] -> flag_arr[0]){
					index = i;
					break;
				}

				else
					index = i + 1;
				lower_bnd = upper_bnd;
			}
			node = node->pointer[index];
		}
		return node;
	}

	Node* insert_val(Node* root, int value){
		Node* temp;
		Node* n = lookup(root, value, true);
		temp = insert(n, value);
		if(temp != NULL)
			root = temp;
		return root;
	}

	bool find(Node* leaf, int val){
		for (auto i = leaf->keys.begin(); i!= leaf->keys.end(); i++){
			if(*i == val)
				return true;
		}
		return false;
	}



	void range(Node* leaf, int lower_bnd, int upper_bnd, vector<string>& v){
		int count = 0, flag = false;
		int num_pointers = leaf->pointer.size();
		int last_index = num_pointers - 1;
		
		while(leaf != NULL){
			for (auto i = leaf->keys.begin(); i!= leaf->keys.end(); i++){
				if(*i > upper_bnd && *i != pinf){
					flag = true;
					break;
				}

		
				else if(*i >= lower_bnd && *i <= upper_bnd)
					count ++;
					
			}
			if(flag)
				break;
			leaf = leaf->pointer[last_index];
		}
		v.push_back(to_string(count));
		return;
	}

	int count(Node* leaf, int val){
		int count = 0, flag = false;
		int num_pointers = leaf->pointer.size();
		int last_index = num_pointers - 1;
		
		while(leaf != NULL){
			for (auto i = leaf->keys.begin(); i != leaf->keys.end(); i++){
				
				if(*i > val){
					if(*i != pinf){
						flag = true;
						break;
					}
				}
				else if(*i == val)
					count++;
			}
			if(flag)
				break;
			leaf = leaf->pointer[last_index];
		}
		return count;
	}



};



bool isPresent(string s, string sub){
    if (s.find(sub)!= string::npos)
        return true;
    return false;
}
void put_output(vector<string> &v){
    
    ofstream outfile("output.txt", std::ios_base::app);

    for(auto i= v.begin(); i!= v.end(); ++i)
        outfile<<*i<<endl;
    v.clear();  
    outfile.close();

}
int main(int argc, char const *argv[]){
	int n, B, M;

	
	string file_name;
	file_name = argv[1];
	B=(long long) argv[2];
	n = (B - 1)/4;

	if(n < 2)
		n = 2;
	
	// fileRead(n, file_name);
	Tree t;
	Node* root = t.createNode(n, true);
	int value1, value2;
	string line;
	ifstream input_file(file_name);
	vector <string> out;
	while(getline(input_file, line)){
		if(isPresent(line, "INSERT")){
			istringstream (line.substr(7)) >> value1;
			root = t.insert_val(root, value1);
		}
		else if(isPresent(line, "RANGE")){
			istringstream (line.substr(6)) >> value1 >> value2;
			t.range(t.lookup(root, value1, false), value1, value2, out);
		}
		else if(isPresent(line, "FIND")){
			istringstream (line.substr(5)) >> value1;
			if(t.find(t.lookup(root, value1, false), value1)){
				out.push_back("YES");
				// cout<<"YES\n";
			}
			else{
				out.push_back("NO");
				// cout<<"NO\n";
			}
		}
		else if(isPresent(line, "COUNT")){
			istringstream (line.substr(6)) >> value1;
			string ans = to_string(t.count(t.lookup(root, value1, false), value1));
			out.push_back(ans);
			// cout<<to_string(t.count(t.lookup(root, value1, false), value1))<<"\n";
		}
		
	}

	put_output(out);
	return 0;
}