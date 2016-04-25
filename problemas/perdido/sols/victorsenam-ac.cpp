#include <bits/stdc++.h>
using namespace std;

const int N = 1007;

char mat[N][N];
int res;
int att;
int n, m;

int main () {
    scanf("%d %d", &n, &m);

    for (int i =0 ; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf(" %c", &mat[i][j]);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            int p = j;
            if (i&1)
                p = m - j - 1;
            if (mat[i][p] == '.') {
                att++;
            } else if (mat[i][p] == 'L') {
                att = 0;
            }

            res = max(res, att);
        }
    }
    printf("%d\n", res);
}
