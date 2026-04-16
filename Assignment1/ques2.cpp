
#include<iostream>
#include<vector>
#include<unordered_map>
#include<queue>
using namespace std;

unordered_map<string,vector<string>>adj;

void bfs<const string &start>{
    unordered_map<string,bool>visited;
    queue<string>q;

    visited<start>=true;
    result.push(start);
    while(!q.empty()){
        string curr=q.front();
        q.pop();
        cout<<curr<<" ";

        for(auto neighbour:adj){
            if(!visited[neighbour]){
                visited[neighbour]=true;
                cout<<neighbour;
            }
        }
    }
    cout<<endl;
}

