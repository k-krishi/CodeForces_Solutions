#include<iostream>
#include<vector>
#include<algorithm>
#include<climits>
typedef long long ll;
using namespace std;

int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int num_fences;
    cin>>num_fences;
    int piano_width;
    cin>>piano_width;
    vector<int> fences_height(num_fences,0);
    for(int i = 0; i<num_fences; i++){
        cin>>fences_height[i];
    }
    int ans = 0;
    int height_sum = INT_MAX;
    for(int i = 0; i<num_fences - piano_width+1; i++){
        int sum = 0;
        for(int j = i; j<i+piano_width; j++){
            sum += fences_height[j];
        }
        if(sum<=height_sum){
            ans = i;
            height_sum = sum;
        }
    }
    cout<<ans+1;
    return 0;
}