#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n = 0, k = 0;
    cin >> n >> k;
    k--;
    vector<int> a(n);
    int r = 0;
    
    for (int i = 0; i < n; i++)
        cin >> a[i];
    
    for (int j = 0; j < n; j++) {
        if (a[j] >= a[k] && a[j] > 0)
            r++;
    }
    
    cout << r;
    return 0;
}