#include<iostream>
#include<vector>
using namespace std;
#pragma GCC optimize("Ofast, unroll-loops")
typedef long long ll;

static const int _ = [](){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    return 0;
}();

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        vector<ll> a(n,0);
        for(int i = 0; i<n; i++){
            cin>>a[i];
        }
        int k = -1;
        bool b = true;
        for(int i = 1; i<n; i++){
            if(a[i]<a[i-1]){
                k = (k==-1) ? a[i-1]-a[i] : k;
                a[i]+=k;
                if(a[i]<a[i-1]){
                    b = false;
                    break;
                }
            }
        }
        cout<<(b ? "YES" : "NO")<<endl;
    }
    return 0;
}