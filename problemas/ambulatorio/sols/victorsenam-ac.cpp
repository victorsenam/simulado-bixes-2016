#include <bits/stdc++.h>

using namespace std;

int main () {
    int n;
    scanf("%d", &n);

    int r = 1;

    while (n > 1) {
        n >>= 1;
        r++;
    }
    printf("%d\n", r);
}
