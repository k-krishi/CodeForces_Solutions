#include <cstdio>

int main()
{
    int n, total = 0;
    int a, b, c;
    scanf("%d", &n);
    while (n--) {
        scanf("%d%d%d", &a, &b, &c);
        total += (a&b) | (b&c) | (a&c);  // bitwise, no branching
    }
    printf("%d", total);
}