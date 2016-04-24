#include <bits/stdc++.h>
using namespace std;

#include "testlib.h"

char let[6] = {'p','c','t','b','r','k'};
char qtd[6] = {8,2,2,2,1,1};
char pcs[32];
char mat[8][8];

bool gen_uniform () {
    int n = 32;
    int q = 0;
    int t = 0;
    bool ma = 0;
    for (int i = 0; i < n; i++) {
        if (q == qtd[t])
            q = 0, t++;
        if (t == 6)
            ma = 1, t = 0;
        q++;

        pcs[i] = let[t];
        if (ma) 
            pcs[i] += 'A' - 'a';
    }

    int pi = -1;
    int pj = -1;
    q = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (rnd.next(0,1) && n) {
                swap(pcs[rnd.next(n--)], pcs[n]);
                mat[i][j] = pcs[n];

                if (pcs[n] >= 'A' && pcs[n] <= 'Z' && !rnd.next(0,q++)) {
                    pi = i;
                    pj = j;
                }
            } else {
                mat[i][j] = '.';
            }
        }
    }

    if (pi == -1)
        return 0;

    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++)
            putchar(mat[i][j]);
        putchar('\n');
    }
    putchar('a'+pj);
    putchar('1'+pi);
    return 1;
}

int main (int argn, char ** args) {
    registerGen(argn, args, 1);
    while (!gen_uniform());
}
