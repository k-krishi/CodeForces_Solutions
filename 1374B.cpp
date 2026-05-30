#include<iostream>
using namespace std;

int main(){
    int t;
    cin>>t;
    for(int i = 0; i<t; i++){
        int n,m=0;
        cin>>n;
        while(n!=1){
            if(n%6==0) n /= 6;
            else{
                n *= 2;
            }
        }
    }
}