#include<iostream>
#include<vector>
#include<algorithm>
typedef long long ll;
using namespace std;

int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int num_shops;
    cin >> num_shops;
    vector<int> shop_coin(num_shops);
    for(int i = 0; i < num_shops; i++)
        cin >> shop_coin[i];
    
    sort(shop_coin.begin(), shop_coin.end());
    
    int days;
    cin >> days;
    while(days--){
        ll day_coin;
        cin >> day_coin;
        int ans = upper_bound(shop_coin.begin(), shop_coin.end(), day_coin) - shop_coin.begin();
        cout << ans << "\n";
    }
}