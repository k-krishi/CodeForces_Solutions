#include<iostream>
#pragma GCC optimize("Os")

static const int speed = [](){
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);
    return 0;
}();

int main()
{
    int s;
    std::cin>>s;
    if(s%2==0 && s>2) 
        std::cout<<"YES";
    else
        std::cout<<"NO";
    return 0;
}