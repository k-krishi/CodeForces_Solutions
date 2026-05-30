#include<iostream>

using namespace std;

int main(){
    int n;
    int x = 0;
    cin>>n;
    while(n--){
        string s;
        cin>>s;
        int len = s.size();
        if(s[0] == '+' || s[len-1] == '+'){
            x++;
        }
        else if(s[0] == '-' || s[len-1] == '-'){
            x--;
        }
    }
    cout<<x;
    return 0;
}